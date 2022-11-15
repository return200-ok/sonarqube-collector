# sonarqube-collector
## Install requirement <br>
```
pip install -r /path/to/requirements.txt
```
## Config env from .env <br>
```
SONARQUBE_TOKEN = "squ_af1e521e19aef5c5de1cb6df89adf3cbb3a9759e"
INFLUX_TOKEN = "KlXfBqa0uSGs0icfE-3g8FsQAoC9hx_QeDsxE3pn0p9wWWLn0bzDZdSmrOijoTA_Tr2MGPnF-LxZl-Nje8YJGQ=="
INFLUX_DB = "http://192.168.3.101:8086"
ORG_NAME = "org"
BUCKET_NAME = "sonarqube_kpi"
SONARQUBE_URL = "http://192.168.3.101:9001"
```
## Run collector to collect data from sonarqube and put to influxdb
```
python3 branch_collecter.py
...
```
