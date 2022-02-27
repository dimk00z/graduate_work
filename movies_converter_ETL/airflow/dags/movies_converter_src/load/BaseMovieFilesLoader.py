from abc import ABC, abstractmethod

from airflow.utils.log.logging_mixin import LoggingMixin
from movies_converter_src.models.film import TransformResults


class BaseMovieFilesLoader(ABC):
    def __init__(self, transform_results: str, *args, **kwargs) -> None:
        LoggingMixin().log.info("Loader started")

        self.transform_results: TransformResults = TransformResults.parse_raw(transform_results)
        LoggingMixin().log.info(transform_results)

    @abstractmethod
    def load_movies_files(self, *args, **kwargs):
        raise NotImplementedError("func load_movies_files should have been implemented")

    @abstractmethod
    def update_movies(self, *args, **kwargs):
        raise NotImplementedError("func update_movies should have been implemented")
