"""
AI Marketing Content Engine — LinkedIn Agent Unit Tests

Tests for LinkedInAgent execution, post generation, and carousel slide structure.
"""

import json
import pytest

from app.agents.linkedin_agent import LinkedInAgent
from app.schemas.linkedin import LinkedInOutput
from tests.test_llm_provider import MockLLMProvider

MOCK_LINKEDIN_JSON = json.dumps({
    "post_text": """Most construction projects lose 15% of their margin to unaddressed site safety delays.

Here is what manual safety inspections miss:
• Paper-based reporting delays hazard fixes by 48+ hours.
• Human inspectors can only cover 20% of an active jobsite.
• OSHA penalties add up fast when violations are caught retroactively.

With Physical AI and Computer Vision:
1. 24/7 real-time hazard detection on active sites.
2. Automated instant alert logs sent straight to site managers.
3. Up to 40% reduction in safety-related project delays.

Stop letting safety risks stall your delivery timeline.

👉 Schedule your Free Jobsite AI Assessment today: https://example.com/assess

#ConstructionTech #AIinConstruction #JobsiteSafety #PropTech #SafetyFirst""",
    "carousel_slides": [
        {
            "slide_number": 1,
            "header": "How AI Prevents Costly Construction Jobsite Delays",
            "body_points": ["Why manual safety inspections are failing commercial projects in 2026."],
            "visual_note": "Bold contrast title slide with construction drone graphic."
        },
        {
            "slide_number": 2,
            "header": "The Hidden Cost of Paper Inspections",
            "body_points": ["48-hour lag in reporting", "Overlooked site hazards", "Expensive OSHA penalties"],
            "visual_note": "Red warning icon with bullet points."
        },
        {
            "slide_number": 3,
            "header": "The Physical AI Solution",
            "body_points": ["24/7 autonomous site monitoring", "Instant hazard detection", "Automated compliance logs"],
            "visual_note": "Green checkmarks with computer vision wireframe overlay."
        },
        {
            "slide_number": 4,
            "header": "Real World Impact",
            "body_points": ["40% delay reduction", "Zero OSHA fines", "3x inspection coverage"],
            "visual_note": "Bar chart illustrating 40% efficiency gains."
        },
        {
            "slide_number": 5,
            "header": "Claim Your Free AI Assessment",
            "body_points": ["Get your site evaluated in under 15 minutes.", "Visit link in comments!"],
            "visual_note": "Call-to-action button graphic with arrow icon."
        }
    ]
})


@pytest.mark.asyncio
async def test_linkedin_agent_run_success():
    """Test LinkedInAgent produces valid post_text and carousel_slides."""
    mock_llm = MockLLMProvider(responses=[MOCK_LINKEDIN_JSON])
    agent = LinkedInAgent(llm_provider=mock_llm)

    master_content_data = {
        "title": "Eliminating Jobsite Delays with Safety Inspection AI",
        "core_idea": "Deploying computer vision AI eliminates inspection bottlenecks.",
        "problem": "Manual safety inspections are slow and cause project delays.",
        "solution": "Physical AI provides 24/7 automated hazard detection.",
        "business_value": ["40% delay reduction", "Zero OSHA fines"],
        "target_personas": ["CEO", "Head of Safety"],
        "key_message": "Transform safety into an operational efficiency advantage.",
        "cta": {"primary": "Schedule Free Assessment", "secondary": "Download Report"}
    }

    campaign_data = {
        "name": "Construction AI",
        "industry": "Construction",
        "tone": "Professional"
    }

    result = await agent.run(master_content_data, campaign_data)

    assert isinstance(result, LinkedInOutput)
    assert "Most construction projects lose" in result.post_text
    assert "#ConstructionTech" in result.post_text
    assert len(result.carousel_slides) == 5
    assert result.carousel_slides[0].slide_number == 1
    assert result.carousel_slides[0].header.startswith("How AI Prevents")
    assert mock_llm.call_count == 1
