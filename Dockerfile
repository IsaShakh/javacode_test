FROM python:3.12.3-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && apt-get clean

WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev
COPY . .
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=core.settings
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
