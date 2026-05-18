# 🏪 Local Content Agent

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status: Alpha](https://img.shields.io/badge/Status-Alpha-orange.svg)](https://github.com/ChenneyZhuang/local-content-agent)

**An AI agent that generates a full month of Facebook posts for local businesses — complete with brand voice analysis, web research, drafting, and human-style polishing.**

> Built for small businesses, tradies, cafés, clinics, real estate agents, and anyone who needs authentic local social media content without the marketing agency price tag.
> Human-in-the-loop by design — the agent prepares everything, you review and publish.

---

## 📑 Table of Contents

- [What It Does](#-what-it-does)
- [Key Features](#-key-features)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Detailed Usage](#-detailed-usage)
  - [CLI Commands](#cli-commands)
  - [Python API](#python-api)
  - [Environment Variables](#environment-variables)
  - [Batch Mode](#batch-mode)
- [Output Structure](#-output-structure)
- [Architecture](#-architecture)
- [How It Works](#-how-it-works)
  - [Step 1: Find Business Links](#step-1-find-business-links)
  - [Step 2: Analyse Brand Voice](#step-2-analyse-brand-voice)
  - [Step 3: Generate Topics](#step-3-generate-topics)
  - [Step 4: Research](#step-4-research)
  - [Step 5: Draft](#step-5-draft)
  - [Step 6: Polish](#step-6-polish)
  - [Content Calendar](#content-calendar)
- [Configuration](#-configuration)
- [Pydantic Data Models](#-pydantic-data-models)
- [FAQ / Troubleshooting](#-faq--troubleshooting)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 What It Does

You give it a business name (and optionally a website URL). The agent:

1. **Finds** the business website and Facebook page (if not provided)
2. **Analyses** the brand voice by reading the actual website
3. **Generates** 8 monthly Facebook post topics tailored to the business
4. **Researches** each topic using web search + DeepSeek AI
5. **Drafts** each post in the brand's voice
6. **Polishes** each draft to sound natural and human

The result: 8 ready-to-post Facebook entries plus a content calendar — all in a single command.

```
                          ┌──────────────────────┐
                          │  Business Name       │
                          │  (e.g. "Joe's Café") │
                          └──────────┬───────────┘
                                     │
                                     ▼
                   ┌─────────────────────────────────┐
                   │  STEP 1: Find Business Links    │
                   │  Web search → website + FB page  │
                   │  (DuckDuckGo / websearch pkg)    │
                   └────────────────┬────────────────┘
                                    │
                                    ▼
                   ┌─────────────────────────────────┐
                   │  STEP 2: Analyse Brand Voice    │
                   │  Scrapes website → LLM analysis  │
                   │  → BrandVoice.md                 │
                   └────────────────┬────────────────┘
                                    │
                                    ▼
                   ┌─────────────────────────────────┐
                   │  STEP 3: Generate Topics         │
                   │  8 monthly topics, 4 categories  │
                   │  → topic_list.md                 │
                   └────────────────┬────────────────┘
                                    │
                         ┌──────────┴──────────┐
                         │   For each topic:   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                   ┌─────────────────────────────────┐
                   │  STEP 4: Research               │
                   │  Web search + LLM outline        │
                   │  → research_outline.md           │
                   └────────────────┬────────────────┘
                                    │
                                    ▼
                   ┌─────────────────────────────────┐
                   │  STEP 5: Draft                  │
                   │  LLM drafts full Facebook post   │
                   │  180–220 words, brand-aligned    │
                   │  → draft_post.md                 │
                   └────────────────┬────────────────┘
                                    │
                                    ▼
                   ┌─────────────────────────────────┐
                   │  STEP 6: Polish                 │
                   │  Humanisation pass by LLM        │
                   │  Removes AI clichés              │
                   │  → final_post.md                 │
                   └────────────────┬────────────────┘
                                    │
                                    ▼
                   ┌─────────────────────────────────┐
                   │  Content Calendar               │
                   │  8 posts mapped to weeks/days    │
                   │  → content_calendar.md           │
                   └─────────────────────────────────┘
```

---

## ✨ Key Features

- **6-Step AI Pipeline** — Fully automated from business discovery to polished posts
- **Brand Voice Analysis** — Reads your real website, doesn't make things up
- **Real Web Research** — Searches DuckDuckGo for current, verified information
- **4 Content Types** — Educational Tips, Customer Stories, Festival Greetings, Local Community Engagement
- **Human-Style Polishing** — Dedicated pass to remove AI clichés and corporate stiffness
- **Idempotent by Design** — Re-running skips completed steps; safe to resume after interruption
- **Pydantic-Validated** — Structured data models at every pipeline stage
- **Canberra-Aware** — Australian local business context baked into search and topic generation
- **Batch-Ready** — Run the pipeline programmatically for multiple businesses
- **OpenAI-Compatible** — Swap DeepSeek for any OpenAI-compatible LLM provider
- **Multiple Search Backends** — `websearch` package, local script, or raw DuckDuckGo HTML
- **Resumable Pipeline** — Cached intermediate files; restart from where you left off

---

## 📋 Requirements

| Requirement | Details |
|-------------|---------|
| **Python** | 3.11 or newer |
| **API Key** | DeepSeek API key (or any OpenAI-compatible endpoint) |
| **Operating System** | macOS, Linux, Windows (any platform with Python) |
| **Disk Space** | ~50 MB for the package + output files |
| **Internet** | Required for API calls and web search |

> **Note:** No GPU needed. Everything runs via cloud APIs. A basic laptop is sufficient.

---

## 📦 Installation

### Method 1: Install from Git (Recommended)

```bash
# Clone the repository
git clone https://github.com/ChenneyZhuang/local-content-agent.git
cd local-content-agent

# Install in editable mode (changes to source take effect immediately)
pip install -e .

# Verify installation
lca --help
```

### Method 2: Install with Dev Dependencies

```bash
git clone https://github.com/ChenneyZhuang/local-content-agent.git
cd local-content-agent
pip install -e ".[dev]"
```

### Method 3: Install for Perplexity Pro Research (Optional)

If you have a Perplexity Pro subscription and want deeper research:

```bash
pip install -e ".[dev,perplexity]"
```

This installs Playwright for browser automation. For most users, the free DuckDuckGo-based research is perfectly adequate.

### Verify Everything Works

```bash
# Should print help text
lca --help

# Check Python is accessible
python -c "import lca; print(lca.__version__)"
# Expected: 0.1.0
```

---

## 🚀 Quick Start

### 1. Get a DeepSeek API Key

1. Visit [platform.deepseek.com](https://platform.deepseek.com/)
2. Sign up and navigate to **API Keys**
3. Create a new key and copy it (starts with `sk-`)
4. Set it as an environment variable:

```bash
export DEEPSEEK_API_KEY="sk-your-actual-key-here"
```

> 💡 **Tip:** Add this line to your `~/.zshrc` or `~/.bashrc` so it persists across terminal sessions.

### 2. Run Your First Generation

```bash
lca run "Brett's Automotive" --website https://brettwillard.com
```

**What you'll see:**

```
============================================================
  Local Content Agent
  Business: Brett's Automotive
============================================================

  Step 2: Analysing brand voice...
  Step 3: Generating 8 topics...
  Topic 1/8: How to prepare your car for winter driving...
  Topic 2/8: Why regular LPG system checks save you money...
  Topic 3/8: Meet our senior mechanic — 20 years of stories...
  ...
  Topic 8/8: King's Birthday long weekend road safety tips...
  ✅ Complete: 8 posts → output/Bretts_Automotive
```

### 3. Check Your Output

```bash
ls output/Bretts_Automotive/
# brand_voice.md    topic_list.md    content_calendar.md
# topic_01_.../     topic_02_.../    ...    topic_08_.../

cat output/Bretts_Automotive/topic_01_*/final_post.md
```

### 4. Without a Known Website

If you don't know the business website, the agent can find it for you:

```bash
lca run "Joe's Café Canberra"
# The agent will search DuckDuckGo to find the website and Facebook page
```

---

## 📖 Detailed Usage

### CLI Commands

```bash
# Basic usage — auto-discovers website
lca run "Business Name"

# With known website (faster, more reliable)
lca run "Business Name" --website https://example.com
lca run "Business Name" -w https://example.com

# With both website and Facebook
lca run "Business Name" \
  --website https://example.com \
  --facebook https://facebook.com/BusinessPage
```

#### Full CLI Reference

```
usage: lca run [-h] [--website WEBSITE] [--facebook FACEBOOK] name

Generate content for a business

positional arguments:
  name                  Business name

optional arguments:
  -h, --help            show this help message and exit
  --website WEBSITE, -w WEBSITE
                        Website URL (auto-detected if omitted)
  --facebook FACEBOOK, -f FACEBOOK
                        Facebook page URL
```

### Python API

You can use the pipeline directly in your Python scripts:

```python
from lca.pipeline import run

# Generate a full month of content
result = run(
    business_name="Brett's Automotive",
    website="https://brettwillard.com",
)

# Access structured results
print(f"Business: {result.business.name}")
print(f"Website: {result.business.website}")
print(f"Brand intro: {result.brand_voice.introduction[:100]}...")
print(f"Topics generated: {len(result.topics)}")
print(f"Posts written: {len(result.posts)}")

# Iterate through posts
for post in result.posts:
    print(f"\n--- Post {post.topic_index}: {post.topic_title} ---")
    print(f"Word count: {post.word_count}")
    print(post.content[:200])
```

#### Available Pipeline Result Fields

```python
result.business          # BusinessInfo: name, website, facebook
result.brand_voice       # BrandVoice: introduction, personality, writing_style, ...
result.topics            # list[Topic]: index, title, category
result.posts             # list[FinalPost]: topic_index, topic_title, content, word_count
result.calendar          # ContentCalendar: business_name, month, year, posts
result.generated_at      # datetime: when the pipeline finished
```

#### Using Individual Pipeline Steps

Each step can be called independently:

```python
from lca.agents.brand_voice import find_business
from lca.agents.topics import analyse_brand, generate_topics
from lca.agents.researcher import research_topic
from lca.agents.drafter import draft_post
from lca.agents.polisher import polish_post
from lca.models.schemas import BusinessInfo

# Step 1: Find the business
info = find_business("Brett's Automotive")

# Step 2: Analyse brand voice
brand = analyse_brand("Brett's Automotive", info)

# Step 3: Generate topics
topics = generate_topics("Brett's Automotive", info, brand)

# Steps 4-6: Process a single topic
research = research_topic(
    business_name="Brett's Automotive",
    website=info.website,
    brand_intro=brand.introduction,
    topic_title=topics[0].title,
    topic_index=1,
)
draft = draft_post(brand.raw, research, topics[0].title)
final = polish_post(brand.raw, draft.content, topics[0].title, 1)

print(final.content)
```

### Environment Variables

All configuration is done via environment variables. None are *required* for basic usage (except `DEEPSEEK_API_KEY`).

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DEEPSEEK_API_KEY` | **Yes** | *(none)* | Your DeepSeek API key (starts with `sk-`) |
| `DEEPSEEK_BASE_URL` | No | `https://api.deepseek.com` | API base URL (change for proxies/compatible providers) |
| `LCA_LLM_MODEL` | No | `deepseek-chat` | Model name to use for completions |
| `PERPLEXITY_ENABLED` | No | *(disabled)* | Set to `1`/`true`/`yes` to use Perplexity Pro research |
| `LCA_CDP_URL` | No | `http://localhost:9222` | Chrome DevTools Protocol URL (for Perplexity mode) |
| `LCA_OUTPUT_DIR` | No | `./output` | Directory for generated content |
| `LCA_MAX_TOPICS` | No | `8` | Number of topics to generate (max recommended: 12) |
| `LCA_RESEARCH_TIMEOUT` | No | `300` | Timeout in seconds for research step (per topic) |

#### Using Other LLM Providers

DeepSeek uses an OpenAI-compatible API, so you can swap to any compatible provider:

```bash
# Use OpenAI
export DEEPSEEK_BASE_URL="https://api.openai.com/v1"
export DEEPSEEK_API_KEY="sk-..."
export LCA_LLM_MODEL="gpt-4o"

# Use a local model (e.g., Ollama)
export DEEPSEEK_BASE_URL="http://localhost:11434/v1"
export DEEPSEEK_API_KEY="ollama"  # Ollama doesn't require a real key
export LCA_LLM_MODEL="llama3"
```

### Batch Mode

Process multiple businesses programmatically:

```python
from lca.pipeline import run

businesses = [
    {"name": "Brett's Automotive", "website": "https://brettwillard.com"},
    {"name": "Canberra City Dental", "website": "https://canberracitydental.com.au"},
    {"name": "The Green Grocer Ainslie", "website": None},
]

for biz in businesses:
    try:
        result = run(biz["name"], website=biz["website"])
        print(f"✅ {result.business.name}: {len(result.posts)} posts")
    except Exception as e:
        print(f"❌ {biz['name']}: {e}")
```

---

## 📁 Output Structure

After running, your output directory looks like this:

```
output/
└── Business_Name/
    ├── brand_voice.md          # Full brand voice analysis
    ├── topic_list.md           # All 8 topics with categories
    ├── content_calendar.md     # Posting schedule (week/day mapping)
    │
    ├── topic_01_how_to_prepare_your_car_for_winter/
    │   ├── research_outline.md  # Raw research + structured outline
    │   ├── draft_post.md        # First draft (before polishing)
    │   └── final_post.md        # Polished final version ← ready to post!
    │
    ├── topic_02_why_regular_lpg_checks_save_you_money/
    │   ├── research_outline.md
    │   ├── draft_post.md
    │   └── final_post.md
    │
    ├── topic_03_meet_our_senior_mechanic/
    │   └── ...
    │
    └── topic_08_kings_birthday_safety_tips/
        └── ...
```

### File Purposes

| File | Purpose | Ready to Use? |
|------|---------|---------------|
| `brand_voice.md` | Business description, personality, writing guidelines | Reference only |
| `topic_list.md` | All 8 topics with categories | For review |
| `content_calendar.md` | 4-week posting schedule | For planning |
| `research_outline.md` | Verified facts, hooks, CTA ideas | For fact-checking |
| `draft_post.md` | First draft of the post | For comparison |
| `final_post.md` | **Polished, ready-to-post content** | ✅ **Copy & paste to Facebook!** |

### Resumability

The pipeline is **idempotent** — it skips steps that have already been completed:

- If a file already exists, the step is skipped (no duplicate API calls)
- Safe to interrupt with `Ctrl+C` and re-run — it picks up where it left off
- Delete any intermediate file to force regeneration of that step

```bash
# Re-run from where you left off (skips completed steps)
lca run "Brett's Automotive" --website https://brettwillard.com

# Force regeneration of a specific topic
rm -rf output/Bretts_Automotive/topic_03_*/
lca run "Brett's Automotive" --website https://brettwillard.com
```

---

## 🏗 Architecture

### Project Structure

```
local-content-agent/
│
├── pyproject.toml              # Package metadata, dependencies, CLI entry point
├── README.md                   # You are here
├── LICENSE                     # MIT License
│
└── src/
    └── lca/
        ├── __init__.py          # Package version (0.1.0)
        │
        ├── cli.py              # CLI entry point — `lca run` command
        │                        # Uses argparse, delegates to pipeline.run()
        │
        ├── pipeline.py         # 🧠 Main orchestrator
        │                        # Coordinates all 6 steps, manages output dirs,
        │                        # handles caching/resumability
        │
        ├── config.py           # ⚙️ Environment variable configuration
        │                        # API keys, URLs, limits, output paths
        │
        ├── agents/             # 🤖 AI pipeline steps
        │   ├── brand_voice.py  # Step 1: Find business links via web search
        │   ├── topics.py       # Step 2: Brand voice analysis (website scraping)
        │   │                   # Step 3: Topic generation (8 monthly topics)
        │   ├── researcher.py   # Step 4: Web research + structured outline
        │   ├── drafter.py      # Step 5: Draft Facebook post (180-220 words)
        │   └── polisher.py     # Step 6: Polish / humanise the draft
        │
        ├── models/             # 📐 Pydantic data models
        │   └── schemas.py      # BusinessInfo, BrandVoice, Topic, Research,
        │                        # DraftPost, FinalPost, ContentCalendar, PipelineResult
        │
        └── tools/              # 🔧 Low-level utilities
            ├── llm.py          # LLM API client (OpenAI-compatible)
            │                   # Rate limiting (1.5s between calls)
            │                   # Handles authentication, error reporting
            │
            ├── web_search.py   # Web search with 3-tier fallback
            │                   # 1. websearch Python package (preferred)
            │                   # 2. Local web_search.py script
            │                   # 3. Raw DuckDuckGo HTML scraping
            │
            └── website.py      # Website content fetching
                                # fetch(): scrape + clean HTML → plain text
                                # probe_urls(): guess website from business name
```

### Data Flow

```
CLI (cli.py)
  │
  ▼
Pipeline (pipeline.py)
  │
  ├─► find_business()         ──► web_search.py, website.py
  │
  ├─► analyse_brand()         ──► website.py → fetch() → llm.py → chat()
  │
  ├─► generate_topics()       ──► llm.py → chat()
  │
  ├─► research_topic() ×8     ──► web_search.py → search() → llm.py → chat()
  │
  ├─► draft_post() ×8         ──► llm.py → chat()
  │
  ├─► polish_post() ×8        ──► llm.py → chat()
  │
  └─► ContentCalendar         ──► in-memory assembly
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **LLM** | DeepSeek API (`deepseek-chat`) | AI generation for all steps |
| **Web Search** | DuckDuckGo (via `websearch` package or raw HTML) | Finding businesses and researching topics |
| **Web Scraping** | `urllib.request` + regex | Extracting website text for brand voice analysis |
| **Data Validation** | Pydantic v2 | Structured, type-safe data at every stage |
| **Config** | Environment variables + `pyyaml` | Flexible, 12-factor app style |
| **CLI** | `argparse` (stdlib) | Clean command-line interface |
| **Packaging** | `setuptools` + `pyproject.toml` | Standard Python packaging |

---

## 🔬 How It Works

### Step 1: Find Business Links

**File:** `agents/brand_voice.py` → `find_business()`

The agent discovers the business website and Facebook page if not provided:

1. **Direct URL probe:** Converts business name to a slug (e.g., `brettsautomotive`) and tries `brettsautomotive.com`, `www.brettsautomotive.com`, `brettsautomotive.com.au`, `www.brettsautomotive.com.au`
2. **Canberra search:** Searches DuckDuckGo for `"Business Name" Canberra`, then `"Business Name" ACT Australia`, then `"Business Name" Australia`
3. **Facebook search:** Searches for the Facebook page specifically
4. Returns a `BusinessInfo` object with `name`, `website`, and `facebook` fields

> **Note:** Canberra-first search is hardcoded because the agent was originally built for Australian local businesses. The search queries can be adjusted in the source if you're in a different region.

### Step 2: Analyse Brand Voice

**File:** `agents/topics.py` → `analyse_brand()`

1. **Fetches** the business website content using `tools/website.py` → `fetch()` (up to 8,000 characters)
2. **Sends** the website text to DeepSeek with a prompt to extract:
   - Business introduction (what they actually do)
   - Core brand voice and personality
   - Writing style and Facebook post rules
   - Natural key phrases
   - Service reference list
   - Posting guidelines per content type
3. **Parses** the LLM output using regex into a structured `BrandVoice` Pydantic model
4. **Saves** the full analysis to `brand_voice.md`

The prompt explicitly instructs: *"ONLY use the website content above. Do NOT invent facts."* — this keeps the brand voice authentic to the real business.

### Step 3: Generate Topics

**File:** `agents/topics.py` → `generate_topics()`

1. Takes the business name, website, and brand voice introduction
2. Sends a prompt to DeepSeek requesting **exactly 8 topics** for the current month
3. Topics must match the business industry and services
4. Season-aware (late autumn/winter in Australia, local Canberra context)
5. **Four content types mixed evenly:**
   - **Educational Tip** — teach customers something useful
   - **Customer Story** — showcase testimonials or success stories
   - **Festival Greeting** — tie into holidays and seasonal events
   - **Local Community Engagement** — connect with the local area
6. Output is parsed line-by-line, categorised by keyword matching
7. Returns `list[Topic]`

### Step 4: Research

**File:** `agents/researcher.py` → `research_topic()`

For each topic, the agent:

1. **Searches the web** using DuckDuckGo for `"{business_name} {topic_title}"`
2. **Sends search results + topic + brand context** to DeepSeek
3. DeepSeek produces a structured outline with 9 sections:
   - **Core Summary** (100–200 words) — what this post is about
   - **Key Insights** (3–5 bullet points) — verified facts
   - **Sources** (2–3 URLs or organisations)
   - **Claims to Avoid** — common myths or risky statements
   - **Hook Options** (2–3 casual opening lines)
   - **Key Points** (2–3 one-sentence verified facts)
   - **Practical Takeaway** — one simple tip for the reader
   - **CTA Concept** — soft, community-style call to action
   - **Image Idea** — real local photo concept
4. Returns a structured `Research` Pydantic model

The prompt enforces: *"Only verified facts. Follow brand context. No full post draft."*

### Step 5: Draft

**File:** `agents/drafter.py` → `draft_post()`

1. Takes the **brand voice** + **research outline**
2. Sends to DeepSeek with strict requirements:
   - Structure: Hook → Key Points → Practical Takeaway → CTA
   - Word count: **180–220 words**
   - Tone: casual, warm, local, non-pushy
   - Short paragraphs, mobile-friendly
   - No corporate jargon, no AI clichés
3. Outputs the raw Facebook post draft
4. Returns `DraftPost` with content and word count

### Step 6: Polish

**File:** `agents/polisher.py` → `polish_post()`

The critical humanisation step:

1. Takes the **brand voice** + **draft content**
2. Sends to DeepSeek acting as a *"human local business editor"*
3. Polish rules:
   - Remove stiff AI phrases and repetitive templates
   - Keep all original facts — never modify real information
   - Make it sound like a real business owner talking
   - Short paragraphs, clean line breaks for mobile
   - Keep 180–220 words
   - Max 1 emoji, only if brand-appropriate
4. Output: **only** the polished final post (no headers, no meta-commentary)
5. Returns `FinalPost` — this is the version you copy-paste to Facebook

### Content Calendar

After all 8 topics are processed, the pipeline builds a content calendar:

- Posts are mapped to weeks (1–4) and days (Mon, Wed, Fri, Sat — 2 posts/week)
- Each entry includes: week, day, topic title, content category
- Written to `content_calendar.md`

---

## ⚙️ Configuration

### Full Environment Setup

```bash
# Required — get from platform.deepseek.com
export DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Optional — customise behaviour
export DEEPSEEK_BASE_URL="https://api.deepseek.com"     # API endpoint
export LCA_LLM_MODEL="deepseek-chat"                    # Model name
export LCA_OUTPUT_DIR="./output"                        # Where files go
export LCA_MAX_TOPICS="8"                               # Posts per run
export LCA_RESEARCH_TIMEOUT="300"                       # Seconds per topic
```

### Rate Limiting

The LLM client includes built-in rate limiting: **1.5 seconds between API calls**. This prevents hitting DeepSeek's rate limits during multi-step generation. A full pipeline run (8 topics × 3 API calls each + brand voice + topics ≈ 26 API calls) takes approximately 40–60 seconds of API time plus inference time.

---

## 📐 Pydantic Data Models

All pipeline stages use Pydantic v2 models for type safety and validation. Here's the complete model reference:

### BusinessInfo
```python
class BusinessInfo(BaseModel):
    name: str                           # Business name
    website: Optional[str] = None       # Website URL
    facebook: Optional[str] = None      # Facebook page URL
```

### BrandVoice
```python
class BrandVoice(BaseModel):
    introduction: str      # What the business actually does
    personality: str       # Core brand voice and personality traits
    writing_style: str     # Writing rules and conventions
    key_phrases: list[str] # Natural key phrases used by the business
    services: list[str]    # Service offerings
    guidelines: str        # Posting guidelines per content type
    raw: str               # Full raw LLM output
```

### Topic
```python
class Topic(BaseModel):
    index: int    # 1–8
    title: str    # Topic headline
    category: str # Educational Tip | Customer Story | Festival Greeting | Local Community Engagement
```

### Research
```python
class Research(BaseModel):
    topic_index: int
    core_summary: str          # 100–200 word summary
    key_insights: list[str]    # 3–5 verified fact bullets
    sources: list[str]         # 2–3 URLs or org names
    claims_to_avoid: list[str] # Myths or risky claims
    hook_options: list[str]    # 2–3 casual opening lines
    key_points: list[str]      # 2–3 one-sentence facts
    takeaway: str              # One practical tip
    cta_concept: str           # Soft community CTA
    image_idea: str            # Real local photo concept
    raw: str                   # Full LLM output
```

### DraftPost
```python
class DraftPost(BaseModel):
    topic_index: int
    content: str      # The full draft
    word_count: int   # Should be 180–220
```

### FinalPost
```python
class FinalPost(BaseModel):
    topic_index: int
    topic_title: str
    content: str      # The polished, publishable post
    word_count: int   # Should be 180–220
    changes_made: list[str]  # Tracked edits (reserved for future use)
```

### ContentCalendar
```python
class ContentCalendar(BaseModel):
    business_name: str
    month: str        # e.g. "May"
    year: int         # e.g. 2026
    posts: list[dict] # week, day, topic, category
```

### PipelineResult
```python
class PipelineResult(BaseModel):
    business: BusinessInfo
    brand_voice: BrandVoice
    topics: list[Topic]
    posts: list[FinalPost]
    calendar: ContentCalendar
    generated_at: datetime
```

---

## ❓ FAQ / Troubleshooting

### "DEEPSEEK_API_KEY not set"

```
RuntimeError: DEEPSEEK_API_KEY not set. Run: export DEEPSEEK_API_KEY=sk-...
```

**Solution:** You haven't set your API key. Run:
```bash
export DEEPSEEK_API_KEY="sk-your-actual-key"
```
Get a key at [platform.deepseek.com](https://platform.deepseek.com/).

### "Could not find website or Facebook for 'Business Name'"

```
RuntimeError: Could not find website or Facebook for 'Business Name'
```

**Solution:** The agent couldn't auto-discover the business online. Provide the website manually:
```bash
lca run "Business Name" --website https://their-website.com
```

### "LLM API error: ..."

This usually means one of:
- **Invalid API key** — Double-check your key at [platform.deepseek.com](https://platform.deepseek.com/)
- **Rate limit exceeded** — Wait a minute and try again. The agent has built-in 1.5s rate limiting but provider-side limits can still apply.
- **Network issue** — Check your internet connection
- **Insufficient credits** — Top up your DeepSeek account

### Posts sound too "AI-like"

This is expected for the *draft* stage. Check the `final_post.md` — this has been through the polishing step specifically designed to remove AI clichés. If the final version still sounds off:

1. Try re-generating a specific topic: delete its folder and re-run
2. The polisher prompt can be adjusted in `agents/polisher.py` if you need different polish rules
3. Consider the content as a *starting point* — the final human edit is still yours

### "How do I change the number of posts?"

```bash
export LCA_MAX_TOPICS="12"
lca run "Business Name" --website https://example.com
```

Max recommended is 12 (3 posts/week for a month). Going higher may produce repetitive content.

### "Can I use this for non-Australian businesses?"

Yes! The search queries in `agents/brand_voice.py` are Canberra-centric by default. To adapt:

1. Edit the search queries in `find_business()` in `agents/brand_voice.py`
2. Edit the location context in `generate_topics()` in `agents/topics.py`
3. Change "Canberra" and "Australia" to your region

Or set `LCA_OUTPUT_DIR` to a custom path if you don't want output in the default `./output`.

### "How much does it cost?"

Using DeepSeek's API pricing (as of 2025):
- Each full pipeline run uses ~26 API calls totaling roughly 50K–80K tokens
- At DeepSeek's pricing (~$0.27 per 1M input tokens, ~$1.10 per 1M output tokens), a full run costs approximately **$0.05–$0.10 USD**
- Very affordable for monthly content generation

### "The web search isn't finding good results"

The agent uses DuckDuckGo by default, which may not be as comprehensive as Google. Options:

1. **Install the `websearch` Python package** (auto-detected if present):
   ```bash
   pip install git+https://github.com/ChenneyZhuang/web-search.git
   ```
2. **Enable Perplexity Pro** for deeper research (requires subscription + Playwright):
   ```bash
   pip install -e ".[perplexity]"
   export PERPLEXITY_ENABLED=1
   ```

### "Can I use GPT-4 or Claude instead of DeepSeek?"

Yes! Any OpenAI-compatible API works:

```bash
# For OpenAI
export DEEPSEEK_BASE_URL="https://api.openai.com/v1"
export DEEPSEEK_API_KEY="sk-..."
export LCA_LLM_MODEL="gpt-4o"

# For Anthropic via a compatible proxy
export DEEPSEEK_BASE_URL="https://your-proxy.com/v1"
export LCA_LLM_MODEL="claude-3-5-sonnet"
```

### "The pipeline stopped halfway — can I resume?"

Yes! The agent is designed to be resumable. Each step checks if its output file already exists and skips if so. Just re-run the same command:

```bash
lca run "Business Name" --website https://example.com
```

It will skip completed steps and finish the remaining ones.

### "How do I uninstall?"

```bash
pip uninstall local-content-agent
```

---

## 🗺 Roadmap

- [ ] **Multi-language support** — Generate posts in languages other than English
- [ ] **Instagram & LinkedIn support** — Platform-specific formatting and tone
- [ ] **Perplexity Pro integration** — Deeper research with source citations
- [ ] **Template library** — Pre-built content templates for common business types
- [ ] **Scheduling integration** — Direct publish to Facebook/Meta Business Suite
- [ ] **Image generation prompts** — DALL-E/Midjourney prompts for each post
- [ ] **Analytics feedback loop** — Learn from post performance to improve future content
- [ ] **Web UI / Streamlit app** — No-code interface for non-technical users
- [ ] **Multi-business dashboard** — Track content calendars across multiple clients
- [ ] **Hashtag suggestions** — Platform-optimised hashtag sets per post

---

## 👥 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/local-content-agent.git
   cd local-content-agent
   ```
3. **Install dev dependencies:**
   ```bash
   pip install -e ".[dev]"
   ```
4. **Create a branch:**
   ```bash
   git checkout -b feature/my-awesome-feature
   ```
5. **Make your changes** and add tests if applicable
6. **Run tests:**
   ```bash
   pytest
   ```
7. **Submit a Pull Request** with a clear description

### Development Guidelines

- Follow existing code style (simple, readable Python)
- Add docstrings for new public functions
- Keep dependencies minimal — prefer stdlib where possible
- Test with Python 3.11+

### Ideas for Contributions

- New content categories or templates
- Better search backends (Google, Bing)
- Platform adapters (Instagram, LinkedIn, Twitter/X)
- Improved prompt engineering for better output quality
- CLI improvements (interactive mode, progress bars)
- Docker support

---

## 📄 License

MIT — free for personal and commercial use.

---

*Built with ❤️ in Canberra, Australia*
