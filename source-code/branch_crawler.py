import os
from os import environ
from time import time
import json
import requests
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS


# sonarqube_token = os.environ.get('SONARQUBE_TOKEN')
# influx_token = os.environ.get('INFLUX_TOKEN')
# influx_server = os.environ.get('INFLUX_SERVER')
# org_name = os.environ.get('ORG_NAME')
# bucket_name = os.environ.get('BUCKET_NAME')
# sonarqube_server = os.environ.get('SONARQUBE_SERVER')

sonarqube_token = "squ_af1e521e19aef5c5de1cb6df89adf3cbb3a9759e"
influx_token = "KlXfBqa0uSGs0icfE-3g8FsQAoC9hx_QeDsxE3pn0p9wWWLn0bzDZdSmrOijoTA_Tr2MGPnF-LxZl-Nje8YJGQ=="
influx_server = "http://192.168.3.101:8086"
org_name = "org"
bucket_name = "sonarqube_kpi"
sonarqube_server = "http://192.168.3.101:9001"

#Get data from url and convert to JSON
def get_data(url, token):
  session = requests.Session()
  session.auth = token, ''
  call = getattr(session, 'get')
  res = call(url)
  data = json.loads(res.content)
  return data

def get_json(element, json_data):
  if element in json_data:
    return json_data[element]
  else:
    return 0

#Get list of project
def get_project():
  url = sonarqube_server+"/api/components/search?qualifiers=TRK"
  list_components = get_data(url, sonarqube_token)
  return list_components['components']

#Get list of branch
def get_branch(component):
  url = sonarqube_server+"/api/project_branches/list?project="+component
  list_branch = get_data(url, sonarqube_token)
  return list_branch['branches']

#Put branch to InfluxDB
def put_branch(project_key, project_name, branch_name, is_main, branch_type, status, analysis_date):
  client = InfluxDBClient(url=influx_server, token=influx_token, org=org_name)
  kpi = [{
    "measurement": project_key,
    "tags": {
      "project_name": project_name,
      "isMain": is_main,
      "branch_type": branch_type,
      "status": status,
      "analysisDate": analysis_date,
    },
    "time": int(time()) * 1000000000,
    "fields": {
      "branch_name": branch_name
    }
  }]
  write_api = client.write_api(write_options=ASYNCHRONOUS)
  write_api.write(bucket_name, org_name, kpi)
  print ("write ", kpi," to bucket "+bucket_name)

#Put branch for each project
def branch_crawler():
  list_project = get_project()
  for components in list_project:
    data = get_branch((components['key']))
    project_key = get_json('key', components)
    project_name = get_json('name', components)
    branch_name = get_json('name', data[0])
    is_main = get_json('isMain', data[0])
    branch_type = get_json('type', data[0])
    status = get_json('qualityGateStatus', data[0]["status"])
    analysis_date = get_json('analysisDate', data[0])
    put_branch(project_key, project_name, branch_name, is_main, branch_type, status, analysis_date)



if __name__ == '__main__':
  branch_crawler()

