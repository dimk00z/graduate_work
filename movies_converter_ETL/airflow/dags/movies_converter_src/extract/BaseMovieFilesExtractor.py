from abc import ABC, abstractmethod


class BaseMovieFilesExtractor(ABC):
    @abstractmethod
    def extract_movies(self, *args, **kwargs):
        raise NotImplementedError("func extract_movies should have been implemented")
