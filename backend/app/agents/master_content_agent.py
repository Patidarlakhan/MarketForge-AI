"""
AI Marketing Content Engine — Master Content Agent

Generates a platform-neutral Master Content source of truth from a Campaign brief,
Brand Context, and Marketing Strategy.
"""

import json
import logging
from typing import Any, Dict, Union

from app.agents.base import BaseAgent
from app.schemas.master_content import MasterContentOutput

logger = logging.getLogger(__name__)

MASTER_CONTENT_SYSTEM_PROMPT = """You are a Chief Brand Officer and Master Content Architect.
Your task is to synthesize a Campaign Brief, Brand Context, and Marketing Strategy into a single, authoritative MASTER CONTENT blueprint.

CRITICAL INSTRUCTIONS:
1. The Master Content MUST be PLATFORM-NEUTRAL.
2. DO NOT include platform-specific formatting, hashtags, tweets, carousel slides, or HTML/Markdown posts.
3. Establish a compelling core narrative that connects the customer problem to your solution and business value drivers.
4. Ensure the output serves as the single source of truth from which platform-specific content generators (LinkedIn, X, Instagram, Blog) will derive their platform posts.
"""


class MasterContentAgent(BaseAgent):
    """AI Agent responsible for platform-neutral Master Content generation."""

    async def run(
        self,
        campaign_data: Union[Dict[str, Any], Any],
        strategy_data: Union[Dict[str, Any], Any],
    ) -> MasterContentOutput:
        """
        Generate platform-neutral master content from campaign and strategy data.
        
        Accepts dicts or ORM/Pydantic objects.
        Returns validated MasterContentOutput Pydantic model.
        """
        # Format Campaign dict
        if not isinstance(campaign_data, dict):
            c_dict = {
                "name": getattr(campaign_data, "name", ""),
                "objective": getattr(campaign_data, "objective", ""),
                "industry": getattr(campaign_data, "industry", ""),
                "product_service": getattr(campaign_data, "product_service", ""),
                "target_audience": getattr(campaign_data, "target_audience", ""),
                "target_personas": getattr(campaign_data, "target_personas", []),
                "pain_points": getattr(campaign_data, "pain_points", []),
                "offer": getattr(campaign_data, "offer", None),
                "landing_page": getattr(campaign_data, "landing_page", None),
                "brand_info": getattr(campaign_data, "brand_info", None),
                "tone": getattr(campaign_data, "tone", "Professional"),
            }
        else:
            c_dict = campaign_data

        # Format Strategy dict
        if not isinstance(strategy_data, dict):
            content_attr = getattr(strategy_data, "content", strategy_data)
            if hasattr(content_attr, "model_dump"):
                s_dict = content_attr.model_dump()
            elif isinstance(content_attr, dict):
                s_dict = content_attr
            else:
                s_dict = {}
        else:
            s_dict = strategy_data.get("content", strategy_data)

        user_prompt = f"""Please synthesize the following Campaign Brief and Marketing Strategy into a Master Content blueprint:

CAMPAIGN BRIEF:
- Name: {c_dict.get('name')}
- Objective: {c_dict.get('objective')}
- Industry: {c_dict.get('industry')}
- Product / Service: {c_dict.get('product_service')}
- Target Audience: {c_dict.get('target_audience')}
- Target Personas: {json.dumps(c_dict.get('target_personas', []))}
- Customer Pain Points: {json.dumps(c_dict.get('pain_points', []))}
- Offer: {c_dict.get('offer') or 'N/A'}
- Landing Page: {c_dict.get('landing_page') or 'N/A'}
- Brand Info: {c_dict.get('brand_info') or 'N/A'}
- Tone: {c_dict.get('tone')}

STRATEGY BLUEPRINT:
- Audience Insights: {json.dumps(s_dict.get('audience_insights', []))}
- Content Pillars: {json.dumps(s_dict.get('content_pillars', []))}
- Key Messages: {json.dumps(s_dict.get('key_messages', []))}
- Topics: {json.dumps(s_dict.get('topics', []))}
- Content Angles: {json.dumps(s_dict.get('content_angles', []))}
- Primary CTA: {s_dict.get('cta', {}).get('primary', '')}
- Secondary CTA: {s_dict.get('cta', {}).get('secondary', '')}

Provide a platform-neutral Master Content output with:
1. title: Overarching master headline.
2. core_idea: Central core concept unifying the campaign.
3. problem: Comprehensive problem breakdown.
4. solution: How the product/service solves the problem.
5. business_value: List of 3-5 concrete business value drivers.
6. target_personas: List of target personas addressed.
7. key_message: Single overarching key message.
8. cta: Object with primary and secondary calls to action.
"""

        logger.info(f"MasterContentAgent executing for campaign: '{c_dict.get('name')}'")

        master_output = await self.llm.generate_structured(
            system_prompt=MASTER_CONTENT_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=MasterContentOutput,
        )

        return master_output
