from functools import lru_cache

from pydantic import BaseSettings, Field


class Config(BaseSettings):
    # prod_mode: bool = Field(False, env="PROD_MODE")
    prod_mode: bool = Field(True, env="PROD_MODE")
    schedule_interval: str = Field("00 12 * * *", env="SCHEDULE_INTERVAL")

    class Config:
        env = ".env"


@lru_cache()
def get_config():
    return Config()
