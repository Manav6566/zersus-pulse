import feedparser
import json
from datetime import datetime

# Heavily shifted focus to Global, Indian Domestic, and Defense news.
FEEDS = [
    # GLOBAL NEWS
    {"url": "https://www.rt.com/rss/news/", "category": "GLOBAL", "source": "RT News"},
    {"url": "https://feeds.washingtonpost.com/rss/world", "category": "GLOBAL", "source": "Washington Post"},
    {"url": "https://www.aljazeera.com/xml/rss/all.xml", "category": "GLOBAL", "source": "Al Jazeera"},
    
    # INDIA DOMESTIC
    {"url": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms", "category": "INDIA", "source": "Times of India"},
    {"url": "https://www.news18.com/commonfeeds/v1/eng/rss/india.xml", "category": "INDIA", "source": "News18"},
    {"url": "https://feeds.feedburner.com/ndtvnews-india-news", "category": "INDIA", "source": "NDTV India"},
    
    # DEFENSE & MILITARY
    {"url": "https://breakingdefense.com/feed/", "category": "DEFENSE", "source": "Breaking Defense"},
    {"url": "https://www.defensenews.com/arc/outboundfeeds/rss/category/global/", "category": "DEFENSE", "source": "Defense News"},
    
    # MARKETS & ECONOMY
    {"url": "https://cointelegraph.com/rss", "category": "MARKETS", "source": "Crypto"},
    {"url": "https://techcrunch.com/feed/", "category": "MARKETS", "source": "TechCrunch"},
    
    # TECH & AI (Reduced footprint)
    {"url": "https://news.ycombinator.com/rss", "category": "TECH", "source": "Hacker News"}
]

def fetch_trends():
    trends = []
    id_counter = 1
    
    for feed in FEEDS:
        try:
            parsed = feedparser.parse(feed["url"])
            
            # Pulling up to 12 top stories per feed to keep the dashboard packed
            for entry in parsed.entries[:12]: 
                summary = entry.get("summary", "")
                if "<" in summary: 
                    summary = summary.split("<")[0]
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
            
    with open("trends.json", "w", encoding="utf-8") as f:
        json.dump(trends, f, indent=4, ensure_ascii=False)
    print(f"Successfully harvested {len(trends)} signals.")

if __name__ == "__main__":
    fetch_trends()
