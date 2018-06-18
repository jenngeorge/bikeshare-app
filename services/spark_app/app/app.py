import requests
import json
import time
from pyspark import SparkContext
# from pyspark.streaming import StreamingContext
# from pyspark.streaming.kafka import KafkaUtils
#
def poll():
    url = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"

    while True:
        response = requests.get(url)
        response = json.loads(response.content)
        print(response)
        time.sleep(5)
        print('NEWWWWW')



poll()
