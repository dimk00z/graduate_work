from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, Field


class DBConfig(BaseSettings):
    postgres_db: str = Field("online_movie_theater_db", env="POSTGRES_DB")
    postgres_host: str = Field("postges_movie_db", env="POSTGRES_HOST")
    postgres_port: str = Field("5432", env="POSTGRES_PORT")
    postgres_user: str = Field("postgres", env="POSTGRES_USER")
    postgres_password: str = Field("1234", env="POSTGRES_PASSWORD")

    class Config:
        env = ".env"


@lru_cache()
def get_converter_db_config():
    return DBConfig()
