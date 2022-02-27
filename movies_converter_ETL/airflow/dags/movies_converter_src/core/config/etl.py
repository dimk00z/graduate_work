from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    convert_api_host: str = Field("convert_api:8000", env="CONVERT_API_HOST")
    codec_name: Optional[str] = Field(None, env="CODEC_NAME")
    display_aspect_ratio: Optional[str] = Field(None, env="DISPLAY_ASPECT_RATIO")
    fps: Optional[str] = Field(None, env="FPS")
    prod_mode: bool = Field(False, env="PROD_MODE")
    schedule_interval: str = Field("00 12 * * *", env="SCHEDULE_INTERVAL")

    class Config:
        env = ".env"


@lru_cache()
def get_config():
    return Config()
