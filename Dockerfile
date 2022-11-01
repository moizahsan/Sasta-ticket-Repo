# This is a simple Dockerfile to use while developing
# It's not suitable for production
#
# It allows you to run both flask and celery if you enabled it
# for flask: docker run --env-file=.flaskenv image flask run
# for celery: docker run --env-file=.flaskenv image celery worker -A myapi.celery_app:app
#
# note that celery will require a running broker and result backend
FROM python:3.6

RUN mkdir /code
WORKDIR /code

COPY requirements.txt setup.py tox.ini ./
RUN apt-get update && apt-get -y install unixodbc-dev alien
RUN wget https://ds-st-public-bucket.s3.ap-southeast-1.amazonaws.com/dremio-odbc-1.3.19.1052-1.x86_64.rpm && alien -i --scripts dremio-odbc-1.3.19.1052-1.x86_64.rpm
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install -e .

COPY dsapi dsapi/
COPY migrations migrations/

EXPOSE 5000
