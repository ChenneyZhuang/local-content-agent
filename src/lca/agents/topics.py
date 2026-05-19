"""Steps 2-3: Brand Voice analysis and Topic generation."""

import re
from lca.tools.llm import chat
from lca.tools.website import fetch
from lca.models.schemas import BrandVoice, Topic, BusinessInfo


def analyse_brand(name: str, info: BusinessInfo) -> BrandVoice:
    """Step 2: Analyse brand voice from real website AND Facebook content."""
    website_text = fetch(info.website) if info.website else ""
    facebook_text = fetch(info.facebook) if info.facebook else ""

    if not website_text and not facebook_text:
        raise RuntimeError(
            f"Could not fetch any content from website or Facebook for '{name}'. "
            f"Cannot build brand voice from real content."
        )

    prompt = f"""Analyse and create a complete Brand Voice profile for this local business.
Use ONLY the real content from their website and Facebook page below.

Business Name: {name}
Website: {info.website or "N/A"}
Facebook: {info.facebook or "N/A"}

=== WEBSITE CONTENT (formal, public-facing) ===
{website_text or "(Could not fetch website content)"}

=== FACEBOOK PAGE CONTENT (casual, community-facing) ===
{facebook_text or "(Could not fetch Facebook content)"}

Rules:
1. ONLY use the content above. Do NOT invent facts or guess.
2. If the website clearly shows the business type, describe THAT business.
3. Note any differences between website tone (formal) vs Facebook tone (casual/community).
4. Output in exactly this structure:
- Business brief introduction (what they actually do — from website)
- Core brand voice & personality (from both sources)
- Writing style & Facebook post rules (how they talk on Facebook specifically)
- Suitable natural key phrases (words/phrases they actually use)
- Business service reference list (what services/products they offer)
- Posting guidelines per content type
5. Keep tone warm, casual, local, non-corporate."""

    raw = chat(prompt)
    return BrandVoice(
        introduction=_extract_section(raw, "introduction"),
        personality=_extract_section(raw, "personality"),
        writing_style=_extract_section(raw, "writing style|facebook post rules"),
        key_phrases=_extract_list(raw, "key phrases"),
        services=_extract_list(raw, "service|services"),
        guidelines=_extract_section(raw, "guidelines"),
        raw=raw,
    )


def generate_topics(name: str, info: BusinessInfo, brand: BrandVoice) -> list[Topic]:
    """Step 3: Generate 8 monthly content topics."""
    prompt = f"""Generate exactly 8 Facebook post topics for this business for the current month.

Business: {name}
Website: {info.website or "N/A"}
Facebook: {info.facebook or "N/A"}

BUSINESS TYPE: {brand.introduction[:500]}

Requirements:
1. Fit the business industry and services perfectly.
2. Match current season and upcoming local events in Canberra, Australia.
3. Mix 4 types evenly: Educational Tips / Customer Story / Festival Greeting / Local Community Engagement.
4. No hard-sell. Helpful, friendly, community-focused.
5. Output exactly 8 topics, numbered 1-8, one per line."""

    raw = chat(prompt)
    topics = []
    for line in raw.split("\n"):
        line = line.strip()
        m = re.match(r"^(\d+)[.\)\-:]\s*(.+)$", line)
        if m and 3 < len(m.group(2)) < 250:
            category = "Educational Tip"
            lower = m.group(2).lower()
            if "customer" in lower or "story" in lower:
                category = "Customer Story"
            elif "festival" in lower or "greeting" in lower or "holiday" in lower:
                category = "Festival Greeting"
            elif "community" in lower or "engagement" in lower or "spotlight" in lower:
                category = "Local Community Engagement"
            topics.append(
                Topic(
                    index=len(topics) + 1, title=m.group(2).strip(), category=category
                )
            )

    return topics[:8]


def _extract_section(text: str, pattern: str) -> str:
    m = re.search(
        rf"(?:^|\n)\s*[\*\-]*\s*(?:{pattern})[\*\-:\s]*(.+?)(?:\n\s*(?:\*\*|[A-Z][a-z])|\n\n|\Z)",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    return m.group(1).strip()[:500] if m else ""


def _extract_list(text: str, pattern: str) -> list[str]:
    section = _extract_section(text, pattern)
    items = re.findall(r"[•\-\*]\s*(.+?)(?=\n\s*[•\-\*]|\Z)", section, re.DOTALL)
    return items[:10] if items else []
