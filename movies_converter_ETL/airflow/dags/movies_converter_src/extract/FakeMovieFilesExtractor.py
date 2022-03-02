from random import choice
from typing import List
from uuid import uuid4

from movies_converter_src.extract.BaseMovieFilesExtractor import BaseMovieFilesExtractor
from movies_converter_src.models.film import Film, Films


class FakeMovieFilesExtractor(BaseMovieFilesExtractor):
    def __init__(self, movies_len: int = 20, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.movies_len = movies_len

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
