from fastapi import FastAPI
from datetime import datetime
import requests
import threading
import time

app = FastAPI()
last_ping = datetime.utcnow()

import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

@app.get("/")
def home():
    return {"status": "monitor running"}
    
@app.post("/heartbeat")
def heartbeat():
    global last_ping
    last_ping = datetime.utcnow()
    return {"status": "ok"}

def monitor():
    global last_ping
    while True:
        if (datetime.utcnow() - last_ping).seconds > 60:
            requests.get(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                params={"chat_id": CHAT_ID, "text": "🚨 Heartbeat missed!"}
            )
        time.sleep(10)

@app.on_event("startup")
def start_monitor():
    threading.Thread(target=monitor, daemon=True).start()
