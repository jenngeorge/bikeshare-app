FROM jenngeorge/bikeshare_app:spark

# Set the working directory
RUN mkdir -p /usr/src/citibike_consumer
WORKDIR /usr/src/citibike_consumer

# add requirements
COPY ./app/requirements.txt /usr/src/citibike_consumer/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# add app
COPY ./app /usr/src/citibike_consumer

# add dockerize
RUN apt-get update && apt-get install -y wget

ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz
