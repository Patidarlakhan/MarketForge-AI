"""
AI Marketing Content Engine — LinkedIn Agent

Specialized agent generating LinkedIn long-form posts and PDF carousel scripts from Master Content.
"""

import json
import logging
from typing import Any, Dict, Union

from app.agents.base import BaseAgent
from app.schemas.linkedin import LinkedInOutput

logger = logging.getLogger(__name__)

LINKEDIN_SYSTEM_PROMPT = """You are a World-Class B2B LinkedIn Thought Leadership Copywriter and Carousel Designer.
Your task is to transform Master Content into a high-performing LinkedIn content package:
1. Long-form Text Post:
   - Attention-grabbing opening hook (no generic greetings).
   - Clean formatting with line breaks for mobile readability.
   - Story / context breakdown of the problem and solution.
   - Key bullet points / takeaways.
   - Clear Call-to-Action.
   - 3-5 relevant B2B hashtags.
2. PDF Carousel Script:
   - 5 to 7 slides structured logically (Slide 1: Hook Title, Slide 2: Problem, Slide 3: Insight, Slide 4: Solution & Benefits, Slide 5: CTA).
   - Each slide must have a punchy header, 2-3 body points, and a visual guidance note.
"""


class LinkedInAgent(BaseAgent):
    """AI Agent generating LinkedIn long-form posts and carousel scripts."""

    async def run(
        self,
        master_content_data: Union[Dict[str, Any], Any],
        campaign_data: Union[Dict[str, Any], Any],
    ) -> LinkedInOutput:
        """
        Generate LinkedIn post text and carousel slides from Master Content.
        """
        # Format Master Content dict
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

        # Format Campaign dict
        if not isinstance(campaign_data, dict):
            c_dict = {
                "name": getattr(campaign_data, "name", ""),
                "industry": getattr(campaign_data, "industry", ""),
                "tone": getattr(campaign_data, "tone", "Professional"),
                "product_service": getattr(campaign_data, "product_service", ""),
            }
        else:
            c_dict = campaign_data

        user_prompt = f"""Please create a LinkedIn content package based on this Master Content blueprint:

MASTER CONTENT:
- Title: {mc_dict.get('title')}
- Core Idea: {mc_dict.get('core_idea')}
- Problem: {mc_dict.get('problem')}
- Solution: {mc_dict.get('solution')}
- Business Value Drivers: {json.dumps(mc_dict.get('business_value', []))}
- Target Personas: {json.dumps(mc_dict.get('target_personas', []))}
- Key Message: {mc_dict.get('key_message')}
- Primary CTA: {mc_dict.get('cta', {}).get('primary', '')}
- Secondary CTA: {mc_dict.get('cta', {}).get('secondary', '')}

CAMPAIGN METADATA:
- Industry: {c_dict.get('industry')}
- Tone: {c_dict.get('tone')}

Provide output matching LinkedInOutput schema:
- post_text: High-converting long-form LinkedIn post with hook, body, key points, CTA, and 3-5 hashtags.
- carousel_slides: List of 5-7 CarouselSlide objects.
"""

        logger.info("LinkedInAgent executing content generation")

        return await self.llm.generate_structured(
            system_prompt=LINKEDIN_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=LinkedInOutput,
        )
