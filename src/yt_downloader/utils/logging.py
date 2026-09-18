import logging
from datetime import datetime


class LoggingFormatter(logging.Formatter):
    """Override `logging.Formatter` to use aware datetime objects."""

    def formatTime(self, record, datefmt=None):  # noqa: ANN001, ANN201, N802
        dt = datetime.fromtimestamp(record.created).astimezone()

        if datefmt:
            return dt.strftime(datefmt)

        return dt.isoformat(timespec="milliseconds")


def setup(level: int = logging.INFO) -> None:
    """Create the root logger and set its format and log handlers.
    Set the log level for the stderr stream handler to `level`."""

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    formatter = LoggingFormatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    stderr = logging.StreamHandler()
    stderr.setLevel(level)
    stderr.setFormatter(formatter)

    file = logging.FileHandler("server.log")
    file.setLevel(logging.DEBUG)
    file.setFormatter(formatter)

    root_logger.addHandler(stderr)
    root_logger.addHandler(file)
