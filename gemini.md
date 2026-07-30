# B.L.A.S.T. Project Map & Source of Truth

## Project Info
- **Skill:** `mar2181-spifunrentalsmarketingplan2026-blast-master`
- **Protocol Phase:** Phase 1: Blueprint (Discovery Complete & Schema Approval Pending)
- **Status:** Blueprint Locked. Data Schemas submitted for CTO Review before Phase 2.

---

## 1. Discovery (North Star Blueprint)
1. **North Star Outcome:** Build a clean, responsive web dashboard that fetches, categorizes, and displays top trending AI news/articles from public RSS feeds and tech sources, allowing users to bookmark items.
2. **Integrations & Credentials:** Public RSS/JSON feeds (e.g., HackerNews, RSS feeds, tech news). Standard Node.js / Python HTTP clients. No private API keys required for initial MVP phase.
3. **Source of Truth:** Scraped public RSS/web feeds saved into local structured JSON / SQLite database (`.tmp/articles_db.json`).
4. **Delivery Payload:** An interactive React/HTML dashboard running on Localhost (with article cards, category filters, search, and bookmarking capability).
5. **Behavioral Rules:**
   - Strict Fail-Fast on network errors and malformed feed responses.
   - Clean, modern UI layout with dynamic styling, vibrant subtle aesthetics, and zero cluttered text.
   - All tools built in `tools/` must be single-purpose, atomic scripts with JSON input/output schemas.

---

## 2. Data Schema Governance

### A. Input Data Schema (`raw_feed_item.json`)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "RawFeedItem",
  "type": "object",
  "required": ["id", "title", "link", "source", "published_at"],
  "properties": {
    "id": { "type": "string", "description": "Unique SHA256 identifier based on source and URL" },
    "title": { "type": "string" },
    "link": { "type": "string", "format": "uri" },
    "source": { "type": "string" },
    "published_at": { "type": "string", "format": "date-time" },
    "summary": { "type": "string" },
    "author": { "type": "string" }
  }
}
```

### B. Output Data Schema (`processed_dashboard_payload.json`)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ProcessedDashboardPayload",
  "type": "object",
  "required": ["articles", "metadata"],
  "properties": {
    "articles": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "title", "url", "source", "published_at", "category", "summary", "read_time", "is_bookmarked"],
        "properties": {
          "id": { "type": "string" },
          "title": { "type": "string" },
          "url": { "type": "string", "format": "uri" },
          "source": { "type": "string" },
          "published_at": { "type": "string", "format": "date-time" },
          "category": { "type": "string", "enum": ["LLMs & Foundation Models", "Computer Vision", "AI Tools & Frameworks", "Research & Ethics", "Industry News"] },
          "summary": { "type": "string" },
          "read_time": { "type": "string" },
          "is_bookmarked": { "type": "boolean" },
          "fetched_at": { "type": "string", "format": "date-time" }
        }
      }
    },
    "metadata": {
      "type": "object",
      "required": ["total_count", "categories", "last_updated"],
      "properties": {
        "total_count": { "type": "integer" },
        "categories": { "type": "array", "items": { "type": "string" } },
        "last_updated": { "type": "string", "format": "date-time" }
      }
    }
  }
}
```

---

## 3. Maintenance & Handoff Log
- **2026-07-30:** Initialized `gemini.md` per B.L.A.S.T. Protocol 0. Installed skill `mar2181-spifunrentalsmarketingplan2026-blast-master`.
- **2026-07-30:** Phase 1 Discovery complete. Locked North Star Blueprint and specified Input/Output JSON Schemas. Created `task_plan.md` and `findings.md`. Awaiting CTO Schema Approval before Phase 2.
