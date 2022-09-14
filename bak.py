

# url = 'https://sonarqube.biplus.com.vn/api/measures/component?component=Test&metricKeys=ncloc'
# myToken = 'squ_a4c1bd1d9be8613d1179234e634d7541af960f2b'
# session = requests.Session()
# session.auth = myToken, ''
# call = getattr(session, 'get')
# res = call(url)

# url_component = "https://sonarqube.biplus.com.vn/api/components/search?qualifiers=TRK"
# res_component = call(url_component)
# output = json.loads(res_component.content)

# for components in output['components']:
#     print (components['key'])


# output = json.loads(res.content)
# project_key=output["component"]["key"]
# name=output["component"]["name"]
# metric=output["component"]["measures"][0]["metric"]
# loc=output["component"]["measures"][0]["value"]
# db = InfluxDBClient("localhost", 8086)
# db.switch_database("sonarqube_kpi")
# kpi = [{
#   "measurement": metric,
#   "tags": {
#     "project_key": project_key,
#     "name": name
#   },
#   "time": int(time()) * 1000000000,
#   "fields": {
#     "loc": str(float(loc))
#   }
# }]
# db.write_points(kpi)


