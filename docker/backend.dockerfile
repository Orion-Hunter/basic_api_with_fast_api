FROM tiangolo/uvicorn-gunicorn:python3.9-slim

RUN apt-get update
RUN apt-get -y upgrade

WORKDIR  /usr/src/app
ENV PYTHONPATH /usr/src/app
ENV PYTHONHONUNBUFFERED 1 
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install -Iv poetry==1.3.1
RUN pip install --upgrade pip

RUN poetry config virtualenvs.create false

RUN poetry config experimental.new-installer false

COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install


ENV TZ America/Sao_Paulo

COPY ./ ./


RUN cat ./scripts/web-prestart.sh > /app/prestart.sh   
RUN cat ./scripts/web-start-reload.sh > /start-reload.sh
CMD ["bash", "/start-reload.sh"]