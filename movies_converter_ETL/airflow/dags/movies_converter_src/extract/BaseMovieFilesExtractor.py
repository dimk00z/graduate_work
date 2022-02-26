from abc import ABC, abstractmethod

from movies_converter_src.models.film import Films


class BaseMovieFilesExtractor(ABC):
    @abstractmethod
    def extract_movies(self, *args, **kwargs) -> Films:
        raise NotImplementedError("func extract_movies should have been implemented")
