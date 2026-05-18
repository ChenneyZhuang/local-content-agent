# Local Content Agent

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**An AI agent that generates a month of Facebook posts for local businesses — complete with brand voice analysis, industry research, drafting, and human-ready editing.**

> Built for small businesses, tradies, cafés, clinics, and real estate agents.  
> Human-in-the-loop by design — the agent prepares content, you review and publish.

## What It Does

```
Business Name + Website
        │
        ▼
  ┌─────────────────┐
  │ 1. Brand Voice   │ ← DeepSeek (analyses real website content)
  ├─────────────────┤
  │ 2. Topic Ideas   │ ← 8 monthly topics, 4 content types
  ├─────────────────┤
  │ 3. Research      │ ← Perplexity Pro (or web search fallback)
  ├─────────────────┤
  │ 4. Draft         │ ← DeepSeek (from research + brand voice)
  ├─────────────────┤
  │ 5. Polish        │ ← DeepSeek (humanisation pass)
  ├─────────────────┤
  │ 6. Calendar      │ ← Content calendar ready for scheduling
  └─────────────────┘
        │
        ▼
  8 Facebook posts + content calendar
```

## Quick Start

```bash
# Install
git clone https://github.com/ChenneyZhuang/local-content-agent.git
cd local-content-agent
pip install -e .

# Set your API key
export DEEPSEEK_API_KEY="sk-..."

# Generate posts for a business
lca run "Brett's Automotive" --website https://brettwillard.com
```

## Features

- **6-step AI pipeline** — Brand Voice → Topics → Research → Draft → Polish → Calendar
- **Two research backends** — Perplexity Pro (deep research) or web search (free fallback)
- **Human-in-the-loop** — Every post goes through research → draft → polish stages for review
- **Local-first design** — Canberra-aware search, Australian business context
- **Pydantic-validated output** — Structured JSON output at every stage
- **Batch mode** — Generate content for multiple businesses at once

## Architecture

```
src/lca/
├── cli.py              # CLI entry point (lca command)
├── pipeline.py         # Orchestrator: runs the 6-step pipeline
├── config.py           # Configuration from env vars
├── agents/
│   ├── brand_voice.py  # Step 1: Analyse brand voice from website
│   ├── topics.py       # Step 2: Generate 8 monthly topics
│   ├── researcher.py   # Step 3: Research + outline via Perplexity/web
│   ├── drafter.py      # Step 4: Draft post from research
│   └── polisher.py     # Step 5: Humanise and polish
├── models/
│   └── schemas.py      # Pydantic models for each stage
└── tools/
    ├── llm.py           # LLM API client (DeepSeek / OpenAI-compatible)
    ├── web_search.py    # DuckDuckGo search + content extraction
    └── website.py       # Scrape website content for analysis
```

## Output Structure

```
output/Bretts_Automotive/
├── brand_voice.md
├── topic_list.md
├── content_calendar.md
├── topic_01_how_to_prepare_your_car_for_winter/
│   ├── research_outline.md
│   ├── draft_post.md
│   └── final_post.md
├── topic_02_why_lpg_certificates_matter/
│   └── ...
└── topic_08_king_s_birthday_safety_tips/
    └── ...
```

## Tech Stack

- **LLM:** DeepSeek API (OpenAI-compatible, swap to any provider)
- **Research:** Perplexity Pro (browser automation via Playwright) or DuckDuckGo web search
- **Validation:** Pydantic v2
- **Python:** 3.11+

## License

MIT — free for personal and commercial use.

---

*Built with ❤️ in Canberra, Australia*
