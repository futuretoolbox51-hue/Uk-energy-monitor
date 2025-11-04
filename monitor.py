import requests
from bs4 import BeautifulSoup
from telegram import Bot
import os

# --- Telegram setup ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
bot = Bot(token=TELEGRAM_TOKEN)

# --- URLs to monitor ---
urls = [
    "https://www.just-eat.co.uk/area/se7-charton?filter=grill&filter=new",
    "https://www.just-eat.co.uk/area/sw3-chelsea?filter=grill&filter=new",
    "https://www.just-eat.co.uk/area/br7-chislehurst?filter=grill&filter=new",
    "https://www.just-eat.co.uk/area/ec1a-city_of_london?filter=grill&filter=new",
    "https://www.just-eat.co.uk/area/sw11-clapham?filter=grill&filter=new",
    "https://www.just-eat.co.uk/area/ec1-clerkenwell?filter=grill&filter=new",
    "https://www.just-eat.co.uk/area/e5-clapton?filter=grill&filter=new",
    "https://www.just-eat.co.uk/area/sw4-clapham?filter=grill&filter=new",
    "https://www.just-eat.co.uk/area/ec1p-clerkenwell?filter=grill&filter=new",
    "https://www.just-eat.co.uk/area/ec1r-clerkenwell?filter=grill&filter=new"
]

# --- Keywords to search for ---
keywords = ["restaurant", "takeaway"]

found_count = 0

print("📖 Starting URL scan...", flush=True)

for url in urls:
    try:
        print(f"🔎 Checking URL: {url}", flush=True)
        response = requests.get(url, timeout=15)
        soup = BeautifulSoup(response.text, "html.parser")
        page_text = soup.get_text().lower()

        for keyword in keywords:
            if keyword.lower() in page_text:
                found_count += 1
                message = f"✅ Keyword '{keyword}' found!\nURL: {url}"
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
                print(f"✅ Sent Telegram alert for keyword '{keyword}'", flush=True)
                break  # avoid sending multiple alerts for same URL

    except Exception as e:
        print(f"❌ Error checking {url}: {e}", flush=True)

print(f"📊 Scan completed. Total URLs with keywords found: {found_count}", flush=True)
