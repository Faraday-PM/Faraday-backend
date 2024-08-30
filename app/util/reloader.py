import requests
import time
import threading

url = "https://faraday-backend.onrender.com/"
delay = 10  # 2 * 60  # 2 mins


def dispatch_thread():
    t = threading.Thread(target=_reload)
    t.start()


def _reload():
    while True:
        time.sleep(delay)
        r = requests.get(url)
        print(f"Pinging server with status code: {r.status_code}")
