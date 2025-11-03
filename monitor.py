import json, sqlite3, requests, os
from bs4 import BeautifulSoup
from datetime import datetime
from telegram import Bot

# === Configuration ===
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
BOOKMARKS_JSON = "bookmarks-2025-09-17.json"
DB_FILE = "monitor.db"
USER_AGENT = "Mozilla/5.0 (compatible; MonitorBot/1.0)"
bot = Bot(token=TELEGRAM_TOKEN)

KEYWORDS = [
    "takeaway","take-away","take away","order now","order online",
    "menu","delivery","restaurant","open now","opening hours","collection"
]

def load_urls(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    urls = []
    def collect(n):
        if isinstance(n, dict):
            if n.get("type") == "text/x-moz-place" and n.get("url"):
                urls.append(n["url"])
            for c in n.get("children", []):
                collect(c)
        elif isinstance(n, list):
            for c in n:
                collect(c)
    collect(data)
    return list(set(urls))

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS pages (url TEXT PRIMARY KEY, has_rest INTEGER, last TIMESTAMP)")
    conn.commit()
    return conn

def detect_restaurant(html):
    soup = BeautifulSoup(html, "html.parser")
    for s in soup.find_all("script", type="application/ld+json"):
        try:
            j = json.loads(s.string or "{}")
            def walk(o):
                if isinstance(o, dict):
                    t = o.get("@type") or o.get("type")
                    if t == "Restaurant" or (isinstance(t, list) and "Restaurant" in t):
                        return True
                    return any(walk(v) for v in o.values())
                if isinstance(o, list):
                    return any(walk(v) for v in o)
                return False
            if walk(j): return True
        except Exception: pass
    text = soup.get_text(" ").lower()
    return any(k in text for k in KEYWORDS)

def notify(msg):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg, parse_mode="HTML")
    except Exception as e:
        print("Notify error:", e)

def main():
    urls = load_urls(BOOKMARKS_JSON)
    conn = init_db()
    cur = conn.cursor()
    for u in urls:
        try:
            r = requests.get(u, headers={"User-Agent": USER_AGENT}, timeout=20)
        except Exception as e:
            print("Fetch fail", u, e)
            continue
        has = 1 if detect_restaurant(r.text) else 0
        cur.execute("SELECT has_rest FROM pages WHERE url=?", (u,))
        row = cur.fetchone()
        if row is None:
            cur.execute("INSERT INTO pages VALUES (?,?,?)", (u, has, datetime.utcnow()))
            conn.commit()
            if has:
                notify(f"🔔 New restaurant(s) detected \n{u}")
        else:
            prev = row[0]
            if prev == 0 and has == 1:
                notify(f"🚨 Restaurant opened here \n{u}")
            cur.execute("UPDATE pages SET has_rest=?, last=? WHERE url=?",
                        (has, datetime.utcnow(), u))
            conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
