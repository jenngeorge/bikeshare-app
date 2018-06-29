#try:
import requests
import json
import time
from pyspark import SparkContext, SparkConf
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from avro_schema import station_schema


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

avroProducer = AvroProducer({
    'bootstrap.servers': 'kafka-1:19092, kafka-2:29092',
    'schema.registry.url': 'http://schema-registry:8081',
    }, default_key_schema=key_schema, default_value_schema=value_schema)

def poll():
    # url = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"
    url = "https://feeds.citibikenyc.com/stations/stations.json"

    conf = SparkConf().setAppName('CitibikeDataIngestion')
    sc = SparkContext(conf=conf)
    print('DIDDDD SPARK')
    last_rdd = None

    while True:
        response = requests.get(url)
        response = response.json()['stationBeanList']
        #Create key, value pair rdd with station id as key and all other
        #fields as a value list.
        curr_rdd = sc.parallelize(response).map(lambda x: (list(x.items())[0],
                            list(x.items())[1:]))
        #First request, all stations need to be created
        if last_rdd == None:
            #Create rdd to send to kafka. Append to values list a new field
            #specifying the operation
            rdd_stream = curr_rdd.map(lambda x: (x[0],x[1] + [('op','create')]))
        #Second request forward, updates to existing stations
        else:
            #Subtract by key last rdd from curr rdd to get stations to delete
            rdd_deletes = last_rdd.subtractByKey(curr_rdd)\
                                .map(lambda x: (x[0],x[1] + [('op','delete')]))
            #Subtract by key curr rdd from last rdd to get new stations to create
            rdd_creates = curr_rdd.subtractByKey(last_rdd)\
                                .map(lambda x: (x[0],x[1] + [('op','create')]))
            def flat(x): return x
            #Subtract last rdd from curr id to get updates to existing stations
            rdd_updates = curr_rdd.flatMapValues(flat)\
                                .subtract(last_rdd.flatMapValues(flat))\
                                    .groupByKey()\
                                        .mapValues(list)\
                                            .map(lambda x: (x[0],x[1]
                                                + [('op','update')]))
            #Combine deletes, creates and updates into single stream for kafka
            rdd_stream = rdd_updates.union(rdd_creates)\
                            .union(rdd_deletes)

        for update in rdd_stream.collect():
            # print(update)
            key_dict = dict([update[0]])
            value_dict = dict(update[1])
            avroProducer.produce(topic='station_status', value=value_dict, key=key_dict)
        last_rdd = curr_rdd
        time.sleep(5)

        avroProducer.flush()

if __name__ == '__main__':
    poll()
