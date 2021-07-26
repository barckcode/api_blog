FROM python:3.9

WORKDIR /api

COPY ./requirements.txt /api

RUN pip3 install -r requirements.txt
