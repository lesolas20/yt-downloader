FROM debian:12.12 AS yt-downloader-base

WORKDIR /app

RUN apt-get update \
    && apt-get install -y btop iputils-ping lsd \
    && apt-get install -y python3 python3-pip python3-venv \
    && apt-get install -y ffmpeg \
    && apt-get install -y nodejs npm \
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
