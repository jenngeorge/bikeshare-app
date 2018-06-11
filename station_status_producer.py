from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import requests

import station_status 

value_schema_str = station_status

key_schema_str = """
{
   "namespace": "bikeshare_app",
   "name": "key",
   "type": "record",
   "fields" : [
     {"name" : "station_id", "type" : "int"}
   ]
}
"""

value_schema = avro.loads(value_schema_str)
key_schema = avro.loads(key_schema_str)
# value = {"name": "Value"}
# key = {"name": "Key"}

avroProducer = AvroProducer({
    'bootstrap.servers': 'localhost:9092',
    'schema.registry.url': 'http://localhost:8081'
    }, default_key_schema=key_schema, default_value_schema=value_schema)

    
response_data = requests.get('https://proxy.streamdata.io/https://feeds.citibikenyc.com/stations/stations.json', stream=True)

# citidata streaming api
for chunk in response_data.iter_content():
    
    avroProducer.produce(topic='station_status', value=chunk, key=key)
    avroProducer.flush()
