from influxdb import InfluxDBClient
from time import time
import json
import requests


def getData(url, token):
  session = requests.Session()
  session.auth = token, ''
  call = getattr(session, 'get')
  res = call(url)
  print(type(res.content))
  data = json.loads(res.content)
  # return data
  print("----------------------")
  print(data)

def parseData(component, metricKeys, token):
  url = "https://sonarqube.biplus.com.vn/api/measures/component?component="+component+"&metricKeys="+metricKeys
  return getData(url, token)


def insertData(metricKey, project_key, name, value):
  db = InfluxDBClient(host="localhost", port=8086, username="caolv", password="admin1998")
  db.switch_database("sonarqube_kpi")
  kpi = [{
    "measurement": metricKey,
    "tags": {
      "project_key": project_key,
      "name": name
    },
    "time": int(time()) * 1000000000,
    "fields": {
      "value": str(value)
    }
  }]
  db.write_points(kpi)
getData("https://sonarqube.biplus.com.vn/api/measures/component?component=Test&metricKeys=bugs", "squ_a4c1bd1d9be8613d1179234e634d7541af960f2b")
# if __name__ == '__main__':
  # token = "squ_a4c1bd1d9be8613d1179234e634d7541af960f2b"
  # list_component = getData("https://sonarqube.biplus.com.vn/api/components/search?qualifiers=TRK", token)
  # list_metricKeys = getData("https://sonarqube.biplus.com.vn/api/metrics/search", token)
  # for components in list_component['components']:
  #   for metricKey in list_metricKeys['metrics']:
  #     data = parseData((components['key']), (metricKey['key']), token)
  #     project_key = data["component"]["key"]
  #     name = data["component"]["name"]
  #     value = ""
  #     if len(data["component"]["measures"]) == 0:
  #       value = "null"
  #     elif "value" in data["component"]["measures"][0]: 
  #       value = data["component"]["measures"][0]["value"]
  #     else:
  #       print("Key doesn't exist in JSON data")
  #     insertData((metricKey['key']), project_key, name, value)



