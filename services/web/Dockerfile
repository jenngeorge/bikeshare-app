# Use an official Python runtime as a parent image
FROM python:3.6-slim-jessie

# Set the working directory to /bikeshare_app
WORKDIR /bikeshare_app

# Copy the current directory contents into the container at /bikeshare_app
ADD . /bikeshare_app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run bikeshare_app.py when the container launches
CMD ["python", "manage.py"]
