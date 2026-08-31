"""
AI Marketing Content Engine — Blog Schemas

Pydantic v2 validation models for long-form SEO blog posts.
"""

from typing import List
from pydantic import BaseModel, ConfigDict, Field


class BlogOutput(BaseModel):
    """SEO-optimized long-form Blog post package."""

    title: str = Field(
        ...,
        min_length=10,
        description="SEO H1 title designed for high search click-through rate",
    )
    meta_description: str = Field(
        ...,
        min_length=30,
        max_length=200,
        description="Compelling meta description summary for search engine snippet (150-160 chars target)",
    )
    slug: str = Field(
        ...,
        min_length=5,
        description="URL-friendly slug (e.g. eliminating-jobsite-safety-delays-ai)",
    )
    target_keywords: List[str] = Field(
        ...,
        min_length=2,
        description="Primary and secondary SEO target keywords",
    )
    markdown_content: str = Field(
        ...,
        min_length=200,
        description="Full markdown article formatted with H2/H3 subheadings, intro hook, solution sections, bullet takeaways, FAQ, and CTA",
    )

    model_config = ConfigDict(extra="ignore")
