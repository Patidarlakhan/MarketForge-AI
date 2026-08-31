"""
AI Marketing Content Engine — LinkedIn Schemas

Pydantic v2 validation models for LinkedIn post and carousel content.
"""

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class CarouselSlide(BaseModel):
    """Individual slide structure for a PDF document carousel on LinkedIn."""

    slide_number: int = Field(..., description="Slide position number (1-indexed)")
    header: str = Field(..., description="Punchy slide title/headline")
    body_points: List[str] = Field(
        ...,
        min_length=1,
        description="Key bullet points or concise copy for the slide",
    )
    visual_note: Optional[str] = Field(
        default=None,
        description="Design or visual direction note for graphics creation",
    )


class LinkedInOutput(BaseModel):
    """LinkedIn content package containing long-form text post and PDF carousel script."""

    post_text: str = Field(
        ...,
        min_length=50,
        description="Professional long-form LinkedIn text post formatted with hook, body, takeaways, CTA, and hashtags",
    )
    carousel_slides: List[CarouselSlide] = Field(
        ...,
        min_length=3,
        description="Slide-by-slide PDF document carousel script (Title, Problem, Solution, Benefits, CTA)",
    )

    model_config = ConfigDict(extra="ignore")
