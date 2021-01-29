# Data sync monitor for mysql.

## How to run
env/bin/python3 main.py
env/bin/celery -A tasks worker -l INFO --pidfile=var/%n.pid --logfile=logs/%n%I.log
