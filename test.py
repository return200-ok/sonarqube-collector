import scrapy
from influxdb import InfluxDBClient
from time import time
import pdb
import random
import json
import requests


url = 'https://sonarqube.biplus.com.vn/api/measures/component?component=Test&metricKeys=ncloc'
myToken = 'squ_a4c1bd1d9be8613d1179234e634d7541af960f2b'
session = requests.Session()
session.auth = myToken, ''
call = getattr(session, 'get')
res = call(url)
output = json.loads(res.content)
project_key=output["component"]["key"]
loc=output["component"]["measures"][0]["value"]
db = InfluxDBClient("localhost", 8086)
db.switch_database("sonarqube_kpi")
kpi = [{
  "measurement": "loc",
  "tags": {
    "project_key": "Test",
    "name": "authorization-service"
  },
  "time": int(time()) * 1000000000,
  "fields": {
    "loc": str(float(loc))
  }
}]
db.write_points(kpi)

def parse_args(project_key, name, value):
  kpi = [{
    "measurement": "loc",
    "tags": {
      "project_key": "Test",
      "name": "authorization-service"
    },
    "time": int(time()) * 1000000000,
    "fields": {
      "loc": str(float(loc))
    }
  }]



