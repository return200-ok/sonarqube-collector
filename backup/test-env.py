import os
from os import environ
from datetime import datetime
logname = os.environ.get('LOGNAME')
print(datetime.now().strftime("%H:%M"))