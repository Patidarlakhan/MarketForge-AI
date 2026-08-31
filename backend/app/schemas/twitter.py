"""
AI Marketing Content Engine — X / Twitter Schemas

Pydantic v2 validation models for X/Twitter threads and standalone posts.
"""

from typing import List
from pydantic import BaseModel, ConfigDict, Field


class TweetItem(BaseModel):
    """Single tweet item within a Twitter thread."""

    tweet_number: int = Field(..., description="Position index of the tweet in thread (1-indexed)")
    text: str = Field(
        ...,
        min_length=10,
        max_length=300,
        description="Tweet body copy (strictly capped under 280 characters recommended)",
    )


class TwitterOutput(BaseModel):
    """Twitter content package containing a multi-tweet thread and single standalone tweet."""

    thread: List[TweetItem] = Field(
        ...,
        min_length=3,
        description="5-7 tweet thread (Hook, Problem, Solution, Stat/Insight, CTA)",
    )
    single_post: str = Field(
        ...,
        min_length=10,
        max_length=300,
        description="Punchy standalone post under 280 characters for immediate broadcasting",
    )

    model_config = ConfigDict(extra="ignore")
