from webbrowser import get

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

from movies_converter_src.core.config.etl import get_config
from movies_converter_src.core.logger.logger import logger


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

        logger.info("Exctractor started")
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
        logger.info("Extracted %d films for convertation", len(extracted_movies.films))
        logger.info("Exctractor finished")

        return extracted_movies.json()

    @task()
    def transform(extracted_movies) -> str:
        """
        Конвертация фильмов
        """
        from movies_converter_src.models.film import TransformResults
        from movies_converter_src.transform.BaseMovieFilesTransformer import \
            BaseMovieFilesTransformer

        logger.info("Transformer started")

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

            files_successed_count += len([file for file in film.film_files if file.succeded])
            convert_errors += len([file for file in film.film_files if not file.succeded])

        logger.info(
            "Converted %d files for %d films",
            total_files,
            len(transform_results.results),
        )
        logger.info("Succesed %d", files_successed_count)
        logger.info("Errors %d", convert_errors)
        logger.info("Transformer finished")

        return transform_results.json()

    @task()
    def load(transform_result):
        """
        Загрузка файлов и сохранение данных
        """
        from movies_converter_src.load.BaseMovieFilesLoader import \
            BaseMovieFilesLoader
        from movies_converter_src.models.film import LoaderResults

        logger.info("Loader started")

        movie_files_loader: BaseMovieFilesLoader = None
        if get_config().prod_mode:
            from movies_converter_src.load.CDNMovieFilesLoader import \
                CDNMovieFilesLoader

            Loader = CDNMovieFilesLoader
        else:
            from movies_converter_src.load.FakeMovieFilesLoader import \
                FakeMovieFilesLoader

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
        loader_results: LoaderResults = movie_files_loader.load(transform_result)
        logger.info("%d movies updated", loader_results.updated_movies)
        logger.info("Loader finished")

    extracted_movies = extract()
    transform_results = transform(extracted_movies)
    load(transform_results)


movie_converter_etl_dag = movie_converter_etl()
