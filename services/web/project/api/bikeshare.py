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
    """Add a station"""
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
    land_mark = post_data.get('land_mark')
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
                                   status_value=status_value, status_key=status_key, land_mark=land_mark,
                                   available_bikes=available_bikes, st_address_1=st_address_1,
                                   st_address_2=st_address_2, city=city, postal_code=postal_code,
                                   location=location, altitude=altitude, test_station=test_station,
                                   last_communication_time=last_communication_time))

            # add station history
            db.session.add(StationHistory(station_id=id, station_name=station_name, available_docks=available_docks,
                                   total_docks=total_docks, latitude=latitude, longitude=longitude,
                                   status_value=status_value, status_key=status_key, land_mark=land_mark,
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
    """Update single station details"""
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    put_data = request.get_json()
    print('IN bikeshare update~~~~~data', 'station id:', station_id, 'data', put_data)
    if not put_data:
        return jsonify(response_object), 400

    if not station_id:
        response_object['message'] = 'Invalid payload: Must include a station id'
        return jsonify(response_object), 400

    try:
        station = Station.query.filter_by(id=int(station_id)).first()
        data = request.get_json() or {}
        if not station:
            response_object['message'] = 'Station id does not exist'
            return jsonify(response_object), 404
        else:
            station.from_dict(data)

            # update this to reflect the correct data from object
            db.session.add(StationHistory(station_id=station.id, station_name=station.station_name, available_docks=station.available_docks,
                                   total_docks=station.total_docks, latitude=station.latitude, longitude=station.longitude,
                                   status_value=station.status_value, status_key=station.status_key, land_mark=station.land_mark,
                                   available_bikes=station.available_bikes, st_address_1=station.st_address_1,
                                   st_address_2=station.st_address_2, city=station.city, postal_code=station.postal_code,
                                   location=station.location, altitude=station.altitude, test_station=station.test_station,
                                   last_communication_time=station.last_communication_time))

            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'station {station_id} was updated!'
            return jsonify(response_object), 200
    except ValueError:
        response_object['message'] = 'Value error'
        return jsonify(response_object), 404

@bikeshare_blueprint.route('/stations/<station_id>', methods=['GET'])
def get_single_station(station_id):
    """Get single station details"""
    response_object = {
        'status': 'fail',
        'message': 'Station does not exist'
    }
    try:
        station = Station.query.filter_by(id=int(station_id)).first()
        if not station:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': station.id,
                    'station_name': station.station_name,
                    'available_docks': station.available_docks,
                    'total_docks': station.total_docks,
                    'latitude': station.latitude,
                    'longitude': station.longitude,
                    'status_value': station.status_value,
                    'land_mark': station.land_mark,
                    'status_key': station.status_key,
                    'available_bikes': station.available_bikes,
                    'st_address_1': station.st_address_1,
                    'st_address_2': station.st_address_2,
                    'city': station.city,
                    'postal_code': station.postal_code,
                    'location': station.location,
                    'altitude': station.altitude,
                    'test_station': station.test_station,
                    'last_communication_time': station.last_communication_time
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404

@bikeshare_blueprint.route('/stations/<station_id>', methods=['DELETE'])
def delete_station(station_id):
    """Delete single station"""
    response_object = {
        'status': 'fail',
        'message': 'Station does not exist'
    }
    if not station_id:
        response_object['message'] = 'Invalid request: Must include a station id'
        return jsonify(response_object), 400
    try:
        station = Station.query.filter_by(id=int(station_id)).first()
        if station:
            db.session.delete(station)
            # delete corresponding entries in station history
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'station {station_id} was deleted!'
            return jsonify(response_object), 200
        else:
            return jsonify(response_object), 404
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object['message'] = f'Error: {e}'
        return jsonify(response_object), 404

# post to station histories
@bikeshare_blueprint.route('/station_histories', methods=['POST'])
def add_station_history():
    """Add to station histories"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }

    if not post_data:
        return jsonify(response_object), 400

    station_id = post_data.get('station_id')
    station_name = post_data.get('station_name')
    available_docks = post_data.get('available_docks')
    total_docks = post_data.get('total_docks')
    latitude = post_data.get('latitude')
    longitude = post_data.get('longitude')
    status_value = post_data.get('status_value')
    status_key = post_data.get('status_key')
    land_mark = post_data.get('land_mark')
    available_bikes = post_data.get('available_bikes')
    st_address_1 = post_data.get('st_address_1')
    st_address_2 = post_data.get('st_address_2')
    city = post_data.get('city')
    postal_code = post_data.get('postal_code')
    location = post_data.get('location')
    altitude = post_data.get('altitude')
    test_station = post_data.get('test_station')
    last_communication_time = post_data.get('last_communication_time')

    if not station_id:
        response_object['message'] = 'Invalid payload: Must include a station id'
        return jsonify(response_object), 400
    try:
        db.session.add(StationHistory(station_id=station_id, station_name=station_name, available_docks=available_docks,
                               total_docks=total_docks, latitude=latitude, longitude=longitude,
                               status_value=status_value, status_key=status_key, land_mark=land_mark,
                               available_bikes=available_bikes, st_address_1=st_address_1,
                               st_address_2=st_address_2, city=city, postal_code=postal_code,
                               location=location, altitude=altitude, test_station=test_station,
                               last_communication_time=last_communication_time))
        db.session.commit()
        response_object['status'] = 'success'
        response_object['message'] = f'station {station_id} new history was added!'
        return jsonify(response_object), 201
    except exc.IntegrityError as e:
        response['message'] = e
        db.session.rollback()
        return jsonify(response_object), 400
