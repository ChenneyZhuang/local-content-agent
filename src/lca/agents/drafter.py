"""Step 5: Draft Facebook post from research."""

from lca.tools.llm import chat
from lca.models.schemas import DraftPost, Research


def draft_post(
    brand_voice_raw: str,
    research: Research,
    topic_title: str,
) -> DraftPost:
    """Draft a Facebook post from research outline and brand voice."""

    prompt = f"""## Role
You are a professional local business Facebook copywriter.

## Brand Voice
{brand_voice_raw[:3000]}

## Research & Outline
{research.raw[:6000]}

## Writing Requirements
1. Follow exactly: Hook → Key Points → Practical Takeaway → CTA.
2. Only use verified facts provided — no new claims.
3. Word count: 180-220 words.
4. Tone: casual, warm, local, non-pushy — aligned with brand voice.
5. Short paragraphs, mobile-friendly, natural human style.
6. No corporate jargon, no AI clichés.

Output only the finished Facebook post draft, no extra explanation."""

    content = chat(prompt)
    word_count = len(content.split())

    return DraftPost(
        topic_index=research.topic_index,
        content=content.strip(),
        word_count=word_count,
    )
