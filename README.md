# yt-downloader
A simple web-based video downloader that accepts URLs via a minimal web interface and uses yt-dlp to download videos.

## Installation
```bash
git clone --depth 1 https://github.com/lesolas20/yt-downloader
```

### Dependencies
- Rootless Docker
- Docker Compose

## Setup
- Get a cookiefile for yt-dlp to use (see [yt-dlp wiki](https://www.reddit.com/r/youtubedl/wiki/cookies/)) and save it in the service directory (yt-downloader/cookies.txt).

## Usage
```bash
docker compose build
docker compose up
```

## Configuration
Configuration can be changed by editing `config.yaml`.
Changes to the configuration file will take effect on the next download send from the web interface.

### Configuration options
- progress.update_in_seconds — minimal time passed in seconds before downloader displays its progress again
- progress.update_in_bytes — minimal downloaded data size in bytes before downloader displays its progress again
- yt_dlp — yt-dlp configuration options. See [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp) for available options

### Default configuration
- progress.update_in_seconds: 10
- progress.update_in_bytes: 104857600 (100 MiB)

- yt_dlp:
  - Format: best quality 1080p video, lower resolution if 1080p is unavailable
  - Output file name:
    - `title - channel - date [YT ID]` for individual videos
    - `playlist/# - title - channel - date [YT ID]` for playlists
  - SponsorBlock: remove sponsored segments
  - Rate limits to reduce the risk of getting banned

### Using configuration scripts
The `cli-to-yaml` script translates yt-dlp CLI arguments to a YAML configuration used in `yt_dlp` block in `config.yaml`.

#### Example usage
```bash
docker compose build
docker run --rm -it yt-downloader-server cli-to-yaml --live-from-start --format 'bestvideo[height<=1080]+bestaudio/best[height<=1080]' --limit-rate 20M
```

#### Result
```yaml
yt_dlp:
  format: bestvideo[height<=1080]+bestaudio/best[height<=1080]
  live_from_start: true
  ratelimit: 20971520
```

#### By default, the configuration produced by this command is used
```bash
docker compose build
docker run --rm -it yt-downloader-server cli-to-yaml \
--cookies cookies.txt \
--paths /app/downloads \
--no-playlist \
--no-progress \
--live-from-start \
--embed-metadata --embed-chapters \
--sponsorblock-mark selfpromo,preview --sponsorblock-remove sponsor \
--output './%(playlist&{}|)s/%(playlist_index&{} - |)s%(title)s - %(channel)s - %(release_date>%Y-%m-%d,upload_date>%Y-%m-%d)s [%(id)s].%(ext)s' \
--format 'bestvideo[height<=1080]+bestaudio/best[height<=1080]' \
--extractor-args 'youtube:player_client=default,web_embedded,mweb,tv' \
--sleep-requests 1 --sleep-interval 5 --max-sleep-interval 15 --sleep-subtitles 5 \
--limit-rate 10M \
--verbose
```
