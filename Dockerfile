# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8260

ENV FLASK_APP=App.py

CMD gunicorn --worker-class eventlet -w 1 App:app --bind=localhost:8260