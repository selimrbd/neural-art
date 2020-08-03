FROM python:3.7.2-stretch

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

WORKDIR /app/app

CMD ["uwsgi", "app.ini"]

