import os
import json
import sys

BOOKMARKS_FILE = os.path.join(".tmp", "bookmarks.json")
PAYLOAD_FILE = os.path.join(".tmp", "processed_dashboard_payload.json")

def load_bookmarks() -> list:
    if os.path.exists(BOOKMARKS_FILE):
        try:
            with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def save_bookmarks(bookmarks: list):
    os.makedirs(os.path.dirname(BOOKMARKS_FILE), exist_ok=True)
    with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
        json.dump(bookmarks, f, indent=2)

def toggle_bookmark(article_id: str) -> bool:
    bookmarks = set(load_bookmarks())
    if article_id in bookmarks:
        bookmarks.remove(article_id)
        is_bookmarked = False
    else:
        bookmarks.add(article_id)
        is_bookmarked = True
        
    save_bookmarks(list(bookmarks))

    # Sync into processed_dashboard_payload.json if present
    if os.path.exists(PAYLOAD_FILE):
        try:
            with open(PAYLOAD_FILE, "r", encoding="utf-8") as f:
                payload = json.load(f)
            for art in payload.get("articles", []):
                if art["id"] == article_id:
                    art["is_bookmarked"] = is_bookmarked
            with open(PAYLOAD_FILE, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2)
        except Exception as e:
            print(f"[WARN] Failed syncing bookmark to payload: {e}")

    return is_bookmarked

def main():
    if len(sys.argv) > 1:
        art_id = sys.argv[1]
        state = toggle_bookmark(art_id)
        print(json.dumps({"article_id": art_id, "is_bookmarked": state}))
    else:
        print(json.dumps({"bookmarks": load_bookmarks()}))

if __name__ == "__main__":
    main()
