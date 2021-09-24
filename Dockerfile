FROM python:3.9

COPY ./api/ /api

WORKDIR /api

RUN pip3 install -r requirements.txt

CMD [ "uvicorn", "app:app", "--reload", "--host=0.0.0.0" ]
