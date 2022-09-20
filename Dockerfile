FROM python:3-alpine

COPY requirements.txt .
RUN apk update 
RUN pip3 install -r requirements.txt
COPY . ./
RUN mkdir etc/cron.d
RUN touch /var/log/cron.log
RUN echo "* * * * * XDG_RUNTIME_DIR=/run/user/$(id -u) /usr/local/bin/python3 /test-crawler.py" >> /etc/crontabs/root
# CMD [ "crond" ]


# ENTRYPOINT ["python3", "sonarqube-crawler.py"]
