from typing import List
from uuid import uuid4

from movies_converter_src.core.config.db import DBConfig, get_converter_db_config
from movies_converter_src.extract.BaseMovieFilesExtractor import BaseMovieFilesExtractor
from movies_converter_src.models.film import Film, Films


class DBMovieFilesExtractor(BaseMovieFilesExtractor):
    def __init__(self, query_path: str = "") -> None:
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
        resolutions: List[str] = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "120p"]
        extracted_films: Films = Films(
            films=[
                Film(
                    film_id=uuid4(),
                    file_name=f"movie_{index}.mkv",
                    destination_path="/cinema/movies/converted/",
                    source_path="/cinema/movies/",
                    resolutions=resolutions,
                )
                for index in range(self.movies_len)
            ]
        )
        return extracted_films
