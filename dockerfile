FROM python:3.9-slim-buster
RUN apt-get update && apt-get install -y build-essential libpq-dev gcc
RUN apt-get install -y libxml2-dev libxslt-dev python3-dev libffi-dev musl-dev
RUN apt-get install -y libpoppler-cpp-dev
RUN apt-get install -y python-dev


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.1.13 \
    POETRY_VIRTUALENVS_CREATE=false

RUN pip install "poetry==$POETRY_VERSION"    

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \ 
    && poetry install --no-interaction --no-dev --no-ansi

COPY . ./

CMD ["uvicorn", "twijournal.main:app", "--host", "0.0.0.0", "--port", "8000"]



