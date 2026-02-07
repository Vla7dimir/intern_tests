# Places Remember — dev/prototype image (runserver, not for production).
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY my_django_project/ ./my_django_project/
COPY .env.example .env

WORKDIR /app/my_django_project
ENV DJANGO_SETTINGS_MODULE=my_django_project.settings
# Migrate on start so volume-mounted code and DB stay in sync.
EXPOSE 8000
CMD ["sh", "-c", "python manage.py migrate --noinput && exec python manage.py runserver 0.0.0.0:8000"]
