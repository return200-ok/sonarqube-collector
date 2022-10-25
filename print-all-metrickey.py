import json
import requests
def getData(url, token):
  session = requests.Session()
  session.auth = token, ''
  call = getattr(session, 'get')
  res = call(url)
  print(type(res.content))
  data = json.loads(res.content)
  return data

token = "squ_af1e521e19aef5c5de1cb6df89adf3cbb3a9759e"
list_metricKeys = getData("https://sonarqube-dev.biplus.com.vn/api/metrics/search", token)
for metricKey in list_metricKeys['metrics']:
    print(metricKey['key'])