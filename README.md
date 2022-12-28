# Sonarqube Analysis Dashboard
The `Sonarqube Analysis Dashboard` dashboard presents all metrics in detail and is meant for finer-grained analytics.

## Quick start with `docker`
Run command below (edit env):
```
docker run -d \
SONARQUBE_TOKEN="squ_af1e521e19aef5c5de1cb6df89adf3cbb3a9759e" \
INFLUX_TOKEN="KlXfBqa0uSGs0icfE-3g8FsQAoC9hx_QeDsxE3pn0p9wWWLn0bzDZdSmrOijoTA_Tr2MGPnF-LxZl-Nje8YJGQ==" \
INFLUX_DB="http://192.168.3.101:8086" \
ORG_NAME="org" \
BUCKET_NAME="sonarqube_kpi" \
SONARQUBE_URL="http://192.168.3.101:9001" \
return200/sonarqube-crawler:0.1.0
```

# Use

## Run

### Build image
Run command below:
```
docker build -t sonarqube-crawler:0.1.0 .
```
### Change cronjob
Cronjob is set " 0 0 * * * " in current.
```
cat crontab
# START CRON JOB
0 0 * * * /usr/local/bin/python3 /sonarqube-crawler/main.py > /proc/1/fd/1 2>/proc/1/fd/2
# END CRON JOB
```

### Run with `docker compose`

#### Define your environment

Using the sample environment as a base, 

```bash
$ cd docker-compose
$ cp config/sample.env config/production.env
$ vim config/production.env
```
#### Start with docker compose 
To run with your newly configured environment, execute the following.

```bash
docker-compose up -d
```
### Viewing data with Grafana
By default, a grafana instance preloaded with templated dashboards will be started. Use your browser to view [http://localhost:3000](http://localhost:3000). The default username is `admin` and default password is `admin`. The dasboards are then accessible under the 'Home' tab.

### Templated Grafana dashboards

The files under `dashboards/*.json` contain a grafana dashboards described below.

#### `Sonarqube Analysis Dashboard` dashboard

The `Sonarqube Analysis Dashboard` presents all metrics in detail and is meant for finer-grained analytics. See an image of the dasboard with data below.
![overview!](https://github.com/return200-ok/sonarqube-influx-collector/blob/master/assets/Sonarqube-Analysis-Dashboard.png?raw=true)