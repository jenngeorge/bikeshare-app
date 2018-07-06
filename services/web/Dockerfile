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

# Run bikeshare_app.py when the container launches
CMD python manage.py run -h 0.0.0.0 -p 4000
