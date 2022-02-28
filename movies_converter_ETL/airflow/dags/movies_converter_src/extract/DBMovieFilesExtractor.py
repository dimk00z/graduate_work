from logging import Logger
from pathlib import Path
from random import choice
from typing import List
from uuid import UUID, uuid4

import psycopg2
from airflow.utils.log.logging_mixin import LoggingMixin
from movies_converter_src.core.config.db import DBConfig, get_converter_db_config
from movies_converter_src.extract.BaseMovieFilesExtractor import BaseMovieFilesExtractor
from movies_converter_src.models.film import Film, Films

logger: Logger = LoggingMixin().log


class DBMovieFilesExtractor(BaseMovieFilesExtractor):
    def __init__(self, *args, **kwargs) -> None:
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
        query_path: Path = Path(Path(__file__).parent.resolve(), Path(db_config.query_location))

        with open(query_path) as query_file:
            self.query: str = query_file.read()

        logger.info(self.query)

    def _fetch_db(self):
        try:
            with psycopg2.connect(**self.dsn) as conn, conn.cursor() as cursor:
                cursor.execute(self.query)
                extracted_movies = cursor.fetchall()
        except psycopg2.OperationalError as e:
            logger.exception(e)

    def extract_movies(self, *args, **kwargs) -> Films:
        films: List[Film] = []
        extracted_movies = self._fetch_db()
        for movie_row in extracted_movies:
            films.append(
                Film(
                    film_id=UUID(movie_row["fw_id"]),
                    file_name=movie_row["file_name"],
                    reqired_resolutions=[
                        resolution
                        for resolution in self.resolutions
                        if resolution not in movie_row["resolutions"]
                    ],
                    source_resolution=movie_row["source_resolution"],
                    source_path=movie_row["source_path"],
                    destination_path=movie_row["destination_path"],
                )
            )

        return Films(films=films)
