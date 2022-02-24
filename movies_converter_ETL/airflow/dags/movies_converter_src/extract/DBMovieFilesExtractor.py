from typing import List
from uuid import uuid4

from movies_converter_src.extract.BaseMovieFilesExtractor import BaseMovieFilesExtractor
from movies_converter_src.models.film import Film


class DBMovieFilesExtractor(BaseMovieFilesExtractor):
    def __init__(self, movies_len: int = 20) -> None:
        self.movies_len = movies_len

    def extract_movies(self, *args, **kwargs) -> List[str]:
        movies: List[Film] = []
        resolutions: List[str] = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "120p"]
        for index in range(self.movies_len):
            movies.append(
                Film(
                    film_id=uuid4(),
                    source_file_path=f"/cinema/movies/movie_{index}.mkv",
                    resolutions=resolutions,
                )
            )
        return movies
