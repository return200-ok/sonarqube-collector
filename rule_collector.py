import logging
from time import time

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import ASYNCHRONOUS
from utils import get_branch, get_data, get_json, get_project, get_rule


#Put issue to InfluxDB
def put_rule(project_key, project_name, branch_name, key, rule, severity, status, message, debt, author, creation_date, update_date, issue_type, write_client):
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
  write_client.write_data(data_point)
  logging.info("Wrote "+str(data_point))

#Put event for each project
def rule_crawler(sonarqube_server, sonarqube_token, write_client):
  list_project = get_project(sonarqube_server, sonarqube_token)
  for components in list_project:
    list_branch = get_branch(sonarqube_server, sonarqube_token, components["key"])
    for branch in list_branch:
      branch_name = get_json("name", branch)
      project_key = get_json("key", components)
      data = get_rule(sonarqube_server, project_key, branch_name, sonarqube_token)
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
        put_rule(project_key, project_name, branch_name, key, rule, severity, status, message, debt, author, creation_date, update_date, issue_type, write_client)

