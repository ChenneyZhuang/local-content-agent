"""Pydantic models for the Local Content Agent pipeline."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class BusinessInfo(BaseModel):
    """Business identity discovered in Step 1."""

    name: str
    website: Optional[str] = None
    facebook: Optional[str] = None


class BrandVoice(BaseModel):
    """Brand voice profile from Step 2."""

    introduction: str = Field(description="What the business actually does")
    personality: str = Field(description="Core brand voice and personality traits")
    writing_style: str = Field(description="Writing rules and conventions")
    key_phrases: list[str] = Field(default_factory=list)
    services: list[str] = Field(default_factory=list)
    guidelines: str = Field(description="Posting guidelines per content type")
    raw: str = Field(description="Full raw LLM output", default="")


class Topic(BaseModel):
    """A content topic from Step 3."""

    index: int
    title: str
    category: str = Field(
        description="Educational Tip | Customer Story | Festival Greeting | Local Community Engagement"
    )


class Research(BaseModel):
    """Research output from Step 4."""

    topic_index: int
    core_summary: str
    key_insights: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    claims_to_avoid: list[str] = Field(default_factory=list)
    hook_options: list[str] = Field(default_factory=list)
    key_points: list[str] = Field(default_factory=list)
    takeaway: str = ""
    cta_concept: str = ""
    image_idea: str = ""
    raw: str = ""


class DraftPost(BaseModel):
    """Draft Facebook post from Step 5."""

    topic_index: int
    content: str
    word_count: int


class FinalPost(BaseModel):
    """Polished Facebook post from Step 6."""

    topic_index: int
    topic_title: str
    content: str
    word_count: int
    changes_made: list[str] = Field(default_factory=list)


class ContentCalendar(BaseModel):
    """Monthly content calendar."""

    business_name: str
    month: str
    year: int
    posts: list[dict] = Field(default_factory=list)


class PipelineResult(BaseModel):
    """Complete pipeline output for one business."""

    business: BusinessInfo
    brand_voice: BrandVoice
    topics: list[Topic]
    posts: list[FinalPost]
    calendar: ContentCalendar
    generated_at: datetime = Field(default_factory=datetime.now)
