# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Ensure entrypoint script is executable
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000

# Default to development runserver (override to production command in deployment)
CMD ["python","manage.py","runserver","0.0.0.0:8000"]
