"""
AI Marketing Content Engine — Strategy Agent

Generates strategic marketing positioning, audience insights, content pillars,
key messages, topics, content angles, and CTAs from a campaign brief.
"""

import json
import logging
from typing import Any, Dict, Union

from app.agents.base import BaseAgent
from app.schemas.strategy import StrategyOutput

logger = logging.getLogger(__name__)

STRATEGY_SYSTEM_PROMPT = """You are an elite Senior B2B Marketing Strategist and Growth Copywriter.
Your task is to analyze a marketing campaign brief and generate a comprehensive, highly targeted marketing strategy.

Strategic Rules:
1. Deeply analyze the target buyer personas, their operational challenges, and psychological motivations.
2. Formulate 3-4 distinct Content Pillars that address core customer pain points while showcasing product value.
3. Craft authoritative Key Messages that differentiate the product/service in the market.
4. Propose compelling, high-converting Content Angles (e.g., Data-driven ROI, Industry Benchmarks, Pain Point Relief).
5. Define clear, actionable Call-to-Actions (both primary lead-gen CTA and secondary educational CTA).
6. DO NOT generate platform-specific post text here. Focus strictly on overarching strategic positioning.
"""


class StrategyAgent(BaseAgent):
    """AI Agent responsible for strategic marketing strategy formulation."""

    async def run(self, campaign_data: Union[Dict[str, Any], Any]) -> StrategyOutput:
        """
        Generate marketing strategy from campaign brief data.
        
        Accepts dict or object with campaign attributes.
        Returns validated StrategyOutput Pydantic model.
        """
        if not isinstance(campaign_data, dict):
            # Extract attributes from Pydantic model or ORM model
            campaign_dict = {
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
            campaign_dict = campaign_data

        user_prompt = f"""Please analyze the following campaign brief and formulate a strategic marketing blueprint:

CAMPAIGN BRIEF:
- Campaign Name: {campaign_dict.get('name')}
- Objective: {campaign_dict.get('objective')}
- Industry: {campaign_dict.get('industry')}
- Product / Service: {campaign_dict.get('product_service')}
- Target Audience: {campaign_dict.get('target_audience')}
- Target Buyer Personas: {json.dumps(campaign_dict.get('target_personas', []))}
- Customer Pain Points: {json.dumps(campaign_dict.get('pain_points', []))}
- Offer / Lead Magnet: {campaign_dict.get('offer') or 'N/A'}
- Landing Page URL: {campaign_dict.get('landing_page') or 'N/A'}
- Brand Context: {campaign_dict.get('brand_info') or 'N/A'}
- Communication Tone: {campaign_dict.get('tone')}

Provide a structured strategy containing:
1. audience_insights: Key psychological & operational insights for these personas.
2. content_pillars: 3-4 core thematic pillars.
3. key_messages: Core value proposition statements.
4. topics: 4-6 strategic content topics.
5. content_angles: 3-4 high-converting positioning angles.
6. cta: Primary and secondary call-to-actions.
"""

        logger.info(f"StrategyAgent executing for campaign: '{campaign_dict.get('name')}'")
        
        # Call LLM provider with structured Pydantic schema validation
        strategy_output = await self.llm.generate_structured(
            system_prompt=STRATEGY_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=StrategyOutput,
        )

        return strategy_output
