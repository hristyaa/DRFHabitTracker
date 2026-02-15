FROM python:3.13.3

WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry==2.2.1

# Копируем файлы Poetry
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main

COPY . .
