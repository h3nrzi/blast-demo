# Standard Operating Procedure (SOP): Dashboard UI Architecture

## 1. Overview
This SOP defines the visual interface standards, component hierarchy, and interactivity guidelines for the AI News & Article Dashboard.

---

## 2. Core Aesthetic Principles
- **Modern Dark Theme**: Deep Slate `#0f172a` canvas, `#1e293b` card surfaces, `#334155` borders.
- **Accent Palette**: Indigo `#6366f1` (Primary active), Cyan `#06b6d4` (Highlights/Tags), Emerald `#10b981` (Success/Bookmark active).
- **Typography**: Clean sans-serif hierarchy (Inter / System UI), distinct font weights (600 headings, 400 body text).
- **Zero Clutter**: High contrast, subtle glassmorphism cards, micro-animations on hover, smooth pill transitions.

---

## 3. UI Component Breakdown
1. **Header Component**: Brand title ("AI News Radar / BLAST"), Live Refresh button, Last Updated timestamp badge.
2. **Category Filter Bar**: Dynamic pill buttons (`All`, `LLMs & Foundation Models`, `Computer Vision`, `AI Tools & Frameworks`, `Research & Ethics`, `Industry News`, `Bookmarked`).
3. **Search & Sort Bar**: Real-time title/summary text search and sorting by date or popularity/score.
4. **Article Card Grid**:
   - Source tag badge (Hacker News, arXiv AI, TechCrunch AI)
   - Category pill
   - Title link (opens in new tab)
   - Summary snippet
   - Footer metadata: Author, Published time (relative: "2 hours ago"), Read time (e.g., "3 min read")
   - Interactive Bookmark toggle button (heart / bookmark icon).

---

## 4. State Management Contract
- Frontend reads `.tmp/processed_dashboard_payload.json` via local dev server API endpoint `/api/articles`.
- Bookmarks toggle makes POST request to `/api/bookmark` which updates local state and persists to `.tmp/bookmarks.json`.
