import sys
import json
import signal
import http.server
from pathlib import Path
from collections.abc import Iterable

import yaml
from yt_dlp import YoutubeDL

SERVER_ADDRESS: str = "0.0.0.0"  # noqa: S104
SERVER_PORT: int = 80

YDL_OPTIONS: dict = None


class WebServerHandler(http.server.SimpleHTTPRequestHandler):
    allowed_paths = ("/api/submit",)

    def do_POST(self) -> None:
        if self.path not in self.allowed_paths:
            self.send_response(404)
            self.end_headers()
            return

        if self.path == "/api/submit":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data)
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return

            text = data.get("text", "")

            if not text:
                self.send_error(400, "Empty text")
                return

            self.process_text(text)

            self.send_response(200)
            self.end_headers()

    def do_OPTIONS(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", SERVER_ADDRESS)
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.end_headers()

    def process_text(self, text: str) -> None:
        links: Iterable[str] = text.split()
        with YoutubeDL(YDL_OPTIONS) as ydl:
            ydl.download(links)


def handle_signal(signum, frame):  # noqa: ARG001
    if signum == signal.SIGTERM:
        print("Exiting on SIGTERM")
        sys.exit(0)


if __name__ == "__main__":
    with Path("config.yaml").open() as file:
        config = yaml.safe_load(file)
    YDL_OPTIONS = config["yt_dlp"]

    server_address = (SERVER_ADDRESS, SERVER_PORT)
    httpd = http.server.HTTPServer(server_address, WebServerHandler)
    signal.signal(signal.SIGTERM, handle_signal)
    httpd.serve_forever()
