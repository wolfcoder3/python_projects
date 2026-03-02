from fastapi import FastAPI
from datetime import datetime, timedelta
import threading
import requests

app = FastAPI()
last_ping = datetime.utcnow()

TELEGRAM_TOKEN = "5746897470:AAG8MxzDzsqRKj4XsWkxXRj5LBtvu661t6w"
TELEGRAM_CHAT_ID = "-1001967474585"

def check_health():
    global last_ping
    while True:
        if datetime.utcnow() - last_ping > timedelta(seconds=60):
            requests.get(
                f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                params={"chat_id": TELEGRAM_CHAT_ID, "text": "🚨 Heartbeat missed! Internet might be down"},
            )
        time.sleep(10)

@app.on_event("startup")
def start_checker():
    threading.Thread(target=check_health, daemon=True).start()

@app.post("/heartbeat")
def heartbeat():
    global last_ping
    last_ping = datetime.utcnow()
    return {"status": "ok"}
