from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    ydl_options: dict
    progress_update_in_seconds: float
    progress_update_in_bytes: float
