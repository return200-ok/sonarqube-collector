echo "* * * * * python3 /test-crawler.py >> /var/log/cron.log 2>&1" >> /etc/crontabs/root
crond -l 2 -f > /dev/stdout 2> /dev/stderr &