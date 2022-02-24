from airflow.utils.log.logging_mixin import LoggingMixin
from movies_converter_src.load.BaseMovieFilesLoader import BaseMovieFilesLoader
from movies_converter_src.models.film import Film, Films


class FakeMovieFilesLoader(BaseMovieFilesLoader):
    def __init__(self, transform_result: str, *args, **kwargs) -> None:
        super().__init__(transform_result, *args, **kwargs)

    def load_movies_files(self, *args, **kwargs):
        LoggingMixin().log.info("Files loaded")

    def update_movies(self, *args, **kwargs):
        LoggingMixin().log.info("Movies updated")
