# Use an official Python runtime as a parent image
FROM python:3.6-slim-jessie

# Set the working directory to /bikeshare_app
RUN mkdir -p /usr/src/bikeshare_app
WORKDIR usr/src/bikeshare_app

# add requirements
COPY ./requirements.txt /usr/src/bikeshare_app/requirements.txt

# install requirements
RUN pip install -r requirements.txt

# add app
COPY . /usr/src/bikeshare_app

# add dockerize
RUN apt-get update && apt-get install -y wget

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
