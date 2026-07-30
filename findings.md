# B.L.A.S.T. Findings & Knowledge Base

## Research & Integration Findings

### Target Feed Sources (Public / Key-less)
1. **Hacker News Firebase API (`https://hacker-news.firebaseio.com/v0/`)**:
   - Endpoint: `topstories.json` / `item/{id}.json`
   - Data structure: High reliability JSON format with title, url, score, time, by.
2. **arXiv CS.AI RSS Feed (`http://export.arxiv.org/rss/cs.AI`)**:
   - Format: Standard XML/RSS 2.0 or Atom.
   - Ideal for research & paper updates.
3. **TechCrunch AI Feed (`https://techcrunch.com/category/artificial-intelligence/feed/`)**:
   - Format: Standard RSS 2.0 XML with full title, pubDate, category, and link.

### Architectural Decisions
- **Data Persistence**: `.tmp/articles_db.json` used as local cache / store for quick iteration.
- **Fail-Fast Mechanism**: `fetch_rss_raw.py` will implement a 5-second HTTP timeout and validate JSON output against `raw_feed_item.json` schema. Any broken feed will log a warning and return empty array without crashing the pipeline.
- **Categorization Rule Engine**: Keyword-based classification into 5 distinct categories:
  1. `LLMs & Foundation Models` (GPT, Claude, Gemini, Llama, Transformer, Fine-tuning, Prompt)
  2. `Computer Vision` (Vision, Diffusion, Midjourney, Image, Video, NeRF)
  3. `AI Tools & Frameworks` (LangChain, PyTorch, TensorFlow, Agent, Vector DB, RAG)
  4. `Research & Ethics` (Paper, arXiv, Governance, Alignment, Benchmark, Safety)
  5. `Industry News` (OpenAI, Anthropic, Google, NVIDIA, Funding, Startup)

### Design & Aesthetic Guidelines
- Modern sleek dark mode palette (Slate/Zinc neutral dark `#0f172a`, vibrant indigo/cyan accents `#6366f1` / `#06b6d4`).
- Inter/Outfit typography, glassmorphism cards with smooth hover animations.
- Interactive category tabs and real-time bookmark toggle state.
