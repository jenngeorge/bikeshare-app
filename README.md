## Current Status:
- goal: adding Flask & Postgres to Docker, set up database
  - flask is the api
  - postgres holds all the station data in 2 tables: stations and station_changes
- currently in the code:
  - working through tutorial. status = completed docker-compose -f docker-compose-dev.yml up -d
  - immediate next step: add restful routes


## Resources Used:
- [docker tutorial](https://docs.docker.com/get-started/part4/#set-up-your-swarm)
- [Confluent + Docker tutorial](https://docs.confluent.io/current/installation/docker/docs/quickstart.html)
- [defining an avro schema](https://avro.apache.org/docs/1.8.2/gettingstartedpython.html)
- [Processing streamining.io data code example](https://github.com/streamdataio/streamdataio-python/blob/master/client.py)
- [Citibike "General Bikeshare Feed Specification" (GBFS) for avro schema](https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_statusjson)
- [Docker image and guide for spark, dockerfile and scripts for spark application](https://github.com/mjhea0/flask-spark-docker)
- [flask/ postgres docker tutorial](https://testdriven.io/part-one-postgres-setup)

Helpful Docker commands:
  - `docker-compose up`, `docker-compose down`
  - `docker-compose ps`: prints status of services
  - `docker-compose logs`
  - `docker system prune -a` use this or run out of storage
  - `docker-compose run <service-name> bash`
    - bash depends on the container (bash has to exist). some just have bin/sh
    - from within the container, can run commands
  - `docker-compose exec <service-name> bash`
    - get into an already running service
  - if there isn't permission to run something, add `chmod`
    - `chmod +x services/users/entrypoint.sh`

Helpful database commands:
- recreate the dev database: `docker-compose -f docker-compose.yml \
  run web python manage.py recreate_db`
- get into psql: `docker exec -ti $(docker ps -aqf "name=bikeshare-db") psql -U postgres`
- run flask tests `docker-compose -f docker-compose.yml run web python manage.py test`

Helpful flask:
- Use TDD when adding flask routes https://testdriven.io/part-one-restful-routes
- Postman is nice when working on APIs https://www.getpostman.com/

Tips from friends / the internet:
- AWS
    - look at elastic beanstalk or elastic containers
    - it will take patience
    - look into circleci
    - S3 is for static assets
    - use RDS for db

- might want a docker-compose.prod
    - because there could be a different dev database
    - use env variables in docker-compose
