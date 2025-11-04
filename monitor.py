import json
import requests
import os
import sys

# --- Telegram credentials from GitHub Secrets ---
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# --- Helper: Send message to Telegram ---
def send_message(text):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        resp = requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=15)
        if resp.status_code == 200 and resp.json().get("ok"):
            print("✅ Message sent to Telegram", flush=True)
        else:
            print("❌ Telegram message failed:", resp.text, flush=True)
    except Exception as e:
        print("❌ Exception while sending Telegram message:", e, flush=True)

# --- Helper: Extract all URLs recursively from bookmarks JSON ---
def extract_urls(data):
    urls = []
    if isinstance(data, dict):
        if "url" in data:
            urls.append(data["url"])
        for value in data.values():
            urls.extend(extract_urls(value))
    elif isinstance(data, list):
        for item in data:
            urls.extend(extract_urls(item))
    return urls

# --- Step 1: Read bookmarks file ---
print("📖 Reading bookmarks JSON file...", flush=True)
try:
    with open("bookmarks-2025-09-17.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except Exception as e:
    print("❌ Error reading JSON file:", e, flush=True)
    sys.exit(1)

# --- Step 2: Extract URLs ---
urls = extract_urls(data)
print(f"✅ Total URLs found: {len(urls)}", flush=True)

# --- Step 3: Scan each URL for keywords ---
keywords = ["restaurant", "takeaway"]
found_count_
