import os
from os import environ
from time import time
import json
import requests
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


sonarqube_token = os.environ.get('SONARQUBE_TOKEN')
influx_token = os.environ.get('INFLUX_TOKEN')
influx_server = os.environ.get('INFLUX_SERVER')
org_name = os.environ.get('ORG_NAME')
bucket_name = os.environ.get('BUCKET_NAME')
sonarqube_server = os.environ.get('SONARQUBE_SERVER')


def getData(url, token):
  session = requests.Session()
  session.auth = token, ''
  call = getattr(session, 'get')
  res = call(url)
  data = json.loads(res.content)
  return data

def parseData(component, metricKeys, token):
  url = sonarqube_server+"/api/measures/component?component="+component+"&metricKeys="+metricKeys
  return getData(url, token)


def insertData(metric, project_key, name, value):
  client = InfluxDBClient(url=influx_server, token=influx_token, org=org_name)

  kpi = [{
    "measurement": metric,
    "tags": {
      "project_key": project_key,
      "project_name": name,
    },
    "time": int(time()) * 1000000000,
    "fields": {
      metric: str(value)
    }
  }]
  write_api = client.write_api(write_options=SYNCHRONOUS)
  write_api.write(bucket_name, org_name, kpi)
  print ("write ", kpi," to bucket "+bucket_name)



if __name__ == '__main__':
  url = sonarqube_server+"/api/components/search?qualifiers=TRK"
  list_components = getData(url, sonarqube_token)
  metricKeys = ["ncloc", "bugs", "code_smells", "sqale_index"]
  for components in list_components['components']:
    for metricKey in metricKeys:
      data = parseData((components['key']), metricKey, sonarqube_token)
      project_key = data["component"]["key"]
      name = data["component"]["name"]
      if len(data["component"]["measures"]) == 0:
        value = "null"
      else: 
        value = data["component"]["measures"][0]["value"]
      insertData(metricKey, project_key, name, value)