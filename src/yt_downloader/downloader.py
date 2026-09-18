import time
import logging
from typing import TYPE_CHECKING
from threading import Thread, Semaphore

from yt_dlp import YoutubeDL

if TYPE_CHECKING:
    from collections.abc import Mapping, Iterable

    from yt_downloader.utils import Config


logger = logging.getLogger(__name__)


downloader_semaphore = Semaphore(value=1)

LAST_PROGRESS_TIME: float = time.monotonic()
LAST_PROGRESS_BYTES: int = 0


class YDLLogger:
    @staticmethod
    def debug(message: str) -> None:
        logger.debug(message)

    @staticmethod
    def info(message: str) -> None:
        logger.info(message)

    @staticmethod
    def warning(message: str, *, once: bool = False) -> None:  # noqa: ARG004
        logger.warning(message)

    @staticmethod
    def error(message: str, *, is_error: bool = True) -> None:  # noqa: ARG004
        logger.error(message)

    @staticmethod
    def stdout(message: str) -> None:
        logger.info(message)

    @staticmethod
    def stderr(message: str) -> None:
        logger.error(message)


def load_ydl_options(config: Config):  # noqa: ANN201
    def _ydl_progress_hook(data: Mapping) -> None:
        global LAST_PROGRESS_TIME, LAST_PROGRESS_BYTES  # noqa: PLW0603

        status: str = data["status"]
        statistic: str = data["_default_template"]
        downloaded_bytes: int = data["downloaded_bytes"]

        t = time.monotonic()
        time_delta = t - LAST_PROGRESS_TIME
        data_delta = downloaded_bytes - LAST_PROGRESS_BYTES

        if (
            (status == "finished")
            | (time_delta >= config.progress_update_in_seconds)
            | (data_delta >= config.progress_update_in_bytes)
        ):
            logger.debug(f"[{status}] {statistic}")

            LAST_PROGRESS_TIME = time.monotonic()
            LAST_PROGRESS_BYTES = downloaded_bytes

    ydl_options = config.ydl_options

    ydl_options["logger"] = YDLLogger
    ydl_options["progress_hooks"] = [_ydl_progress_hook]

    return ydl_options


def download(semaphore: Semaphore, text: str, ydl_options) -> None:  # noqa: ANN001
    with semaphore:
        urls: Iterable[str] = text.split()

        with YoutubeDL(ydl_options) as ydl:
            for url in urls:
                ydl.download(url)


def process_download_request(text: str, config: Config) -> None:
    ydl_options = load_ydl_options(config=config)

    t = Thread(
        target=download,
        kwargs={
            "semaphore": downloader_semaphore,
            "text": text,
            "ydl_options": ydl_options,
        },
    )
    t.start()
