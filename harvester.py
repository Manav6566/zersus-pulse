import feedparser
import json
from datetime import datetime

# The free RSS feeds we are monitoring
FEEDS = [
    {"url": "https://news.ycombinator.com/rss", "category": "TECH", "source": "Hacker News"},
    {"url": "https://hnrss.org/frontpage?q=AI", "category": "AI", "source": "HN Artificial Intelligence"},
    {"url": "https://techcrunch.com/feed/", "category": "MARKETS", "source": "TechCrunch"}
]

def fetch_trends():
    trends = []
    id_counter = 1
    
    for feed in FEEDS:
        # Parse the RSS feed
        parsed = feedparser.parse(feed["url"])
        
        # Grab only the top 4 stories from each feed
        for entry in parsed.entries[:4]: 
            # Clean up the summary text
            summary = entry.get("summary", "")
            if "<" in summary: # Strip basic HTML tags if present
                summary = summary.split("<")[0]
            if len(summary) > 120:
                summary = summary[:120] + "..."
                
            trends.append({
                "id": id_counter,
                "title": entry.title,
                "summary": summary if summary else "No summary provided by source.",
                "category": feed["category"],
                "source": feed["source"],
                "url": entry.link,
                "timestamp": datetime.now().strftime("%H:%M UTC")
            })
            id_counter += 1
            
    # Overwrite the whiteboard file (trends.json)
    with open("trends.json", "w") as f:
        json.dump(trends, f, indent=4)
    print(f"Successfully harvested {len(trends)} signals.")

if __name__ == "__main__":
    fetch_trends()
