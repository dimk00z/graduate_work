# ETL pipeline `movies_converter_ETL`

## Описание

Реализован ETL pipeline на базе Airflow

### Endpoints

`http://{ip-address}:8080/home` - веб-интерфейс airflow, user:bitnami


### Запуск

Запуск :

```bash
docker-compose up
```

`http://{ip-address}:8080/home` - веб-интерфейс airflow, user:bitnami


### Описание работы

Используется TaskFlow API Aiflow
В [DAG](dags/movies_converter_dag.py) реализованы следующие таски:

1. `Load` - загрузка информации о файлах фильном для конвертации

2. `Transform` - конвертация фильмов по заданным параметрам

3. `Exctact` - выгрузка в CDN и обновление БД

Операторы и SQL запросы находятся в соответствующих дирикториях.

### Переменные среды

```
PROD_MODE=True
SCHEDULE_INTERVAL=00 12 * * *
RESOLUTIONS=2160, 1440, 1080, 720, 480, 360, 240, 120

CONVERT_API_HOST=http://api:8001
CODEC_NAME(optional)
DISPLAY_ASPECT_RATIO(optional)
FPS(optional)

POSTGRES_DB=bitnami_airflow
POSTGRES_HOST=postgresql
POSTGRES_PORT=5432
POSTGRES_USER=bn_airflow
POSTGRES_PASSWORD=bitnami1
EXTRACT_QUERY_LOCATION=sql/extract.sql
LOAD_QUERY_LOCATION=sql/load.sql

```
