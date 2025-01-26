FROM python:3.12-slim

#FROM python:3
#
#WORKDIR /app
#
#COPY ./requirements.txt .
#
#RUN pip install -r requirements.txt
#
#COPY . .

RUN pip install --no-cache-dir poetry


WORKDIR /app


COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root


COPY . .