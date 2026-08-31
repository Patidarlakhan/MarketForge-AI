"""
AI Marketing Content Engine — Twitter/X Agent

Specialized agent generating X/Twitter multi-tweet threads and standalone posts from Master Content.
"""

import json
import logging
from typing import Any, Dict, Union

from app.agents.base import BaseAgent
from app.schemas.twitter import TwitterOutput

logger = logging.getLogger(__name__)

TWITTER_SYSTEM_PROMPT = """You are a Viral X/Twitter Growth Copywriter and B2B Tech Specialist.
Your task is to transform Master Content into a high-performing X/Twitter content package:
1. Thread (5 to 7 tweets):
   - Tweet 1 (Hook): Ultra-punchy curiosity hook line ending with 🧵 or 👇.
   - Tweet 2 (Problem): The core issue or status quo inefficiency.
   - Tweet 3 (Insight/Shift): Key perspective shift or breakdown.
   - Tweet 4 (Solution/Value): How the solution delivers concrete results.
   - Tweet 5 (CTA): Clear call to action with 1-2 relevant hashtags.
2. Single Post:
   - Standalone punchy post under 280 characters summarizing the primary value driver.
"""


class TwitterAgent(BaseAgent):
    """AI Agent generating X/Twitter threads and standalone posts."""

    async def run(
        self,
        master_content_data: Union[Dict[str, Any], Any],
        campaign_data: Union[Dict[str, Any], Any],
    ) -> TwitterOutput:
        """
        Generate X/Twitter thread and single post from Master Content.
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
                "tone": getattr(campaign_data, "tone", "Punchy"),
            }
        else:
            c_dict = campaign_data

        user_prompt = f"""Please create an X/Twitter content package based on this Master Content blueprint:

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

Provide output matching TwitterOutput schema:
- thread: List of 5-7 TweetItem objects (each text under 280 chars).
- single_post: Standalone post under 280 chars.
"""

        logger.info("TwitterAgent executing content generation")

        return await self.llm.generate_structured(
            system_prompt=TWITTER_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=TwitterOutput,
        )
