import json
import logging
import os
from datetime import datetime, timedelta
from os import environ
from time import time

import requests
import rfc3339
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import ASYNCHRONOUS

# Load env
load_dotenv()

sonarqube_token = os.getenv('INFLUX_TOKEN')
influx_token = os.getenv('INFLUX_TOKEN')
influx_server = os.getenv('INFLUX_DB')
org_name = os.getenv('ORG_NAME')
bucket_name = os.getenv('BUCKET_NAME')
sonarqube_server = os.getenv('SONARQUBE_URL')

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

#Get list of Metrics Key
def get_metric(component, branch, metric_key, token):
  url = sonarqube_server+"/api/measures/component?component="+component+"&branch="+branch+"&metricKeys="+metric_key
  return get_data(url, token)

#Put data_point metric to InfluxDB
def put_metric(metric_key, project_key, project_name, branch_name, value):
  client = InfluxDBClient(url=influx_server, token=influx_token, org=org_name)

  data_point = [{
    "measurement": project_key,
    "tags": {
      "metric": metric_key,
      "project_name": project_name,
      "branch_name": branch_name,
    },
    "time": int(time()) * 1000000000,
    "fields": {
      metric_key: value
    }
  }]
  write_api = client.write_api(write_options=ASYNCHRONOUS)
  write_api.write(bucket_name, org_name, data_point)
  logging.info("write "+str(data_point)+" to bucket "+bucket_name)

#Put metrics for each project
def metric_crawler():
  list_project = get_project()
  for components in list_project:
    list_branch = get_branch(components["key"])
    project_key = get_json("key", components)
    project_name = get_json("name", components)
    for branch in list_branch:
      branch_name = get_json("name", branch)
      list_metric = ["alert_status", "ncloc_language_distribution", "ncloc", "false_positive_issues", "blocker_violations", "critical_violations", "major_violations", "minor_violations", "info_violations", "open_issues", "confirmed_issues", "reopened_issues", "code_smells", "sqale_rating", "sqale_index", "bugs", "vulnerabilities", "security_rating", "coverage", "tests", "duplicated_lines_density", "duplicated_files", "duplicated_blocks", "duplicated_lines"]
      for metric_key in list_metric:
        data = get_metric(project_key, branch_name, metric_key, sonarqube_token)
        if len(data["component"]["measures"]) == 0:
          value = 0
        else: 
          value = get_json("value", data["component"]["measures"][0])
        put_metric(metric_key, project_key, project_name, branch_name, value)



if __name__ == '__main__':
  metric_crawler()

