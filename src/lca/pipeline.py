"""Main pipeline orchestrator — runs the 6-step workflow."""

from pathlib import Path
from datetime import datetime
from lca.config import OUTPUT_DIR, MAX_TOPICS
from lca.models.schemas import (
    BusinessInfo, BrandVoice, Topic, Research,
    DraftPost, FinalPost, ContentCalendar, PipelineResult,
)
from lca.agents.brand_voice import find_business
from lca.agents.topics import analyse_brand, generate_topics
from lca.agents.researcher import research_topic
from lca.agents.drafter import draft_post
from lca.agents.polisher import polish_post


def run(business_name: str, website: str | None = None, facebook: str | None = None) -> PipelineResult:
    """Run the full content generation pipeline for one business.

    Args:
        business_name: Name of the business (e.g. "Brett's Automotive")
        website: Optional known website URL
        facebook: Optional known Facebook page URL
    """
    import re

    safe_name = re.sub(r"[^a-zA-Z0-9_\u4e00-\u9fff]+", "_", business_name).strip("_")
    out_dir = OUTPUT_DIR / safe_name
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── Step 1: Find business links ──
    if website or facebook:
        info = BusinessInfo(name=business_name, website=website, facebook=facebook)
    else:
        info = find_business(business_name)

    if not info.website and not info.facebook:
        raise RuntimeError(f"Could not find website or Facebook for '{business_name}'")

    # ── Step 2: Brand Voice ──
    print(f"  Step 2: Analysing brand voice...")
    brand = analyse_brand(business_name, info)
    (out_dir / "brand_voice.md").write_text(brand.raw, encoding="utf-8")

    # ── Step 3: Topics ──
    print(f"  Step 3: Generating {MAX_TOPICS} topics...")
    topics = generate_topics(business_name, info, brand)
    topics_text = "\n".join(f"{t.index}. [{t.category}] {t.title}" for t in topics)
    (out_dir / "topic_list.md").write_text(
        f"# {business_name} — Topics\n\n{topics_text}\n", encoding="utf-8"
    )

    # ── Steps 4-6: Per topic ──
    posts: list[FinalPost] = []
    for topic in topics:
        print(f"  Topic {topic.index}/{len(topics)}: {topic.title[:60]}...")

        topic_dir = out_dir / f"topic_{topic.index:02d}"
        topic_dir.mkdir(exist_ok=True)

        # Step 4: Research
        if not (topic_dir / "research_outline.md").exists():
            research = research_topic(
                business_name, info.website, brand.introduction,
                topic.title, topic.index,
            )
            (topic_dir / "research_outline.md").write_text(
                f"# Topic {topic.index}: {topic.title}\n\n{research.raw}", encoding="utf-8"
            )
        else:
            research_raw = (topic_dir / "research_outline.md").read_text(encoding="utf-8")
            # Strip the markdown header added during save
            research_raw = re.sub(r"^#\s*Topic\s+\d+:.+\n+", "", research_raw)
            research = Research(
                topic_index=topic.index,
                core_summary=research_raw[:300],
                raw=research_raw,
            )

        # Step 5: Draft
        if not (topic_dir / "draft_post.md").exists():
            draft = draft_post(brand.raw, research, topic.title)
            (topic_dir / "draft_post.md").write_text(
                f"# Topic {topic.index}: {topic.title}\n\n{draft.content}", encoding="utf-8"
            )
        else:
            draft_content = (topic_dir / "draft_post.md").read_text(encoding="utf-8")
            # Strip the markdown header added during save
            draft_content = re.sub(r"^#\s*Topic\s+\d+:.+\n+", "", draft_content)
            draft = DraftPost(topic_index=topic.index, content=draft_content, word_count=len(draft_content.split()))

        # Step 6: Polish
        if not (topic_dir / "final_post.md").exists():
            final = polish_post(brand.raw, draft.content, topic.title, topic.index)
            (topic_dir / "final_post.md").write_text(
                f"{final.content}", encoding="utf-8"
            )
            posts.append(final)
        else:
            final_content = (topic_dir / "final_post.md").read_text(encoding="utf-8")
            posts.append(FinalPost(
                topic_index=topic.index,
                topic_title=topic.title,
                content=final_content,
                word_count=len(final_content.split()),
            ))

    # ── Content Calendar ──
    now = datetime.now()
    calendar = ContentCalendar(
        business_name=business_name,
        month=now.strftime("%B"),
        year=now.year,
        posts=[{
            "week": (i % 4) + 1,
            "day": ["Mon", "Wed", "Fri", "Sat"][i % 4],
            "topic": p.topic_title,
            "category": topics[i].category if i < len(topics) else "General",
        } for i, p in enumerate(posts)],
    )
    (out_dir / "content_calendar.md").write_text(
        f"# {business_name} — Content Calendar\n\n"
        + "\n".join(f"- Week {p['week']} {p['day']}: {p['topic'][:80]}" for p in calendar.posts),
        encoding="utf-8",
    )

    print(f"  ✅ Complete: {len(posts)} posts → {out_dir}")
    return PipelineResult(
        business=info,
        brand_voice=brand,
        topics=topics,
        posts=posts,
        calendar=calendar,
    )
