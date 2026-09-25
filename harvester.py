import feedparser
import json
from datetime import datetime
import re
from collections import Counter

# --- 1. GLOBAL FEEDS (For index.html) ---
GLOBAL_FEEDS = [
    {"url": "https://www.rt.com/rss/news/", "category": "GLOBAL", "source": "RT News"},
    {"url": "https://feeds.washingtonpost.com/rss/world", "category": "GLOBAL", "source": "Washington Post"},
    {"url": "https://www.aljazeera.com/xml/rss/all.xml", "category": "GLOBAL", "source": "Al Jazeera"},
    {"url": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms", "category": "INDIA", "source": "Times of India"},
    {"url": "https://www.news18.com/commonfeeds/v1/eng/rss/india.xml", "category": "INDIA", "source": "News18"},
    {"url": "https://breakingdefense.com/feed/", "category": "DEFENSE", "source": "Breaking Defense"},
    {"url": "https://cointelegraph.com/rss", "category": "MARKETS", "source": "Crypto"},
    {"url": "https://news.ycombinator.com/rss", "category": "TECH", "source": "Hacker News"}
]

# --- 2. CHINA INTELLIGENCE FEEDS (For china.html) ---
CHINA_FEEDS = [
    # DIPLOMACY & DEFENCE 
    {"url": "https://www.scmp.com/rss/318198/feed", "category": "DIPLOMACY", "source": "SCMP Diplomacy"},
    {"url": "https://www.defensenews.com/arc/outboundfeeds/rss/category/global/asia-pacific/", "category": "DEFENCE", "source": "Defense News Asia"},
    
    # MARKETS & ECONOMY 
    {"url": "https://www.scmp.com/rss/318200/feed", "category": "MARKETS", "source": "SCMP Economy"},
    {"url": "https://www.ft.com/china?format=rss", "category": "MARKETS", "source": "Financial Times China"},
    
    # SCIENCE & TECH 
    {"url": "https://www.scmp.com/rss/318216/feed", "category": "SCIENCE", "source": "SCMP Tech"},
    {"url": "https://techcrunch.com/category/asia/feed/", "category": "SCIENCE", "source": "TechCrunch Asia"}
]

def clean_html(raw_html):
    # SCMP uses heavy HTML in summaries; this regex strips it for a clean UI
    cleanr = re.compile('<.*?>')
    return re.sub(cleanr, '', str(raw_html))

def process_feeds(feeds_list, filename):
    trends = []
    id_counter = 1
    
    for feed in feeds_list:
        try:
            parsed = feedparser.parse(feed["url"])
            for entry in parsed.entries[:12]: 
                summary = clean_html(entry.get("summary", ""))
                if len(summary) > 130:
                    summary = summary[:130] + "..."
                    
                trends.append({
                    "id": id_counter,
                    "title": entry.title,
                    "summary": summary if summary.strip() else "No summary provided by source.",
                    "category": feed["category"],
                    "source": feed["source"],
                    "url": entry.link,
                    "timestamp": datetime.now().strftime("%H:%M UTC")
                })
                id_counter += 1
        except Exception as e:
            print(f"Skipping feed {feed['source']} due to error: {e}")
            
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(trends, f, indent=4, ensure_ascii=False)
    print(f"Successfully harvested {len(trends)} signals for {filename}.")
    return trends

def generate_trend_identifier(china_trends):
    # Extracts keywords from headlines to simulate the Social Pulse identifier
    words = []
    stop_words = {"china", "chinese", "beijing", "hong", "kong", "says", "with", "from", "that", "over", "after", "will", "this", "have", "more", "their", "could", "than", "about", "into", "update"}
    
    for t in china_trends:
        tokens = re.findall(r'\b[a-zA-Z]{5,}\b', t['title'].lower())
        words.extend([w for w in tokens if w not in stop_words])
    
    top_keywords = [word[0].upper() for word in Counter(words).most_common(6)]
    if not top_keywords:
        top_keywords = ["TRADE", "SECURITY", "TECH", "POLICY", "MARKET", "MILITARY"]
        
    # Generate Synthetic Daily Figurements based on scraped data density
    activity_level = "SURGING" if len(china_trends) > 30 else "STABLE"
    sentiment = "CAUTIOUS" if any(w in top_keywords for w in ["MILITARY", "DEFENCE", "TARIFF", "STRIKE", "TENSION"]) else "OPTIMISTIC"
    
    pulse_data = {
        "social_pulse": top_keywords,
        "daily_figurements": {
            "weibo_activity": activity_level,
            "market_sentiment": sentiment,
            "data_nodes": str(len(china_trends))
        },
        "last_updated": datetime.now().strftime("%H:%M UTC")
    }
    
    with open("china_pulse.json", "w", encoding="utf-8") as f:
        json.dump(pulse_data, f, indent=4)
    print("Trend Identifier (china_pulse.json) generated.")

if __name__ == "__main__":
    print("Harvesting Global Dashboard Data...")
    process_feeds(GLOBAL_FEEDS, "trends.json")
    
    print("\nHarvesting China Dashboard Data...")
    china_data = process_feeds(CHINA_FEEDS, "china_trends.json")
    generate_trend_identifier(china_data)
