FROM python:3.7-buster

RUN mkdir /app
WORKDIR /app

ADD . /app/

RUN python -m pip install -r requirements.txt

RUN cd w2v_service \
    && python manage.py makemigrations \
    && python manage.py migrate

EXPOSE 8000