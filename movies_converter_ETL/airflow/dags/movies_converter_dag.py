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

    @task()
    def extract():
        """
        Загрузка данных для конвертации
        """
        from movies_converter_src.extract.BaseMovieFilesExtractor import BaseMovieFilesExtractor

        movies_extactor = BaseMovieFilesExtractor()
        extracted_data = movies_extactor.extract_movies()
        return None

    @task()
    def transform(extracted_movies):
        """
        Конвертация фильмов
        """
        from movies_converter_src.transform.BaseMovieFilesTransformer import BaseMovieFilesTransformer

        movies_transformer = BaseMovieFilesTransformer()
        transform_result = movies_transformer.transform_movies(extracted_movies)
        return transform_result

    @task()
    def load(transform_result):
        """
        Загрузка файлов и сохранение данных
        """
        from movies_converter_src.load.BaseMovieFilesLoader import BaseMovieFilesLoader

        movies_loader = BaseMovieFilesLoader()
        movies_loader.update_movies(transform_result)
        movies_loader.load_movies_files(transform_result)
        return

    extracted_movies = extract()
    if extracted_movies:
        transform_result = transform(extracted_movies)
        load(transform_result)


movie_converter_etl_dag = movie_converter_etl()
