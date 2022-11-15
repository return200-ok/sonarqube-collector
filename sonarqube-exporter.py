import requests, time
from prometheus_client import start_http_server, Gauge, Info
from sonarqube import SonarQubeClient
sonarqube_server = "http://192.168.3.101:9001"
sonarqube_token = "squ_af1e521e19aef5c5de1cb6df89adf3cbb3a9759e"
sonar = SonarQubeClient(sonarqube_url=sonarqube_server, token=sonarqube_token)

# event = Info('event', 'Description of info')
bugs = Gauge('bugs', 'Number of bugs')

class Server:
    def __init__(self, value):
        self.value = value

def get_server_info():

    # projects = list(sonar.projects.search_projects())
    # for i in projects:
    #     component = sonar.measures.get_component_with_specified_measures(component=i['key'], branch="master", fields="metrics", metricKeys="bugs")
    #     data = Server(component['component']['measures'][0]['value'])
    #     bugs.set(data.value)

    component = sonar.measures.get_component_with_specified_measures(component="bac", branch="master", fields="metrics", metricKeys="bugs")
    data = Server(component['component']['measures'][0]['value'])
    bugs.set(data.value)

    # project_analyses_and_events = list(sonar.project_analyses.search_project_analyses_and_events(project="bac", branch="master"))
    # event_key = Server(project_analyses_and_events[0])
    # event.info({'key': 'AYPuPSmAIVrsPVkR77ZP', 'date': '2022-10-19T03:12:17+0000', 'revision': 'a7257ec8d4f30b554ca45df9de76ebf649123345', 'detectedCI': 'undetected'})

def main():
    start_http_server(8192)
    while True:
        get_server_info()
        time.sleep(60)

main()
