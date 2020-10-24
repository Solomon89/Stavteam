import threading
import time
from app import dbFunctions


def timer(interval):
    data = threading.local()
    while True:
        time.sleep(interval)
        dbFunctions.killExpiredSessions(interval)


deleteInterval = 3600
t = threading.Thread(target=timer, name="killSessions", args=(deleteInterval,), daemon=True)
t.start()
