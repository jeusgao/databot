# Data sync monitor for mysql.

## How to run
1. env/bin/python3 main.py
2. env/bin/celery -A tasks worker -l INFO --pidfile=var/%n.pid --logfile=logs/%n%I.log
