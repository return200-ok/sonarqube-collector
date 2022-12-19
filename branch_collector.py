import logging
from time import time

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS
from utils import get_branch, get_data, get_json, get_project


#Put branch to InfluxDB
def put_branch(project_key, project_name, branch_name, is_main, branch_type, status, analysis_date, write_client):
  data_point = [{
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
  write_client.write_data(data_point)
  logging.info("Wrote "+str(data_point))

#Put branch for each project
def branch_crawler(sonarqube_server, sonarqube_token, write_client):
  list_project = get_project(sonarqube_server, sonarqube_token)
  for components in list_project:
    data = get_branch(sonarqube_server, sonarqube_token, components['key'])
    project_key = get_json('key', components)
    project_name = get_json('name', components)
    branch_name = get_json('name', data[0])
    is_main = get_json('isMain', data[0])
    branch_type = get_json('type', data[0])
    status = get_json('qualityGateStatus', data[0]["status"])
    analysis_date = get_json('analysisDate', data[0])
    put_branch(project_key, project_name, branch_name, is_main, branch_type, status, analysis_date, write_client)


