"""
AI Marketing Content Engine — Blog Agent

Specialized agent generating long-form SEO blog posts from Master Content.
"""

import json
import logging
from typing import Any, Dict, Union

from app.agents.base import BaseAgent
from app.schemas.blog import BlogOutput

logger = logging.getLogger(__name__)

BLOG_SYSTEM_PROMPT = """You are a Senior B2B SEO Content Strategist and Technical Journalist.
Your task is to transform Master Content into an authoritative, search-optimized long-form blog post:
1. SEO Title: High CTR H1 headline containing primary keyword.
2. Meta Description: 150-160 character punchy search snippet summarizing value.
3. Slug: Clean lowercase URL slug.
4. Target Keywords: 3-5 high-intent SEO keywords.
5. Markdown Content:
   - Engaging intro capturing the problem statement.
   - H2 & H3 subheadings structuring the deep dive.
   - Bulleted list of key business value drivers.
   - FAQ section answering 2-3 common buyer questions.
   - Strong concluding section with clear CTA.
"""


class BlogAgent(BaseAgent):
    """AI Agent generating long-form SEO blog articles."""

    async def run(
        self,
        master_content_data: Union[Dict[str, Any], Any],
        campaign_data: Union[Dict[str, Any], Any],
    ) -> BlogOutput:
        """
        Generate long-form SEO blog post from Master Content.
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
                "tone": getattr(campaign_data, "tone", "Authoritative"),
            }
        else:
            c_dict = campaign_data

        user_prompt = f"""Please create a long-form SEO blog post package based on this Master Content blueprint:

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

Provide output matching BlogOutput schema:
- title: SEO H1 title.
- meta_description: 150-160 char meta description.
- slug: Clean URL slug.
- target_keywords: 3-5 SEO keywords.
- markdown_content: Full Markdown article text (at least 200 words with headings, intro, body, key takeaways, FAQ, CTA).
"""

        logger.info("BlogAgent executing content generation")

        return await self.llm.generate_structured(
            system_prompt=BLOG_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            response_model=BlogOutput,
        )
