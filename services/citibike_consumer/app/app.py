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
    # filter out all the None's
    

def make_request(station_id, data):
    print('in request switch', data)

    # op create
    if data['op'] == 'create':
        print('post')
            # try:
            #     req = requests.request('POST', 'http://web:4000/stations', body)
    elif data['op'] == 'update':
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
        print('~~~~~DIDD ITTTT', "key:", msg.key(), "value:", msg.value())
        # make_request(msg.key, msg.value)
    c.close()

if __name__ == '__main__':
    consume()
