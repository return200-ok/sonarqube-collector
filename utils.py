
import json

import requests


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
def get_project(sonarqube_server, sonarqube_token):
  url = sonarqube_server+"/api/components/search?qualifiers=TRK"
  list_components = get_data(url, sonarqube_token)
  return list_components['components']

#Get list of branch
def get_branch(sonarqube_server, sonarqube_token, component):
  url = sonarqube_server+"/api/project_branches/list?project="+component
  list_branch = get_data(url, sonarqube_token)
  return list_branch['branches']

#Get event scan
def get_event(sonarqube_server, component, branch, token):
  url = sonarqube_server+"/api/project_analyses/search?project="+component+"&branch="+branch
  return get_data(url, token)


#Get list of Metrics Key
def get_metric(sonarqube_server, component, branch, metric_key, token):
  url = sonarqube_server+"/api/measures/component?component="+component+"&branch="+branch+"&metricKeys="+metric_key
  return get_data(url, token)


#Get rule scan
def get_rule(sonarqube_server, component, branch, token):
  url = sonarqube_server+"/api/issues/search?componentKeys="+component+"&branch="+branch
  return get_data(url, token)