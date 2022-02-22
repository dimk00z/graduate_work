from abc import ABC, abstractmethod


class BaseMovieFilesLoader(ABC):
    @abstractmethod
    def load_movies_files(self, *args, **kwargs):
        raise NotImplementedError("func load_movies_files should have been implemented")

    @abstractmethod
    def update_movies(self, *args, **kwargs):
        raise NotImplementedError("func update_movies should have been implemented")
