from abc import ABC, abstractmethod


class BaseMovieFilesLoader(ABC):
    def __init__(self, transform_result: str, *args, **kwargs) -> None:
        self.transform_result = transform_result

    @abstractmethod
    def load_movies_files(self, *args, **kwargs):
        raise NotImplementedError("func load_movies_files should have been implemented")

    @abstractmethod
    def update_movies(self, *args, **kwargs):
        raise NotImplementedError("func update_movies should have been implemented")
