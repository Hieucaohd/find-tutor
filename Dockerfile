# syntax=docker/dockerfile:1
FROM ubuntu:20.04
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/

# # Install postgres client
# RUN apk add --update --no-cache postgresql-client

# # Install individual dependencies
# # so that we could avoid installing extra packages to the container
# RUN apk add --update --no-cache \
# 	gcc libc-dev linux-headers postgresql-dev

RUN apt-get update

RUN apt-get install -y python3-pip

RUN pip3 install -r requirements.txt

# Remove dependencies

COPY . /code/
