FROM jenngeorge/bikeshare_app:spark

# Set the working directory
RUN mkdir -p /usr/src/spark_ingest
WORKDIR /usr/src/spark_ingest

# add requirements
COPY ./app/requirements.txt /usr/src/spark_ingest/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# add app
COPY ./app /usr/src/spark_ingest
