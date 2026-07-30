# AI News Radar (B.L.A.S.T. Master System)

An automated, self-healing AI News & Article Dashboard built strictly following the **B.L.A.S.T.** (Blueprint, Link, Architect, Stylize, Trigger) protocol and **A.N.T.** (Architecture, Navigation, Tools) 3-layer architecture.

---

## 🌟 Features
- **Multi-Source Aggregation**: Ingests trending AI news concurrently from Hacker News, arXiv AI, and TechCrunch AI.
- **Automated Taxonomy Categorization**: Classifies articles into 5 distinct categories:
  - `LLMs & Foundation Models`
  - `Computer Vision`
  - `AI Tools & Frameworks`
  - `Research & Ethics`
  - `Industry News`
- **Sleek Glassmorphism Dashboard**: Modern dark theme with dynamic category pills, instant search, relative date formatting, and interactive bookmarking.
- **Fail-Fast & Resilient**: Built-in 6-second HTTP timeouts, thread-pooled concurrent fetching, fallback endpoints, and unverified SSL context handling for zero-crash stability.

---

## 🏗️ A.N.T. 3-Layer Architecture

```
blast-demo/
├── architecture/                     # LAYER 1: Technical SOPs (Golden Rule)
│   ├── ingest_pipeline_sop.md        # Data pipeline contract & taxonomy rules
│   └── dashboard_ui_sop.md           # Visual design system & UI state contract
│
├── main.py                           # LAYER 2: Navigation Layer (Orchestration)
│
├── tools/                            # LAYER 3: Atomic Execution Tools
│   ├── fetch_rss_raw.py              # Single-purpose raw feed ingestion
│   ├── categorize_articles.py        # Keyword classification & payload formatter
│   └── store_bookmarks.py            # Local bookmark toggle persistence
│
├── public/                           # STYLIZE: Web Frontend Application
│   ├── index.html                    # Dashboard markup & Google Fonts
│   ├── styles.css                    # Dark glassmorphism CSS design system
│   └── app.js                        # Frontend state & API integration engine
│
├── server.py                         # Local Python HTTP server & API gateway
├── gemini.md                         # B.L.A.S.T. Source of Truth & Project Map
├── task_plan.md                      # Phase execution checklist
└── findings.md                       # Feed research & taxonomy rules
```

---

## 🚀 Quickstart Guide

### Prerequisites
- Python 3.8+ (No external third-party dependencies required!)

### 1. Launch the Server & Dashboard
```bash
python3 server.py
```

Open your browser and navigate to:
👉 **`http://localhost:8080`**

### 2. Manual Pipeline Execution
To execute the raw ingestion and categorization pipeline directly from the command line:
```bash
python3 main.py
```

---

## 📡 API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/` | `GET` | Serves the web dashboard UI |
| `/api/articles` | `GET` | Returns processed article cards and metadata JSON |
| `/api/bookmark` | `POST` | Toggles bookmark state for an article ID |
| `/api/refresh` | `POST` | Triggers `main.py` pipeline re-fetch and updates payload |

---

## 📊 Data Schema Governance

### Processed Output Payload (`.tmp/processed_dashboard_payload.json`)
```json
{
  "articles": [
    {
      "id": "7b9c5f12ff2690744846c23228a4f9c739e1a837b4d2566678f974f2dcfabf7e",
      "title": "Superlogical",
      "url": "https://www.superlogical.com/",
      "source": "Hacker News",
      "published_at": "2026-07-29T15:41:33+00:00",
      "category": "Industry News",
      "summary": "Score: 694 | Comments: 409",
      "read_time": "1 min read",
      "is_bookmarked": false,
      "fetched_at": "2026-07-30T09:24:50.709403+00:00"
    }
  ],
  "metadata": {
    "total_count": 35,
    "categories": [
      "LLMs & Foundation Models",
      "Computer Vision",
      "AI Tools & Frameworks",
      "Research & Ethics",
      "Industry News"
    ],
    "last_updated": "2026-07-30T09:24:50.709403+00:00"
  }
}
```

---

## 🛡️ License
Built using the **B.L.A.S.T. Master System** deterministic automation protocol.
