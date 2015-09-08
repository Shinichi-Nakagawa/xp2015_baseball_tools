# No Ball Django application server

FROM python:3.4.3-wheezy

MAINTAINER Shinichi Nakagawa <spirits.is.my.rader@gmail.com>

# add to application
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
RUN mkdir /app/output
ADD ./baseball /app/baseball/
ADD ./service /app/service/
ADD *.py /app/
ADD app.ini /app/
ADD config.ini /app/