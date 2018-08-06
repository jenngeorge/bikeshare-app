#try:
import requests
import json
import time
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

def format_data(data):
    formatted_dict = {k:v for (k,v) in data.items() if v != None}
    print('formatted dict', formatted_dict)
    return formatted_dict
    

def make_request(station_id, data):
    print('in request switch', data)

    # op create
    if data['op'] == 'create':
        print('post')
        try:
            req = requests.request('POST', 'http://web:4000/stations', data = data)
            req.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Message POST request error: {}".format(e))

    elif data['op'] == 'update':
        print('update')
        data = format_data(data)
        try:
            req = requests.request('PUT', 'http://web:4000/stations', data = data)
            req.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Message PUT request error: {}".format(e))

    elif data['op'] == 'delete':
        print('delete')
        try:
            req = requests.request('DELETE', 'http://web:4000/stations/{}'.format(station_id))
            req.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Message DELETE request error: {}".format(e))


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
        print('~~~~~DIDD ITTTT', "key:", msg.key(), "value:", msg.value())
        make_request(msg.key[station_id], msg.value)
    c.close()

if __name__ == '__main__':
    consume()
