import os
import json
import ssl
import hashlib
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

TMP_DIR = ".tmp"
OUTPUT_FILE = os.path.join(TMP_DIR, "raw_feeds.json")
TIMEOUT = 6  # 6-second HTTP timeout per endpoint

# Bypass SSL certificate validation if local environment lacks root certs
SSL_CONTEXT = ssl._create_unverified_context()

def generate_id(source: str, url: str) -> str:
    return hashlib.sha256(f"{source}:{url}".encode("utf-8")).hexdigest()

def fetch_url(url: str, timeout: int = TIMEOUT) -> str:
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    )
    with urllib.request.urlopen(req, timeout=timeout, context=SSL_CONTEXT) as response:
        return response.read().decode("utf-8", errors="ignore")

def fetch_hn_item(sid: int) -> dict:
    item_url = f"https://hacker-news.firebaseio.com/v0/item/{sid}.json"
    story_json = fetch_url(item_url, timeout=3)
    story = json.loads(story_json)
    if not story or "title" not in story:
        return None
    url = story.get("url", f"https://news.ycombinator.com/item?id={sid}")
    pub_time = datetime.fromtimestamp(
        story.get("time", int(datetime.now(timezone.utc).timestamp())),
        tz=timezone.utc
    ).isoformat()
    
    return {
        "id": generate_id("Hacker News", url),
        "title": story["title"],
        "link": url,
        "source": "Hacker News",
        "published_at": pub_time,
        "summary": f"Score: {story.get('score', 0)} | Comments: {story.get('descendants', 0)}",
        "author": story.get("by", "HN Community")
    }

def parse_hackernews() -> list:
    items = []
    source_name = "Hacker News"
    try:
        top_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        raw_json = fetch_url(top_url, timeout=5)
        story_ids = json.loads(raw_json)[:15]  # Top 15 stories
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_id = {executor.submit(fetch_hn_item, sid): sid for sid in story_ids}
            for future in as_completed(future_to_id):
                try:
                    res = future.result()
                    if res:
                        items.append(res)
                except Exception as e:
                    pass
    except Exception as e:
        print(f"[ERROR] Failed fetching Hacker News: {e}")
    return items

def parse_rss(url: str, source_name: str) -> list:
    items = []
    try:
        raw_xml = fetch_url(url, timeout=TIMEOUT)
        root = ET.fromstring(raw_xml)
        
        channel = root.find("channel")
        if channel is not None:
            for elem in channel.findall("item")[:10]:
                title = elem.findtext("title", "").strip()
                link = elem.findtext("link", "").strip()
                pub_date = elem.findtext("pubDate", "")
                description = elem.findtext("description", "").strip()
                author = elem.findtext("dc:creator", "") or elem.findtext("author", source_name)
                
                if not title or not link:
                    continue
                    
                pub_iso = datetime.now(timezone.utc).isoformat()
                if pub_date:
                    try:
                        from email.utils import parsedate_to_datetime
                        dt = parsedate_to_datetime(pub_date)
                        pub_iso = dt.isoformat()
                    except Exception:
                        pass
                
                items.append({
                    "id": generate_id(source_name, link),
                    "title": title,
                    "link": link,
                    "source": source_name,
                    "published_at": pub_iso,
                    "summary": description[:300] if description else title,
                    "author": author or source_name
                })
        else:
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall("atom:entry", ns)[:10]:
                title = entry.findtext("atom:title", "", ns).strip()
                link_elem = entry.find("atom:link", ns)
                link = link_elem.attrib.get("href", "") if link_elem is not None else ""
                published = entry.findtext("atom:published", "", ns) or entry.findtext("atom:updated", "", ns)
                summary = entry.findtext("atom:summary", "", ns).strip()
                author = entry.findtext("atom:author/atom:name", source_name, ns)

                if not title or not link:
                    continue
                    
                items.append({
                    "id": generate_id(source_name, link),
                    "title": title,
                    "link": link,
                    "source": source_name,
                    "published_at": published or datetime.now(timezone.utc).isoformat(),
                    "summary": summary[:300] if summary else title,
                    "author": author
                })
    except Exception as e:
        print(f"[ERROR] Failed fetching RSS from {source_name} ({url}): {e}")
    return items

def main():
    os.makedirs(TMP_DIR, exist_ok=True)
    all_items = []
    
    print("--- Phase 2: Link Feed Ingestion Starting ---")
    
    # 1. Hacker News
    hn_items = parse_hackernews()
    print(f"[{'SUCCESS' if hn_items else 'FAIL'}] Hacker News: Fetched {len(hn_items)} items")
    all_items.extend(hn_items)
    
    # 2. arXiv CS.AI
    arxiv_items = parse_rss("https://rss.arxiv.org/rss/cs.AI", "arXiv AI")
    if not arxiv_items:
        # Fallback arXiv endpoint if main RSS times out
        arxiv_items = parse_rss("https://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=10&sortBy=submittedDate&sortOrder=descending", "arXiv AI")
    print(f"[{'SUCCESS' if arxiv_items else 'FAIL'}] arXiv AI: Fetched {len(arxiv_items)} items")
    all_items.extend(arxiv_items)
    
    # 3. TechCrunch AI
    tc_items = parse_rss("https://techcrunch.com/category/artificial-intelligence/feed/", "TechCrunch AI")
    print(f"[{'SUCCESS' if tc_items else 'FAIL'}] TechCrunch AI: Fetched {len(tc_items)} items")
    all_items.extend(tc_items)
    
    # Save output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_items, f, indent=2)
        
    print(f"\n[COMPLETE] Saved total {len(all_items)} raw feed items to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
