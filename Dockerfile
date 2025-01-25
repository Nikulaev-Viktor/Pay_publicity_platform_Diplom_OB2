FROM python:3.12-slim

RUN pip install --no-cache-dir poetry


WORKDIR /app


COPY pyproject.toml poetry.lock .

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main


COPY . .

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]