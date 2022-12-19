import logging
from time import time

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS
from utils import get_branch, get_data, get_json, get_metric, get_project


#Put data_point metric to InfluxDB
def put_metric(metric_key, project_key, project_name, branch_name, value, write_client):
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
  write_client.write_data(data_point)
  logging.info("Wrote "+str(data_point))

#Put metrics for each project
def metric_crawler(sonarqube_server, sonarqube_token, write_client):
  list_project = get_project(sonarqube_server, sonarqube_token)
  for components in list_project:
    list_branch = get_branch(sonarqube_server, sonarqube_token, components["key"])
    project_key = get_json("key", components)
    project_name = get_json("name", components)
    for branch in list_branch:
      branch_name = get_json("name", branch)
      list_metric = ["alert_status", "ncloc_language_distribution", "ncloc", "false_positive_issues", "blocker_violations", "critical_violations", "major_violations", "minor_violations", "info_violations", "open_issues", "confirmed_issues", "reopened_issues", "code_smells", "sqale_rating", "sqale_index", "bugs", "vulnerabilities", "security_rating", "coverage", "tests", "duplicated_lines_density", "duplicated_files", "duplicated_blocks", "duplicated_lines"]
      for metric_key in list_metric:
        data = get_metric(sonarqube_server, project_key, branch_name, metric_key, sonarqube_token)
        if len(data["component"]["measures"]) == 0:
          value = 0
        else: 
          value = get_json("value", data["component"]["measures"][0])
        put_metric(metric_key, project_key, project_name, branch_name, value, write_client)



