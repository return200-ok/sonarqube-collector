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

#Get rule scan
def get_rule(component, branch, token):
  url = sonarqube_server+"/api/issues/search?componentKeys="+component+"&branch="+branch
  return get_data(url, token)

#Put issue to InfluxDB
def put_rule(project_key, project_name, branch_name, key, rule, severity, status, message, debt, author, creation_date, update_date, issue_type):
  client = InfluxDBClient(url=influx_server, token=influx_token, org=org_name)

  data_point = [{
    "measurement": project_key,
    "tags": {
      "project_name": project_name,
      "branch_name": branch_name,
      "key": key,
      "rule": rule,
      "severity": severity,
      "status": status,
      "message": message,
      "debt": debt,
      "author": author,
      "creation_date": creation_date,
      "update_date": update_date,
      "issue_type": issue_type,
    },
    "fields": {
      "rule-id": key
    }
  }]
  write_api = client.write_api(write_options=ASYNCHRONOUS)
  write_api.write(bucket_name, org_name, data_point)
  logging.info("write "+str(data_point)+" to bucket "+bucket_name)

#Put event for each project
def rule_crawler():
  list_project = get_project()
  for components in list_project:
    list_branch = get_branch(components["key"])
    for branch in list_branch:
      branch_name = get_json("name", branch)
      project_key = get_json("key", components)
      data = get_rule(project_key, branch_name, sonarqube_token)
      project_name = get_json("name", components)
      list_issue = get_json("issues", data)
      for issue in list_issue:
        key = get_json("key", issue)
        rule = get_json("rule", issue)
        severity = get_json("severity", issue)
        status = get_json("status", issue)
        message = get_json("message", issue)
        debt = get_json("debt", issue)
        author = get_json("author", issue)
        creation_date = get_json("creationDate", issue)
        update_date = get_json("updateDate", issue)
        issue_type = get_json("type", issue)
        put_rule(project_key, project_name, branch_name, key, rule, severity, status, message, debt, author, creation_date, update_date, issue_type)


if __name__ == '__main__':
  rule_crawler()
