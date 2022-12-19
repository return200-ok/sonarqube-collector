import logging
from time import time

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS
from utils import get_branch, get_data, get_event, get_json, get_project


#Put event to InfluxDB
def put_event(project_key, project_name, branch_name, key, date, project_version, write_client):
  data_point = [{
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
  write_client.write_data(data_point)
  logging.info("Wrote "+str(data_point))

#Put event for each project
def event_crawler(sonarqube_server, sonarqube_token, write_client):
  list_project = get_project(sonarqube_server, sonarqube_token)
  for components in list_project:
    list_branch = get_branch(sonarqube_server, sonarqube_token, components["key"])
    for branch in list_branch:
      branch_name = get_json("name", branch)
      project_key = get_json("key", components)
      data = get_event(sonarqube_server, project_key, branch_name, sonarqube_token)
      project_name = get_json("name", components)
      list_event = get_json("analyses", data)
      for event in list_event:
        key = get_json("key", event)
        date = get_json("date", event)
        project_version = get_json("projectVersion", event)
        put_event(project_key, project_name, branch_name, key, date, project_version, write_client)


