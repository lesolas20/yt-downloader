# yt-downloader
A simple web-based video downloader that accepts URLs via a minimal web interface and uses yt-dlp to download videos.
> [!IMPORTANT]
> This service is intended for local use and is not suitable for commercial or production environments. It uses Python's built-in http.server, which is not recommended for production due to its lack of advanced security features and limited capabilities.

## Installation
```bash
git clone --depth 1 https://github.com/lesolas20/yt-downloader
```

### Dependencies
- git
- yq
- Podman
- Python

## Setup
- Get a cookiefile for yt-dlp to use (see [yt-dlp wiki](https://www.reddit.com/r/youtubedl/wiki/cookies/)) and save it in the service directory (yt-downloader/cookies.txt).

## Usage
```bash
cd yt-downloader
./deploy
```
The deployment script will build and run the container.

After making changes to any configuration files, the container has to be rebuilt for the changes to take effect. For that, before running `./deploy`, run this:
```bash
podman stop yt-downloader
podman rm yt-downloader
podman rmi yt-downloader
```

## Configuration
Configuration can be changed by editing `config.yaml`.

### Configuration options:
- server.port — port on the host machine on which the web interface will be available
- paths.log — file where the logs will be written to
- paths.cookies — file to read cookies from
- paths.output — directory where downloaded videos will be saved to
- yt_dlp — yt-dlp configuration options. See [yt-dlp documentation](https://github.com/yt-dlp/yt-dlp) for available options

### Default configuration
- server.port: 9320
- paths.log: server.log
- paths.cookies: cookies.txt
- paths.output: ~/Videos

- yt_dlp:
  - Format: best quality 1080p video, lower resolution if 1080p is unavailable
  - Output file name:
    - `title - channel - date [YT ID]` for individual videos
    - `playlist/# - title - channel - date [YT ID]` for playlists
  - SponsorBlock: remove sponsored segments
  - Rate limits to reduce the risk of getting banned

### Using configuration scripts
The `cli_to_yaml.py` script translates yt-dlp CLI arguments to a YAML configuration used in `yt_dlp` block in `config.yaml`. To use the script, ensure that Python is installed.

#### Setup
```bash
# Create a virtual environment and install required libraries for running the script
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

> [!TIP]
> When no longer needed, the virtual environment can be deactivated by running `deactivate`.

#### Example usage:
```bash
python3 cli_to_yaml.py --live-from-start --format 'bestvideo[height<=1080]+bestaudio/best[height<=1080]' --limit-rate 20M
```

#### Result:
```yaml
yt_dlp:
  format: bestvideo[height<=1080]+bestaudio/best[height<=1080]
  ignoreerrors: only_download
  ratelimit: 20971520
  retries: 10
  fragment_retries: 10
  extract_flat: discard_in_playlist
  live_from_start: true
  postprocessors:
  - key: FFmpegConcat
    only_multi_video: true
    when: playlist
  warn_when_outdated: true
```

## Updating
```bash
# Remove old container and image
podman stop yt-downloader
podman rm yt-downloader
podman rmi yt-downloader

# Pull updates
git pull
```

## Uninstallation
```bash
# Remove container and images
podman stop yt-downloader
podman rm yt-downloader
podman rmi yt-downloader
podman rmi yt-downloader-base

cd ..

# Remove service files
rm -rfI ./yt-downloader
```
