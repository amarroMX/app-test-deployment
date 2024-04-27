FROM python:3.11.4-alpine

WORKDIR /app

# This prevents Python from writing out pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# This keeps Python from buffering stdin/stdout
ENV PYTHONUNBUFFERED 1

COPY /afronectar/ /app/

COPY ./afronectar/requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

RUN python manage.py makemigrations \
    && python manage.py migrate 
