import sys

import yaml
from cli_to_api import cli_to_api

if __name__ == "__main__":
    data = cli_to_api(sys.argv[1:], True)
    print(yaml.dump({"yt_dlp": data}, sort_keys=False))
