import feedparser
import json
from datetime import datetime

# Expanded list of free RSS feeds spanning all your categories
FEEDS = [
    # TECH & SYS
    {"url": "https://news.ycombinator.com/rss", "category": "TECH", "source": "Hacker News"},
    {"url": "https://www.reddit.com/r/technology/top/.rss?t=day", "category": "TECH", "source": "r/Technology"},
    {"url": "https://www.theverge.com/rss/index.xml", "category": "TECH", "source": "The Verge"},
    
    # AI & MODELS
    {"url": "https://hnrss.org/frontpage?q=AI", "category": "AI", "source": "HN Artificial Intelligence"},
    {"url": "https://www.reddit.com/r/MachineLearning/top/.rss?t=day", "category": "AI", "source": "r/MachineLearning"},
    
    # OPEN SOURCE & DEV
    {"url": "https://hnrss.org/newest?q=Python", "category": "DEV", "source": "Python News"},
    {"url": "https://github.blog/all.atom", "category": "DEV", "source": "GitHub Blog"},
    {"url": "https://dev.to/feed", "category": "DEV", "source": "DEV Community"},
    
    # GLOBAL & MARKETS
    {"url": "https://techcrunch.com/feed/", "category": "MARKETS", "source": "TechCrunch"},
    {"url": "https://cointelegraph.com/rss", "category": "MARKETS", "source": "Crypto/Markets"}
]

def fetch_trends():
    trends = []
    id_counter = 1
    
    for feed in FEEDS:
        try:
            # Parse the RSS feed
            parsed = feedparser.parse(feed["url"])
            
            # INCREASED LIMIT: Now pulls up to 15 top stories per feed (was 4)
            for entry in parsed.entries[:15]: 
                # Clean up the summary text
                summary = entry.get("summary", "")
                if "<" in summary: # Strip basic HTML tags if present
                    summary = summary.split("<")[0]
                if len(summary) > 120:
                    summary = summary[:120] + "..."
                    
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
            
    # Overwrite the whiteboard file (trends.json)
    with open("trends.json", "w") as f:
        json.dump(trends, f, indent=4)
    print(f"Successfully harvested {len(trends)} signals.")

if __name__ == "__main__":
    fetch_trends()
