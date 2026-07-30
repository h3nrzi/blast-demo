# B.L.A.S.T. Task Plan

## Project Overview
Building a clean, responsive AI News & Article Dashboard using public RSS feeds, atomic ingest scripts, and a modern local web UI.

---

## Phase Status Checklist

### Phase 1: Blueprint (Vision & Logic)
- [x] 1.1 Complete 5 Discovery North Star Questions
- [x] 1.2 Formulate Input & Output JSON Schemas (`raw_feed_item.json`, `processed_dashboard_payload.json`)
- [x] 1.3 Create `gemini.md`, `task_plan.md`, and `findings.md`
- [x] 1.4 Submit Schemas for CTO Approval (APPROVED)

### Phase 2: Link (Connectivity & Handshake Verification)
- [x] 2.1 Verify public RSS feed endpoints (HackerNews API, arXiv AI RSS, TechCrunch AI RSS)
- [x] 2.2 Build atomic handshake tool in `tools/fetch_rss_raw.py` to test feed connectivity and fail-fast handling
- [x] 2.3 Store test payload samples in `.tmp/raw_feeds.json` (35 items fetched successfully)

### Phase 3: Architect (A.N.T. 3-Layer Build)
- [ ] 3.1 **Layer 1 (Architecture)**: Write `architecture/ingest_pipeline_sop.md` and `architecture/dashboard_ui_sop.md`
- [ ] 3.2 **Layer 3 (Tools)**: Build single-purpose atomic tools:
  - `tools/fetch_rss_raw.py`: Fetch & validate RSS/JSON feeds
  - `tools/categorize_articles.py`: Categorize & clean articles into standard categories
  - `tools/store_bookmarks.py`: Persist and toggle user bookmarks
- [ ] 3.3 **Layer 2 (Navigation)**: Build main orchestration entry point `main.py` / `server.js`

### Phase 4: Stylize (UI & Aesthetics)
- [ ] 4.1 Build modern, dynamic Web Dashboard interface (HTML/CSS/JS or Vite React)
- [ ] 4.2 Add sleek dark mode, vibrant accent colors, smooth micro-animations, category pill filters, search bar, and bookmark toggles
- [ ] 4.3 Verify zero text clutter and responsive layout across desktop and mobile viewports

### Phase 5: Trigger (Deployment & Automation)
- [ ] 5.1 Configure dev server startup & automatic feed refresh trigger
- [ ] 5.2 Validate end-to-end self-healing and error handling
- [ ] 5.3 Complete final maintenance & handoff log in `gemini.md`
