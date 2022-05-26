FROM python:3.9-alpine
MAINTAINER realize-sec

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY main.py /app
COPY ../far-shore-config.yaml /app

