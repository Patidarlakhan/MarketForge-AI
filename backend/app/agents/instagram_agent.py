"""
AI Marketing Content Engine — Instagram Agent

Specialized agent generating Instagram captions, Midjourney visual prompts, and Reel scripts.
"""

import json
import logging
from typing import Any, Dict, Union

from app.agents.base import BaseAgent
from app.schemas.instagram import InstagramOutput

logger = logging.getLogger(__name__)

INSTAGRAM_SYSTEM_PROMPT = """You are a Premier Instagram Visual Strategist and Short-Form Reel Producer.
Your task is to transform Master Content into a complete Instagram visual package:
1. Caption:
   - Engaging opening line with hook emoji.
   - Clean spacing with bullet points or emojis.
   - Problem-to-solution narrative.
   - Direct Instagram call-to-action ("Link in bio", "Save this post", "Comment BELOW").
   - 10 to 15 targeted hashtags placed at the bottom.
2. Image Generation Prompt:
   - Photorealistic Midjourney/DALL-E 3 prompt.
   - Include lighting, aspect ratio (--ar 4:5), style, color palette, and subject details.
3. Reel Script (3 to 5 scenes):
   - Scene sequence with visual_direction, audio_cue, and spoken_text.
"""


class InstagramAgent(BaseAgent):
    """AI Agent generating Instagram captions, visual prompts, and Reel scripts."""

    async def run(
        self,
        master_content_data: Union[Dict[str, Any], Any],
        campaign_data: Union[Dict[str, Any], Any],
    ) -> InstagramOutput:
        """
        Generate Instagram caption, image prompt, and Reel script from Master Content.
        """
        if not isinstance(master_content_data, dict):
            mc_content = getattr(master_content_data, "content", master_content_data)
            if hasattr(mc_content, "model_dump"):
                mc_dict = mc_content.model_dump()
            elif isinstance(mc_content, dict):
                mc_dict = mc_content
            else:
                mc_dict = {}
        else:
            mc_dict = master_content_data.get("content", master_content_data)

        if not isinstance(campaign_data, dict):
            c_dict = {
                "name": getattr(campaign_data, "name", ""),
                "industry": getattr(campaign_data, "industry", ""),
                "tone": getattr(campaign_data, "tone", "Engaging"),
            }
        else:
            c_dict = campaign_data

        user_prompt = f"""Please create an Instagram content package based on this Master Content blueprint:

MASTER CONTENT:
- Title: {mc_dict.get('title')}
- Core Idea: {mc_dict.get('core_idea')}
- Problem: {mc_dict.get('problem')}
- Solution: {mc_dict.get('solution')}
- Business Value: {json.dumps(mc_dict.get('business_value', []))}
- Key Message: {mc_dict.get('key_message')}
- Primary CTA: {mc_dict.get('cta', {}).get('primary', '')}

CAMPAIGN METADATA:
- Industry: {c_dict.get('industry')}
- Tone: {c_dict.get('tone')}

Provide output matching InstagramOutput schema:
- caption: Complete Instagram caption with 10-15 hashtags.
- image_prompt: Detailed Midjourney/DALL-E 3 image prompt.
- reel_script: List of 3-5 ReelScene objects.
"""

        logger.info("InstagramAgent executing content generation")

        return await self.llm.generate_structured(
            system_prompt=INSTAGRAM_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=InstagramOutput,
        )
