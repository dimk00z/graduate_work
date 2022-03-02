import logging
from random import choice

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
                        FilmFile(
                            resolution=resolution,
                            succeded=choice((True, False)),
                            destination_path=f"{resolution}p_{film.file_name}",
                        )
                        for resolution in film.reqired_resolutions
                    ],
                )
                for film in self.extracted_movies.films
            ]
        )
