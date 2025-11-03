# test_telegram.py
import os
import requests
import sys

def send_test_message():
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("ERROR: TELEGRAM_TOKEN or TELEGRAM_CHAT_ID missing in environment.")
        sys.exit(1)

    text = "Test message from monitor.py — Telegram working ✅"
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        resp = requests.post(url, data={"chat_id": chat_id, "text": text}, timeout=15)
        print("HTTP status:", resp.status_code)
        print("Response body:", resp.text)
        j = resp.json()
        if j.get("ok"):
            print("✅ Telegram API returned ok = true. Message should be delivered.")
        else:
            print("❌ Telegram API returned ok = false. See response above.")
    except Exception as e:
        print("Exception while sending:", e)
        sys.exit(2)

if __name__ == "__main__":
    send_test_message()
