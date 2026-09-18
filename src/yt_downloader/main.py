import logging

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from yt_downloader.utils import setup_logging
from yt_downloader.router import router

app = FastAPI()

app.include_router(router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


def main() -> None:
    setup_logging(logging.INFO)
    uvicorn.run("yt_downloader:app", host="0.0.0.0", port=80, log_config=None)  # noqa: S104


if __name__ == "__main__":
    main()
