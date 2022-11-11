from sonarqube import SonarQubeClient
sonarqube_server = "http://192.168.3.101:9001"
sonarqube_token = "squ_af1e521e19aef5c5de1cb6df89adf3cbb3a9759e"
sonar = SonarQubeClient(sonarqube_url=sonarqube_server, token=sonarqube_token)
# projects = list(sonar.projects.search_projects())
# for i in projects:
#     print(i['key'])
component = sonar.measures.get_component_with_specified_measures(component="bac", branch="master", fields="metrics", metricKeys="bugs")
print(component['component']['measures'][0]['value'])