import logging
from typing import List

from movies_converter_src.models.film import FilmFile, TransformResult, TransformResults
from movies_converter_src.transform.BaseMovieFilesTransformer import BaseMovieFilesTransformer


class FakeMovieFilesTransformer(BaseMovieFilesTransformer):
    def __init__(self, extracted_movies: str):
        super().__init__(extracted_movies)

    def transform_movies(self, *args, **kwargs) -> TransformResults:
        logging.debug(self.extracted_movies)
        return TransformResults(
            results=[
                TransformResult(
                    film_id=film.film_id,
                    film_files=[
                        FilmFile(resolution=resolution, destination_path=f"{resolution}_{film.file_name}")
                        for resolution in film.resolutions
                    ],
                )
                for film in self.extracted_movies.films
            ]
        )
