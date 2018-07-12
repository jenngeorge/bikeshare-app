from flask import Blueprint, jsonify

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
