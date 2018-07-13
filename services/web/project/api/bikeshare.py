from flask import Blueprint, jsonify, request
from project import db
from project.api.models import Station, StationHistory
from sqlalchemy import exc

# create a new blueprint and bind ping_pong method to it
bikeshare_blueprint = Blueprint('bikeshare', __name__)

@bikeshare_blueprint.route('/', methods=['GET'])
def index():
    return "hello!"

@bikeshare_blueprint.route('/bikeshare/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@bikeshare_blueprint.route('/stations', methods=['POST'])
def add_station():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }

    if not post_data:
        return jsonify(response_object), 400

    id = post_data.get('id')
    station_name = post_data.get('station_name')
    available_docks = post_data.get('available_docks')
    total_docks = post_data.get('total_docks')
    latitude = post_data.get('latitude')
    longitude = post_data.get('longitude')
    status_value = post_data.get('status_value')
    status_key = post_data.get('status_key')
    available_bikes = post_data.get('available_bikes')
    st_address_1 = post_data.get('st_address_1')
    st_address_2 = post_data.get('st_address_2')
    city = post_data.get('city')
    postal_code = post_data.get('postal_code')
    location = post_data.get('location')
    altitude = post_data.get('altitude')
    test_station = post_data.get('test_station')
    last_communication_time = post_data.get('last_communication_time')

    if not id:
        response_object['message'] = 'Invalid payload: Must include a station id'
        return jsonify(response_object), 400
    try:
        station = Station.query.filter_by(id=id).first()
        if not station:
            db.session.add(Station(id=id, station_name=station_name, available_docks=available_docks,
                                   total_docks=total_docks, latitude=latitude, longitude=longitude,
                                   status_value=status_value, status_key=status_key,
                                   available_bikes=available_bikes, st_address_1=st_address_1,
                                   st_address_2=st_address_2, city=city, postal_code=postal_code,
                                   location=location, altitude=altitude, test_station=test_station,
                                   last_communication_time=last_communication_time))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'station {id} was added!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That station id already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400

@bikeshare_blueprint.route('/stations/<station_id>', methods=['PUT'])
def update_station(station_id):
    response_object = {
        'status': 'fail',
        'message': 'Station id does not exist'
    }
    try:
        station = Station.query.filter_by(id=int(station_id)).first()
        data = request.get_json() or {}
        if not station:
            return jsonify(response_object), 404
        else:
            station.from_dict(data)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'station {station_id} was updated!'
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404