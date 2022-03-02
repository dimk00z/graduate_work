import logging
from logging import Logger
from random import choice
from typing import List, Optional

from airflow.utils.log.logging_mixin import LoggingMixin
from movies_converter_src.core.config.converter_api import ConverterAPIConfig, get_converter_API_config
from movies_converter_src.models.film import Film, FilmFile, Films, TransformResult, TransformResults
from movies_converter_src.transform.BaseMovieFilesTransformer import BaseMovieFilesTransformer
from requests import ConnectionError, ConnectTimeout, HTTPError, ReadTimeout, Timeout
from requests import get as http_get

logger: Logger = LoggingMixin().log


class ApiMovieFilesTransformer(BaseMovieFilesTransformer):
    def __init__(self, extracted_movies: str):
        super().__init__(extracted_movies)
        self.config: ConverterAPIConfig = get_converter_API_config()

    def _convert_file(self, film: Film, resolution: int) -> FilmFile:
        "Отправка запросов на API для конвертацию файлов"
        result: FilmFile = FilmFile(
            resolution=resolution, destination_path=film.destination_path, succeded=False
        )
        params = {
            "source_path": film.source_path,
            "destination_path": film.destination_path,
            "resolution": f"{resolution}p",
        }
        if self.config.codec_name:
            params["codec_name"] = self.config.codec_name
        if self.config.display_aspect_ratio:
            params["display_aspect_ratio"] = self.config.display_aspect_ratio
        if self.config.fps:
            params["fps"] = self.config.fps
        try:
            response = http_get(self.config.convert_api_host, params=params)
            response.raise_for_status()
            if response.status_code != 200:
                return result
            result.succeded = result.json()["result"]

        except (ConnectTimeout, HTTPError, ReadTimeout, Timeout, ConnectionError) as err:
            logger.exception(err)
        return result

    def _transform_movie(self, film: Film) -> TransformResult:
        film_files: List[FilmFile] = [
            self._convert_file(film, resolution) for resolution in film.reqired_resolutions
        ]

        return TransformResult(film_id=film.film_id, film_files=film_files)

    def transform_movies(self, *args, **kwargs) -> TransformResults:

        logging.debug(self.extracted_movies)
        results: List[TransformResult] = [
            self._convert_movie(film=film) for film in self.extracted_movies.films
        ]

        return TransformResults(results=results)
