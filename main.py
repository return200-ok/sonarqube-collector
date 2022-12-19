import logging
import os
import sys
from datetime import datetime

import rfc3339
from branch_collector import branch_crawler
from dotenv import load_dotenv
from event_collector import event_crawler
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS
from metric_collector import metric_crawler
from rule_collector import rule_crawler

'''
  Config logging handler
'''
def get_date_string(date_object):
  return rfc3339.rfc3339(date_object)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()
fileName = get_date_string(datetime.now())+'_sonarqube_collecter'
logPath = 'logs'
fileHandler = logging.FileHandler("{0}/{1}.log".format(logPath, fileName))
fileHandler.setFormatter(logFormatter)

'''
  Avoid duplicated logs
'''
if (rootLogger.hasHandlers()):
    rootLogger.handlers.clear()
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
logging.getLogger().setLevel(logging.DEBUG)

class SonarqubeInstance:
    """Initialize defaults."""
    def __init__(self, sonarqube_server, sonarqube_token):
        self.sonarqube_server = sonarqube_server
        self.sonarqube_token = sonarqube_token
class InfluxClient:
    
    '''
    Initialize defaults.
    Usage: client = InfluxClient(influx_server, influx_token, org_name, bucket_name)
    Example:
        client = InfluxClient("http://localhost:8086", "KlXfBqa0uSGs0icfE", "org", "bucket")
        client.write_data(data)
    '''
    def __init__(self, url, token, org, bucket): 
        self._org = org
        self._bucket = bucket
        self._client = InfluxDBClient(url=url, token=token, org=org)
    def write_data(self, data, write_option=ASYNCHRONOUS):
        write_api = self._client.write_api(write_option)
        write_api.write(self._bucket, self._org, data, write_precision='s')

if __name__ == '__main__':
    # Load env
    load_dotenv()

    sonarqube_token = os.getenv('SONARQUBE_TOKEN')
    influx_token = os.getenv('INFLUX_TOKEN')
    influx_server = os.getenv('INFLUX_DB')
    org_name = os.getenv('ORG_NAME')
    bucket_name = os.getenv('BUCKET_NAME')
    sonarqube_server = os.getenv('SONARQUBE_URL')

    write_client = InfluxClient(influx_server, influx_token, org_name, bucket_name)

    branch_crawler(sonarqube_server, sonarqube_token, write_client)
    metric_crawler(sonarqube_server, sonarqube_token, write_client)
    event_crawler(sonarqube_server, sonarqube_token, write_client)
    rule_crawler(sonarqube_server, sonarqube_token, write_client)


