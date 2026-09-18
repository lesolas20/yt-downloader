from typing import Annotated
from pathlib import Path

import yaml
from fastapi import Depends, APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from yt_downloader.utils import Config
from yt_downloader.downloader import process_download_request

router = APIRouter()


class SubmitDownloadRequest(BaseModel):
    text: str


def load_config() -> Config:
    with Path("config.yaml").open() as file:
        config = yaml.safe_load(file)

    ydl_options = config["yt_dlp"]
    progress_update_in_seconds = config["progress"]["update_in_seconds"]
    progress_update_in_bytes = config["progress"]["update_in_bytes"]

    return Config(
        ydl_options=ydl_options,
        progress_update_in_seconds=progress_update_in_seconds,
        progress_update_in_bytes=progress_update_in_bytes,
    )


ConfigDependency = Annotated[Config, Depends(load_config)]


@router.post("/api/submit")
def submit(
    body: SubmitDownloadRequest,
    config: ConfigDependency,
    background_tasks: BackgroundTasks,
) -> None:
    if not body.text:
        raise HTTPException(status_code=400, detail="Empty text")

    background_tasks.add_task(
        process_download_request,
        text=body.text,
        config=config,
    )
