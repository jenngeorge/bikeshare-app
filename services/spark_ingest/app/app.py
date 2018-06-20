
try:
    import requests
    import json
    import time
    from pyspark import SparkContext, SparkConf
except:
    print('error importing for spark_ingest/app')


def poll():
    url = "https://gbfs.citibikenyc.com/gbfs/en/station_status.json"


    conf = SparkConf().setAppName('CitibikeDataIngestion')
    sc = SparkContext(conf=conf)
    print('DIDDDD SPARK')

    while True:
        response = requests.get(url)
        response = json.loads(response.content)
        distData = sc.parallelize(response)
        print(distData)
        time.sleep(5)
        print('NEWWWWW')


if __name__ == '__main__':
    poll()
