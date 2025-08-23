#!/usr/bin/env python
"""
Najprostszy możliwy monitor .onion
Użycie:
    python monitor_onion.py http://adres1.onion [http://adres2.onion ...]
"""
import sys, time, requests

PROXIES = {"http": "socks5h://127.0.0.1:9150", "https": "socks5h://127.0.0.1:9150"}
TIMEOUT = 15  # sekund
SLEEP_SEC = 300  # 5 min

if len(sys.argv) < 2:
    print("Podaj co najmniej jeden URL .onion")
    sys.exit(1)

urls = sys.argv[1:]

while True:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    for u in urls:
        try:
            r = requests.get(u, proxies=PROXIES, timeout=TIMEOUT)
            print(f"{ts}  {u}  OK  {r.status_code}")
        except Exception as e:
            print(f"{ts}  {u}  ERROR  {e}")
    time.sleep(SLEEP_SEC)
