from airflow.utils.log.logging_mixin import LoggingMixin
from movies_converter_src.load.BaseMovieFilesLoader import BaseMovieFilesLoader
from movies_converter_src.models.film import Film, Films, LoaderResults


class CDNMovieFilesLoader(BaseMovieFilesLoader):
    def __init__(self, transform_results: str, *args, **kwargs) -> None:
        super().__init__(transform_results, *args, **kwargs)

    def load(self, *args, **kwargs) -> LoaderResults:
        return LoaderResults(
            loaded_files=len(self.transform_results.results),
            updated_movies=len(self.transform_results.results),
        )
        return len(self.transform_results.results)
