from airflow.decorators import dag, task
from airflow.utils.dates import days_ago


@dag(
    schedule_interval="00 12 * * *",
    start_date=days_ago(1),
    catchup=False,
    tags=["Дипломный проект ETL на стероидах"],
)
def movie_converter_etl():
    """
    Направленный ассинхронный граф для конвертации фильмов онлайн кинотеатра
    """
    from typing import List

    from movies_converter_src.models.film import Film

    @task()
    def extract() -> List[str]:
        """
        Загрузка данных для конвертации.
        На выходе JSON, т.к. используется XCOM интерфейс Airflow
        """
        from movies_converter_src.extract.BaseMovieFilesExtractor import BaseMovieFilesExtractor
        from movies_converter_src.extract.FakeMovieFilesExtractor import FakeMovieFilesExtractor

        movies_extactor: BaseMovieFilesExtractor = FakeMovieFilesExtractor()
        return movies_extactor.extract_movies()

    @task()
    def transform(extracted_movies):
        """
        Конвертация фильмов
        """
        from movies_converter_src.transform.BaseMovieFilesTransformer import BaseMovieFilesTransformer
        from movies_converter_src.transform.FakeMovieFilesTransformer import FakeMovieFilesTransformer

        movie_converter: BaseMovieFilesTransformer = FakeMovieFilesTransformer(
            extracted_movies=extracted_movies
        )

        transform_result = movie_converter.transform_movies()
        return transform_result

    @task()
    def load(transform_result):
        """
        Загрузка файлов и сохранение данных
        """
        from movies_converter_src.load.BaseMovieFilesLoader import BaseMovieFilesLoader

        # movies_loader = BaseMovieFilesLoader()
        # movies_loader.update_movies(transform_result)
        # movies_loader.load_movies_files(transform_result)
        return

    extracted_movies = extract()
    # if extracted_movies:
    transform_result = transform(extracted_movies)
    load(transform_result)


movie_converter_etl_dag = movie_converter_etl()
