import logging
from typing import List

from movies_converter_src.models.film import FilmFile, FilmFiles
from movies_converter_src.transform.BaseMovieFilesTransformer import BaseMovieFilesTransformer


class FakeMovieFilesTransformer(BaseMovieFilesTransformer):
    def __init__(self, extracted_movies: str):
        super().__init__(extracted_movies)

    def transform_movies(self, *args, **kwargs):
        result: List[str] = []
        logging.debug(self.extracted_movies)
        for film in self.extracted_movies.films:
            result.append(
                FilmFiles(
                    film_id=film.film_id,
                    film_files=[
                        FilmFile(resolution=resolution, file_name=f"{resolution}_{film.file_name}")
                        for resolution in film.resolutions
                    ],
                ).json()
            )
        return result
