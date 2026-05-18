"""Step 4: Research and outline via web search."""

from lca.tools.llm import chat
from lca.tools.web_search import search
from lca.models.schemas import Research


def research_topic(
    business_name: str,
    website: str | None,
    brand_intro: str,
    topic_title: str,
    topic_index: int,
) -> Research:
    """Research a topic and build a post outline using web search + LLM."""

    # Search for relevant info
    search_results = search(f"{business_name} {topic_title[:60]}", 5)

    prompt = f"""Research this local business topic and build a Facebook post outline. Do NOT write the full post.

Business: {business_name}
Website: {website or 'N/A'}
Topic: {topic_title}

Brand Context: {brand_intro[:400]}

Web Search Results:
{search_results[:3000]}

=== Output Structure ===
1. Core Summary (100-200 words)
2. Key Insights (3-5 bullet points)
3. Sources (2-3 URLs or organisation names)
4. Claims to Avoid (common myths/safer alternatives)
5. Hook Options (2-3 casual opening lines)
6. Key Points (2-3 one-sentence points from verified facts)
7. Practical Takeaway (one simple tip)
8. CTA Concept (soft community-style)
9. Image Idea (real local photo concept)

Rules: Only verified facts. Follow brand context. No full post draft."""

    raw = chat(prompt, max_tokens=3000)

    return Research(
        topic_index=topic_index,
        core_summary=_extract(raw, "core summary", 300),
        key_insights=_extract_bullets(raw, "key insights", 5),
        sources=_extract_bullets(raw, "sources", 3),
        claims_to_avoid=_extract_bullets(raw, "claims to avoid", 3),
        hook_options=_extract_bullets(raw, "hook options", 3),
        key_points=_extract_bullets(raw, "key points", 3),
        takeaway=_extract(raw, "takeaway", 200),
        cta_concept=_extract(raw, "cta concept", 150),
        image_idea=_extract(raw, "image idea", 150),
        raw=raw,
    )


def _extract(text: str, label: str, max_chars: int) -> str:
    import re
    m = re.search(rf"{label}[:\-\s]*(.+?)(?:\n\s*\n|\n\d|\Z)", text, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip()[:max_chars] if m else ""


def _extract_bullets(text: str, label: str, max_items: int) -> list[str]:
    import re
    section = _extract(text, label, 2000)
    items = re.findall(r"[•\-\*\d]+\.?\s*(.+?)(?:\n|$)", section)
    return [i.strip() for i in items[:max_items] if len(i.strip()) > 5]
