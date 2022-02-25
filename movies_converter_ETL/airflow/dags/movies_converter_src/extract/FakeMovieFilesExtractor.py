from typing import List
from uuid import UUID, uuid4

from movies_converter_src.extract.BaseMovieFilesExtractor import BaseMovieFilesExtractor
from movies_converter_src.models.film import Film, Films


class FakeMovieFilesExtractor(BaseMovieFilesExtractor):
    def __init__(self, movies_len: int = 20) -> None:
        self.movies_len = movies_len

    def extract_movies(self, *args, **kwargs) -> List[str]:
        resolutions: List[str] = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "120p"]

        return Films(
            films=[
                Film(
                    film_id=uuid4(),
                    file_name=f"movie_{index}.mkv",
                    source_file_path=f"/cinema/movies/",
                    resolutions=resolutions,
                )
                for index in range(self.movies_len)
            ]
        ).json()
