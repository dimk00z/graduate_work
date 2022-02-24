from abc import ABC, abstractmethod
from typing import List


class BaseMovieFilesExtractor(ABC):
    @abstractmethod
    def extract_movies(self, *args, **kwargs) -> List[str]:
        raise NotImplementedError("func extract_movies should have been implemented")
