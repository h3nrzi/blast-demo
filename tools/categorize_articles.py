import os
import json
import re
from datetime import datetime, timezone

RAW_FILE = os.path.join(".tmp", "raw_feeds.json")
BOOKMARKS_FILE = os.path.join(".tmp", "bookmarks.json")
OUTPUT_FILE = os.path.join(".tmp", "processed_dashboard_payload.json")

CATEGORIES = [
    "LLMs & Foundation Models",
    "Computer Vision",
    "AI Tools & Frameworks",
    "Research & Ethics",
    "Industry News"
]

TAXONOMY = {
    "LLMs & Foundation Models": [
        r"\bllm\b", r"\bllms\b", r"\bgpt\b", r"\bclaude\b", r"\bgemini\b", r"\bllama\b",
        r"\btransformer\b", r"\blanguage model\b", r"\bprompt\b", r"\bfine-tuning\b",
        r"\breasoning model\b", r"\bdeepseek\b", r"\bmistral\b", r"\bgemma\b", r"\bkimi\b",
        r"\battention\b", r"\bcontext window\b"
    ],
    "Computer Vision": [
        r"\bvision\b", r"\bdiffusion\b", r"\bmidjourney\b", r"\bimage\b", r"\bvideo\b",
        r"\bnerf\b", r"\b3d\b", r"\bperception\b", r"\bspatial\b", r"\bsegmentation\b",
        r"\bmultimodal\b", r"\bgenerative image\b"
    ],
    "AI Tools & Frameworks": [
        r"\btool\b", r"\btools\b", r"\bframework\b", r"\bagent\b", r"\bagents\b",
        r"\blangchain\b", r"\bpytorch\b", r"\btensorflow\b", r"\bvector db\b", r"\brag\b",
        r"\bengine\b", r"\bopen-source\b", r"\bcopilot\b", r"\bcode\b", r"\bcoding\b",
        r"\brtl\b", r"\bskill\b", r"\bfirmware\b", r"\bapi\b", r"\bapp\b"
    ],
    "Research & Ethics": [
        r"\bpaper\b", r"\barxiv\b", r"\bresearch\b", r"\bbenchmark\b", r"\bgovernance\b",
        r"\balignment\b", r"\bsafety\b", r"\bethics\b", r"\bdeception\b", r"\bevaluation\b",
        r"\bprobing\b", r"\bprobing\b", r"\bstudy\b", r"\bbarely publishing\b"
    ]
}

def load_bookmarks() -> set:
    if os.path.exists(BOOKMARKS_FILE):
        try:
            with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data)
        except Exception:
            pass
    return set()

def classify_text(title: str, summary: str) -> str:
    combined = f"{title} {summary}".lower()
    
    for category, patterns in TAXONOMY.items():
        for pattern in patterns:
            if re.search(pattern, combined):
                return category
                
    return "Industry News"

def calculate_read_time(title: str, summary: str) -> str:
    words = len(f"{title} {summary}".split())
    minutes = max(1, round(words / 40))  # approx reading speed for summary snippets
    return f"{minutes} min read"

def main():
    if not os.path.exists(RAW_FILE):
        print(f"[WARN] {RAW_FILE} not found. Creating empty payload.")
        raw_items = []
    else:
        with open(RAW_FILE, "r", encoding="utf-8") as f:
            raw_items = json.load(f)

    bookmarks = load_bookmarks()
    processed_articles = []
    now_iso = datetime.now(timezone.utc).isoformat()

    for item in raw_items:
        title = item.get("title", "")
        summary = item.get("summary", "")
        article_id = item.get("id", "")
        
        category = classify_text(title, summary)
        read_time = calculate_read_time(title, summary)
        is_bookmarked = article_id in bookmarks

        processed_articles.append({
            "id": article_id,
            "title": title,
            "url": item.get("link", ""),
            "source": item.get("source", "Unknown"),
            "published_at": item.get("published_at", now_iso),
            "category": category,
            "summary": summary,
            "read_time": read_time,
            "is_bookmarked": is_bookmarked,
            "fetched_at": now_iso
        })

    payload = {
        "articles": processed_articles,
        "metadata": {
            "total_count": len(processed_articles),
            "categories": CATEGORIES,
            "last_updated": now_iso
        }
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"[SUCCESS] Categorized {len(processed_articles)} articles into {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
