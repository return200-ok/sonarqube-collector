FROM python:3-alpine
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . ./
# ENTRYPOINT ["python3", "sonarqube-crawler.py"]
