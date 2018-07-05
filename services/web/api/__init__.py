import os
import sys
from flask import Flask, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
# from consumer import station_consumer

#Continuously listen to the connection and print messages as recieved
app = Flask(__name__)

# set config
app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

print(app.config, file=sys.stderr)

@app.route('/api/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@app.route('/')
def index():
    return "hello!"
