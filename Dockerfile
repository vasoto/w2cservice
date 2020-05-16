FROM python:3.7-buster

RUN mkdir /app
WORKDIR /app

ADD . /app/

RUN python -m pip install -r requirements.txt
    
RUN cd w2v_service \
    && python manage.py makemigrations \
    && python manage.py migrate

EXPOSE 8000
WORKDIR /app/w2v_service
CMD python manage.py runserver 0.0.0.0:8000
