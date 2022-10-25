import os
from os import environ

import pandas as pd
from influxdb_client import InfluxDBClient

token = "owNcFjQ_CYRqF17x8Nlt0ByUdGg4xMar51ziPJ7murTdoptCvy6BBwUYwHWL7JdPmWD7qsc4y1FgKRqGrCrPVw=="
org = "mainorg"
url = "http://localhost:8086"
bucket = "sonarqube_kpi"
#   client = InfluxDBClient(url=url, token=token, org=org)
def client(database=None):
    return InfluxDBClient(url=url, token=token, org=org)
query_string = 'from(bucket: "sonarqube_kpi")  |> range(start: -200h, stop: now())  |> filter(fn: (r) => r["_measurement"] == "bugs" or r["_measurement"] == "code_smells")'
r = client(database='sonarqube_kpi').query_api().query(query_string)

df = pd.DataFrame(columns=['measurement', 'time', 'ncloc'])
print(r)

# for k, v in r.items():
#     data = {'measurement': k[0]}
#     for p in v:
#         data.update({'time': p['time'], 'ncloc': p['ncloc']})
#         df = df.append(data, ignore_index=True)

# df.head()