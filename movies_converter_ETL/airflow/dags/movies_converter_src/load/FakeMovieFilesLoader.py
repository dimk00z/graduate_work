from airflow.utils.log.logging_mixin import LoggingMixin
from movies_converter_src.load.BaseMovieFilesLoader import BaseMovieFilesLoader


class FakeMovieFilesLoader(BaseMovieFilesLoader):
    def __init__(self, transform_results: str, *args, **kwargs) -> None:
        super().__init__(transform_results, *args, **kwargs)

    def load_movies_files(self, *args, **kwargs):
        # LoggingMixin().log.info(f"{self.transform_results} files loaded")
        return

    def update_movies(self, *args, **kwargs):
        # LoggingMixin().log.info(f"{self.transform_results} movies updated")
        return
