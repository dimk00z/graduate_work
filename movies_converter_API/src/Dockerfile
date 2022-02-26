FROM python:3.9.7-slim-buster

EXPOSE 8001

RUN apt-get -y update && apt-get install -y ffmpeg

COPY ./requirements.txt /
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY api /app
WORKDIR /app

CMD gunicorn \
    -k uvicorn.workers.UvicornWorker \
    -b 0.0.0.0:8001 \
    --log-level debug \
    main:app