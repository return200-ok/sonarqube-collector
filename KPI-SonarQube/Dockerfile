FROM python:3-alpine

COPY requirements.txt .
RUN apk update 
RUN pip3 install -r requirements.txt
COPY sonarq-crawler.py ./
RUN touch /var/log/cron.log
RUN echo "* * * * * python3 /sonarq-crawler.py >> /var/log/cron.log 2>&1" > /etc/crontabs/root
RUN crond
