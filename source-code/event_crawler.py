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

#Get event scan
def get_event(component, branch, token):
  url = sonarqube_server+"/api/project_analyses/search?project="+component+"&branch="+branch
  return get_data(url, token)

#Put event to InfluxDB
def put_event(project_key, project_name, branch_name, key, date, project_version):
  client = InfluxDBClient(url=influx_server, token=influx_token, org=org_name)

  kpi = [{
    "measurement": project_key,
    "tags": {
      "project_name": project_name,
      "branch_name": branch_name,
      "key": key,
      "date": date,
      "projectVersion": project_version,
    },
    "fields": {
      "event": key
    }
  }]
  write_api = client.write_api(write_options=ASYNCHRONOUS)
  write_api.write(bucket_name, org_name, kpi)
  print ("write ", kpi," to bucket "+bucket_name)

#Put event for each project
def event_crawler():
  list_project = get_project()
  for components in list_project:
    list_branch = get_branch(components["key"])
    for branch in list_branch:
      branch_name = get_json("name", branch)
      project_key = get_json("key", components)
      data = get_event(project_key, branch_name, sonarqube_token)
      project_name = get_json("name", components)
      list_event = get_json("analyses", data)
      for event in list_event:
        key = get_json("key", event)
        date = get_json("date", event)
        project_version = get_json("projectVersion", event)
        put_event(project_key, project_name, branch_name, key, date, project_version)



if __name__ == '__main__':
  event_crawler()

