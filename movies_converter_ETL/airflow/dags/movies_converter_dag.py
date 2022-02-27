from webbrowser import get

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.utils.log.logging_mixin import LoggingMixin
from movies_converter_src.core.config.etl import get_config


@dag(
    schedule_interval=get_config().schedule_interval,
    start_date=days_ago(1),
    catchup=False,
    tags=["Дипломный проект ETL на стероидах"],
)
def movie_converter_etl():
    """
    Направленный ассинхронный граф для конвертации фильмов онлайн кинотеатра
    """

    @task()
    def extract() -> str:
        """
        Загрузка данных для конвертации.
        На выходе str(JSON), т.к. используется XCOM интерфейс Airflow
        """
        from movies_converter_src.extract.BaseMovieFilesExtractor import \
            BaseMovieFilesExtractor
        from movies_converter_src.models.film import Films

        movies_extactor: BaseMovieFilesExtractor = None
        if get_config().prod_mode:
            from movies_converter_src.extract.DBMovieFilesExtractor import \
                DBMovieFilesExtractor

            Extractor = DBMovieFilesExtractor
        else:
            from movies_converter_src.extract.FakeMovieFilesExtractor import \
                FakeMovieFilesExtractor

            Extractor = FakeMovieFilesExtractor
        movies_extactor = Extractor()
        extracted_movies: Films = movies_extactor.extract_movies()
        LoggingMixin().log.info(
            f"Extracted {len(extracted_movies.films)} films for convertation"
        )

        return extracted_movies.json()

    @task()
    def transform(extracted_movies) -> str:
        """
        Конвертация фильмов
        """
        from movies_converter_src.models.film import TransformResults
        from movies_converter_src.transform.BaseMovieFilesTransformer import \
            BaseMovieFilesTransformer

        movie_converter: BaseMovieFilesTransformer = None
        if get_config().prod_mode:
            from movies_converter_src.transform.ApiMovieFilesTransformer import \
                ApiMovieFilesTransformer

            Transformer = ApiMovieFilesTransformer
        else:
            from movies_converter_src.transform.FakeMovieFilesTransformer import \
                FakeMovieFilesTransformer

            Transformer = FakeMovieFilesTransformer
        movie_converter = Transformer(extracted_movies=extracted_movies)
        transform_results: TransformResults = movie_converter.transform_movies()
        files_successed_count: int = 0
        convert_errors: int = 0
        total_files: int = 0
        for film in transform_results.results:
            total_files += len(film.film_files)

            files_successed_count += len(
                [file for file in film.film_files if file.succeded]
            )
            convert_errors += len(
                [file for file in film.film_files if not file.succeded]
            )

        LoggingMixin().log.info(
            f"Converted {total_files} files for {len(transform_results.results)} films"
        )
        LoggingMixin().log.info(f"Succesed {files_successed_count}")
        LoggingMixin().log.info(f"Errors {convert_errors}")

        return transform_results.json()

    @task()
    def load(transform_result):
        """
        Загрузка файлов и сохранение данных
        """
        from movies_converter_src.load.BaseMovieFilesLoader import \
            BaseMovieFilesLoader

        movie_files_loader: BaseMovieFilesLoader = None
        if get_config().prod_mode:
            from movies_converter_src.load.CDNMovieFilesLoader import \
                CDNMovieFilesLoader

            Loader = CDNMovieFilesLoader
        else:
            from movies_converter_src.load.FakeMovieFilesLoader import \
                FakeMovieFilesLoader

            Loader = FakeMovieFilesLoader
        movie_files_loader = Loader(transform_result)
        movie_files_loader.update_movies(transform_result)
        movie_files_loader.load_movies_files(transform_result)

    extracted_movies = extract()
    transform_results = transform(extracted_movies)
    load(transform_results)


movie_converter_etl_dag = movie_converter_etl()
