import os
import requests
from bs4 import BeautifulSoup
from telegram import Bot

# -------------------------
# CONFIGURATION
# -------------------------
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
KEYWORDS = ["restaurant", "takeaway"]

# For testing/demo purpose, direct URLs list
URLS = [
    "https://www.just-eat.co.uk/area/ec1a-city_of_london?filter=grill&filter=new",
    "https://www.just-eat.co.uk/area/sw11-clapham?filter=grill&filter=new",
    "https://www.just-eat.co.uk/area/ec1-clerkenwell?filter=grill&filter=new"
]

# Initialize Telegram bot
bot = Bot(token=TELEGRAM_TOKEN)

# -------------------------
# MAIN SCANNING LOGIC
# -------------------------
found_count = 0

print("📖 Starting URL scan...", flush=True)
print(f"📁 Current directory: {os.getcwd()}", flush=True)
print(f"📂 URLs to scan: {len(URLS)}", flush=True)

for url in URLS:
    print(f"🔍 Fetching URL: {url}", flush=True)
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text().lower()

        for keyword in KEYWORDS:
            if keyword.lower() in page_text:
                found_count += 1
                message = f"🍽️ Keyword '{keyword}' found at URL:\n{url}"
                print(f"✅ {message}", flush=True)

                # Send Telegram message
                if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
                    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
                break  # stop checking other keywords for this URL

    except Exception as e:
        print(f"⚠️ Error fetching {url}: {e}", flush=True)

print(f"✅ Scan complete! Total matches: {found_count}", flush=True)

