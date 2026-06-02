FROM debian:bookworm-slim AS yt-downloader-base

ARG DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update \
    && apt-get install --yes --no-install-recommends python3 python3-pip python3-venv \
    && apt-get install --yes --no-install-recommends ffmpeg \
    && apt-get install --yes --no-install-recommends nodejs npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && npm install -g deno \
    && npm cache clean --force


FROM yt-downloader-base AS main

COPY requirements.txt config.yaml cookies.txt \
    server.py index.html styles.css main.js \
    .

RUN python3 -m venv venv \
    && ./venv/bin/pip install --upgrade pip \
    && ./venv/bin/pip install -r requirements.txt

CMD ["./venv/bin/python", "server.py"]
