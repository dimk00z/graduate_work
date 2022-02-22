from abc import ABC, abstractmethod


class BaseMovieFilesTransformer(ABC):
    @abstractmethod
    def transform_movies(self, *args, **kwargs):
        raise NotImplementedError("func transform_movies should have been implemented")
