from random import choice
from typing import List
from uuid import uuid4

from movies_converter_src.core.config.db import DBConfig, get_converter_db_config
from movies_converter_src.extract.BaseMovieFilesExtractor import BaseMovieFilesExtractor
from movies_converter_src.models.film import Film, Films


class DBMovieFilesExtractor(BaseMovieFilesExtractor):
    def __init__(self, query_path: str = "", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        db_config: DBConfig = get_converter_db_config()
        self.dsn = {
            "dbname": db_config.postgres_db,
            "user": db_config.postgres_user,
            "password": db_config.postgres_password,
            "host": db_config.postgres_host,
            "port": db_config.postgres_port,
            "options": "-c search_path=content",
        }

        self.movies_len = 20

    def extract_movies(self, *args, **kwargs) -> Films:
        films: List[Film] = []
        for index in range(self.movies_len):
            source_resolution: int = choice(self.resolutions)
            films.append(
                Film(
                    film_id=uuid4(),
                    file_name=f"movie_{index}.mkv",
                    destination_path="/cinema/movies/converted/",
                    source_path="/cinema/movies/",
                    source_resolution=source_resolution,
                    reqired_resolutions=[
                        resolution for resolution in self.resolutions if resolution < source_resolution
                    ],
                )
            )
        return Films(films=films)
