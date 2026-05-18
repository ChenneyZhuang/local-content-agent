"""Step 6: Polish and humanise the draft post."""

from lca.tools.llm import chat
from lca.models.schemas import FinalPost


def polish_post(
    brand_voice_raw: str,
    draft_content: str,
    topic_title: str,
    topic_index: int,
) -> FinalPost:
    """Polish a draft post — remove AI-isms, make it sound human."""

    prompt = f"""## Task
Act as a human local business editor. Polish this Facebook post to sound fully natural and on-brand. Remove all robotic AI writing style.

## Brand Voice
{brand_voice_raw[:2000]}

## Draft to Polish
{draft_content[:5000]}

Polish Rules:
1. Remove stiff AI phrases, repetitive templates.
2. Keep all original facts — do not modify real information.
3. Make it sound like a real local business owner talking to customers.
4. Short paragraphs, clean line breaks for mobile.
5. Keep 180-220 words.
6. Max 1 emoji, only if brand-appropriate.

Output ONLY the polished final post ready for publishing. No meta-commentary, no "Key Changes Made" sections, no "Polished Final Post" headers."""

    content = chat(prompt)
    word_count = len(content.split())

    return FinalPost(
        topic_index=topic_index,
        topic_title=topic_title,
        content=content.strip(),
        word_count=word_count,
    )
