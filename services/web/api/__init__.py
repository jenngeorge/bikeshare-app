import os
import datetime
# import sys
from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

# instantiate the db
db = SQLAlchemy(app)


# TODO: read about model inheritance http://docs.sqlalchemy.org/en/latest/orm/inheritance.html
# model: station information
class Stations(db.Model):
    __tablename__ = "stations"
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # here id will be the station_id, so no auto-incrememnt
    id = db.Column(db.Integer(), primary_key=True, nullable=False)
    station_name = db.Column(db.String(128), nullable=True)
    available_docks = db.Column(db.Integer(), nullable=True)
    total_docks = db.Column(db.Integer(), nullable=True)
    latitude = db.Column(db.Decimal(), nullable=True)
    longitude = db.Column(db.Decimal(), nullable=True)
    status_value = db.Column(db.String(128), nullable=True)
    status_key = db.Column(db.Integer(), nullable=True)
    available_bikes = db.Column(db.Integer(), nullable=True)
    st_address_1 = db.Column(db.String(128), nullable=True)
    st_address_2 = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=True)
    postal_code = db.Column(db.String(128), nullable=True)
    location = db.Column(db.String(128), nullable=True)
    altitude = db.Column(db.String(128), nullable=True)
    test_station = db.Column(db.Boolean(), nullable=True)
    last_communication_time = db.Column(db.String(128), nullable=True)

    def __init__(self, id, station_name, available_docks, total_docks, latitude,
                 longitude, status_value, status_key, available_bikes, st_address_1,
                 st_address_2, city, postal_code, location, altitude, test_station,
                 last_communication_time):
        self.id = id
        self.station_name = station_name
        self.available_docks = available_docks
        self.total_docks = total_docks
        self.latitude = latitude
        self.longitude = longitude
        self.status_value = status_value
        self.status_key = status_key
        self.available_bikes = available_bikes
        self.st_address_1 = st_address_1
        self.st_address_2 = st_address_2
        self.city = city
        self.postal_code = postal_code
        self.location = location
        self.altitude = altitude
        self.test_station = test_station
        self.last_communication_time = last_communication_time

# model
# logs changes to a station (excluding last comm time)
class StationChanges(Stations):
    __tablename__ = "station_changes"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    station_id = db.Column(db.Integer(), nullable=False)
    station_name = db.Column(db.String(128), nullable=True)
    available_docks = db.Column(db.Integer(), nullable=True)
    total_docks = db.Column(db.Integer(), nullable=True)
    latitude = db.Column(db.Decimal(), nullable=True)
    longitude = db.Column(db.Decimal(), nullable=True)
    status_value = db.Column(db.String(128), nullable=True)
    status_key = db.Column(db.Integer(), nullable=True)
    available_bikes = db.Column(db.Integer(), nullable=True)
    st_address_1 = db.Column(db.String(128), nullable=True)
    st_address_2 = db.Column(db.String(128), nullable=True)
    city = db.Column(db.String(128), nullable=True)
    postal_code = db.Column(db.String(128), nullable=True)
    location = db.Column(db.String(128), nullable=True)
    altitude = db.Column(db.String(128), nullable=True)
    test_station = db.Column(db.Boolean(), nullable=True)
    last_communication_time = db.Column(db.String(128), nullable=True)

    def __init__(self, id, station_name, available_docks, total_docks, latitude,
                 longitude, status_value, status_key, available_bikes, st_address_1,
                 st_address_2, city, postal_code, location, altitude, test_station,
                 last_communication_time):
        Station.__init__(self, id, station_name, available_docks, total_docks, latitude,
                     longitude, status_value, status_key, available_bikes, st_address_1,
                     st_address_2, city, postal_code, location, altitude, test_station,
                     last_communication_time)
            self.id = None
            self.station_id = id

def __init__(self, username, email):
    self.username = username
    self.email = email




@app.route('/')
def index():
    return "hello!"

@app.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })
