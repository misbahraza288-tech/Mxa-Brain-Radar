import requests
import feedparser
import time
import os

# --- MXA CORE CONFIG ---
TOKEN = "8751201256:AAGDG-E3mSuNbV6gyjsaagw9fwGm0Arr6kA"
CHAT_ID = "-1003578111414"

# --- LIVE TARGETS ---
TARGETS = {
    "📺 YOUTUBE_LIVE": [
        "https://www.youtube.com/feeds/videos.xml?channel_id=UCX6OQ3DkcsbYNE6H8uQQuVA" # Example link
    ],
    "🌐 GOOGLE_PUBLIC": [
        "https://news.google.com/rss",
        "https://trends.google.com/trends/trendingsearches/daily/rss?geo=IN"
    ],
    "🗣️ SOCIAL_REDDIT": [
        "https://www.reddit.com/r/technology/new/.rss",
        "https://www.reddit.com/r/worldnews/new/.rss"
    ]
}

# GitHub Actions har baar fresh chalta hai, isliye hum ek file mein purane links save karenge
HISTORY_FILE = "seen_links.txt"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_history(link):
    with open(HISTORY_FILE, "a") as f:
        f.write(link + "\n")

seen_data = load_history()

def fire_to_telegram(category, title, link):
    message = (
        f"🚨 <b>MXA LIVE SENSOR: {category}</b>\n\n"
        f"📝 <b>Data:</b> {title}\n"
        f"🔗 <b>Source:</b> {link}"
    )
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}, timeout=5)
        # Tumhara Anti-Ban Rule!
        print(f"✅ Sent! Waiting 4.2 seconds...")
        time.sleep(4.2) 
    except Exception as e:
        print(f"Error: {e}")

def run_radar():
    print("🛸 Mxa Live Radar Activated...")
    new_items_found = 0
    
    for category, urls in TARGETS.items():
        for url in urls:
            try:
                headers = {'User-Agent': 'Mozilla/5.0'}
                response = requests.get(url, headers=headers, timeout=10)
                feed = feedparser.parse(response.content)
                
                for entry in feed.entries[:3]: # Har source se top 3 latest uthao
                    if entry.link not in seen_data:
                        fire_to_telegram(category, entry.title, entry.link)
                        seen_data.add(entry.link)
                        save_history(entry.link)
                        new_items_found += 1
            except Exception as e:
                print(f"Skipping {url}: {e}")
                
    print(f"🏁 Radar Cycle Complete. New items: {new_items_found}")

if __name__ == "__main__":
    run_radar()
  
