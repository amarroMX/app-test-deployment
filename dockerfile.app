FROM python:3.7-alpine:latest

WORKDIR /app

COPY ./django/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py runserver
