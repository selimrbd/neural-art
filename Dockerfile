FROM python:3.7.2-stretch

WORKDIR /app
ADD requirements.txt /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . /app
WORKDIR /app/app

CMD ["uwsgi", "wsgi.ini"]
