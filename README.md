docker tutorial: https://docs.docker.com/get-started/part4/#set-up-your-swarm

updating the etc/hosts file for kafka: https://github.com/simplesteph/kafka-stack-docker-compose
- how to edit hosts file on a mac: https://www.imore.com/how-edit-your-macs-hosts-file-and-why-you-would-want


Confluent + Docker tutorial: https://docs.confluent.io/current/installation/docker/docs/quickstart.html
- helpful commands:
  - `docker-compose up`, `docker-compose down`
  - `docker-compose ps`: prints status of services
  - `docker-compose logs`
  - `docker system prune -a` use this or run out of storage
  - `docker-compose run <service-name> bash`
    - bash depends on the container (bash has to exist). some just have bin/sh
    - from within the container, can run commands
  - `docker-compose exec <service-name> bash`
    - get into an already running service


Citibike "General Bikeshare Feed Specification" (GBFS) for avro schema
- https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_statusjson


defining an avro schema:
https://avro.apache.org/docs/1.8.2/gettingstartedpython.html

Processing streamining.io data
- https://github.com/streamdataio/streamdataio-python/blob/master/client.py

Docker image and guide for spark, dockerfile and scripts for spark application - https://github.com/mjhea0/flask-spark-docker


flask/ postgres docker tutorial:
- https://testdriven.io/part-one-postgres-setup

AWS
- look at elastic beanstalk or elastic containers
- it will take patience
- look into circleci
- S3 is for static assets
- use RDS for db

might want a docker-compose.prod
  - because there could be a different dev database
  - use env variables in docker-compose

initializing a database
