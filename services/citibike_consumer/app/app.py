#try:
import requests
import json
import time
import re # regex
#from pyspark import SparkContext, SparkConf
from confluent_kafka import avro, KafkaError
from confluent_kafka.avro import AvroConsumer
from avro_schema import station_schema
from confluent_kafka.avro.serializer import SerializerError
from multiprocessing import Process


value_schema_str = station_schema

key_schema_str = """
{
   "namespace": "bikeshare_app",
   "name": "key",
   "type": "record",
   "fields" : [
     {"name" : "id", "type" : "int"}
   ]
}
"""

value_schema = avro.loads(value_schema_str)
key_schema = avro.loads(key_schema_str)

def convert_camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def format_update_data(station_id, data):
    # filter out all the None's
    # format data for a post request
    formatted_data = {}
    formatted_data['station_id'] = station_id['id']
    # print('DATA', data)

    for key, value in data.items():
        if value != 'null':
            formatted_data[convert_camel_to_snake(key)] = value

    print('UPDATE DATA', json.dumps(formatted_data))
    return formatted_data

def format_post_data(station_id, data):
    # format data for a post request
    formatted_data = {}
    formatted_data['id'] = station_id['id']

    for key, value in data.items():
        formatted_data[convert_camel_to_snake(key)] = value

    print('POST DATA', json.dumps(formatted_data))
    return formatted_data


def make_request(station_id, data):
    # data is a dict with camelCase keys
    # need to change to snake_case

    # op create
    if data['op'] == 'create':
        # send create request
        # send station histories request
        print('post')
            # try:
            #     req = requests.request('POST', 'http://web:4000/stations', body)
    elif data['op'] == 'update':
        format_update_data(station_id, data)
        # send update request
        # send station histories request
        print('update')
    elif data['op'] == 'delete':
        print('delete')


def consume():
    c = AvroConsumer({
    'bootstrap.servers': 'kafka-1:19092, kafka-2:29092',
    'schema.registry.url': 'http://schema-registry:8081',
    'group.id': 'citibike_station_data',
    })

    c.subscribe(['station_status'])

    while True:
        try:
            msg = c.poll(10)

        except SerializerError as e:
            print("Message deserialization failed for {}: {}".format(msg, e))
            break

        if msg is None:
            print("~~~~MESSAGE IS NONE")
            continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print("~~A MESSAGE ERROR", msg.error())
                break

        # do something with the data
        #print('~~~~~DIDD ITTTT', "key:", msg.key(), "value:", msg.value())
        make_request(msg.key(), msg.value())
    c.close()

if __name__ == '__main__':
    consume()
