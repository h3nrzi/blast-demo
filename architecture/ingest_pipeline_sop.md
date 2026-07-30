# Standard Operating Procedure (SOP): Data Ingestion & Categorization Pipeline

## 1. Overview
This SOP defines the technical contract, data flow, and error handling for fetching raw AI news feeds, classifying them into standard categories, calculating estimated reading time, and outputting a structured payload for the frontend dashboard.

---

## 2. Pipeline Execution Steps

```
[ Public Feeds ] 
      │ (HackerNews, arXiv, TechCrunch)
      ▼
┌───────────────────────────────────────────┐
│ tools/fetch_rss_raw.py                    │
│ - 6s Timeout, Fail-Fast                   │
│ - Output: .tmp/raw_feeds.json             │
└───────────────────────────────────────────┘
      │
      ▼
┌───────────────────────────────────────────┐
│ tools/categorize_articles.py              │
│ - Multi-keyword Taxonomy Classifier       │
│ - Read Time Calculator                    │
│ - Bookmark State Preserver                │
│ - Output: .tmp/processed_dashboard_payload.json
└───────────────────────────────────────────┘
```

---

## 3. Data Transformation Specification

### Input Schema
Expects array of `RawFeedItem` objects from `.tmp/raw_feeds.json`:
- `id` (SHA256 string)
- `title` (string)
- `link` (URI)
- `source` (string)
- `published_at` (ISO date-time)
- `summary` (string)
- `author` (string)

### Categorization Taxonomy Rules
Articles are evaluated against keyword dictionaries in order:
1. `LLMs & Foundation Models`: `gpt`, `claude`, `gemini`, `llama`, `transformer`, `llm`, `language model`, `prompt`, `fine-tuning`, `reasoning model`, `deepseek`, `mistral`, `gemma`, `kimi`
2. `Computer Vision`: `vision`, `diffusion`, `midjourney`, `image`, `video`, `nerf`, `3d`, `perception`, `spatial`, `segmentation`
3. `AI Tools & Frameworks`: `tool`, `framework`, `agent`, `langchain`, `pytorch`, `tensorflow`, `vector db`, `rag`, `engine`, `open-source`, `copilot`, `code`
4. `Research & Ethics`: `paper`, `arxiv`, `research`, `benchmark`, `governance`, `alignment`, `safety`, `ethics`, `deception`, `evaluation`
5. `Industry News`: (Fallback category for company funding, acquisitions, hardware, startups)

### Output Schema Compliance
Outputs `ProcessedDashboardPayload` to `.tmp/processed_dashboard_payload.json`:
- `articles`: Array of categorized article cards containing `category`, `read_time`, `is_bookmarked`, `fetched_at`.
- `metadata`: `total_count`, `categories` array, `last_updated` ISO timestamp.

---

## 4. Error Handling & Self-Annealing
- **Missing File Failure**: If `.tmp/raw_feeds.json` does not exist or is malformed, `categorize_articles.py` returns an empty array with zero-state metadata instead of raising an unhandled exception.
- **Bookmark State Persistence**: Preserves `is_bookmarked` flags from `.tmp/bookmarks.json` if present.
