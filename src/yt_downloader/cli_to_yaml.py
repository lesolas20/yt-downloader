#!/usr/bin/env python3

import re
import sys
import optparse
from typing import TYPE_CHECKING

import yaml
import yt_dlp
import yt_dlp.options

if TYPE_CHECKING:
    from collections.abc import Mapping


def diff_mappings(old: Mapping, new: Mapping) -> dict:
    return {key: value for key, value in new.items() if old[key] != value}


def cli_to_yaml() -> None:
    args = sys.argv[1:]

    # NOTE: `argv` is a `Collection` instead of `None` to avoid yt-dlp
    # using data from `sys.argv`
    default_config = yt_dlp.parse_options([]).ydl_opts

    try:
        passed_config = yt_dlp.parse_options(args).ydl_opts

    except optparse.OptParseError as e:
        m = re.match(r"^.*?error: (.*$)\n", e.msg, flags=re.DOTALL)

        if m is None:
            print(e.msg)  # noqa: T201
            return

        error_message = m.groups()[0]
        print(f"Error: {error_message}")  # noqa: T201
        return

    diff = diff_mappings(default_config, passed_config)

    yaml.safe_dump(data={"yt_dlp": diff}, stream=sys.stdout, sort_keys=True)


if __name__ == "__main__":
    cli_to_yaml()
