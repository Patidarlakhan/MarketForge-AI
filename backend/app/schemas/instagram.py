"""
AI Marketing Content Engine — Instagram Schemas

Pydantic v2 validation models for Instagram captions, image generation prompts, and Reel scripts.
"""

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ReelScene(BaseModel):
    """Single scene definition for a short-form video Reel script."""

    scene_number: int = Field(..., description="Scene sequence number (1-indexed)")
    visual_direction: str = Field(..., description="Camera angle, movement, or visual action")
    audio_cue: str = Field(..., description="Background sound effect, voiceover inflection, or music cue")
    spoken_text: str = Field(..., description="On-screen text overlay or spoken voiceover line")


class InstagramOutput(BaseModel):
    """Instagram content package containing caption, image generation prompt, and Reel script."""

    caption: str = Field(
        ...,
        min_length=30,
        description="Engaging Instagram caption with hook, emojis, CTA, and 10-15 relevant hashtags",
    )
    image_prompt: str = Field(
        ...,
        min_length=20,
        description="Detailed text prompt for AI image generation (e.g. Midjourney, DALL-E 3)",
    )
    reel_script: List[ReelScene] = Field(
        ...,
        min_length=3,
        description="3-5 scene short-form video Reel script (Visual, Audio, Spoken Copy)",
    )

    model_config = ConfigDict(extra="ignore")
