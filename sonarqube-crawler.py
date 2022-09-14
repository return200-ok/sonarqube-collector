import scrapy
from influxdb import InfluxDBClient
from time import time
import pdb
import random
import json
import requests


def getData(url, token):
  session = requests.Session()
  session.auth = token, ''
  call = getattr(session, 'get')
  res = call(url)
  data = json.loads(res.content)
  return data

def parseData(component, metricKeys, token):
  url = "https://sonarqube.biplus.com.vn/api/measures/component?component="+component+"&metricKeys="+metricKeys
  return getData(url, token)


def insertData(metric, project_key, name, value):
  db = InfluxDBClient("localhost", 8086)
  db.switch_database("sonarqube_kpi")
  kpi = [{
    "measurement": metric,
    "tags": {
      "project_key": project_key,
      "name": name
    },
    "time": int(time()) * 1000000000,
    "fields": {
      "loc": str(float(value))
    }
  }]
  db.write_points(kpi)

if __name__ == '__main__':
  token = "squ_a4c1bd1d9be8613d1179234e634d7541af960f2b"
  output = getData("https://sonarqube.biplus.com.vn/api/components/search?qualifiers=TRK", token)
  metricKeys = ["ncloc", "bugs", "code_smells", "sqale_index"]
  for components in output['components']:
    for metricKey in metricKeys:
      data = parseData((components['key']), metricKey, token)
      project_key = data["component"]["key"]
      name = data["component"]["name"]
      if len(data["component"]["measures"]) == 0:
        value = 0
      else: 
        value = data["component"]["measures"][0]["value"]
      insertData(metricKey, project_key, name, value)



