"""
AI Marketing Content Engine — Twitter/X Agent Unit Tests

Tests for TwitterAgent thread generation and standalone tweet formatting.
"""

import json
import pytest

from app.agents.twitter_agent import TwitterAgent
from app.schemas.twitter import TwitterOutput
from tests.test_llm_provider import MockLLMProvider

MOCK_TWITTER_JSON = json.dumps({
    "thread": [
        {
            "tweet_number": 1,
            "text": "Most construction projects lose 15% of margin to jobsite safety delays.\n\nHere is how Physical AI fixes site monitoring 🧵👇"
        },
        {
            "tweet_number": 2,
            "text": "1/ Manual safety inspections are slow and error-prone.\n\nPaper reports lag by 48+ hours while safety violations stay unaddressed on site."
        },
        {
            "tweet_number": 3,
            "text": "2/ Computer Vision AI monitors active jobsites 24/7 in real-time, detecting hazards before they turn into costly delays or OSHA fines."
        },
        {
            "tweet_number": 4,
            "text": "3/ Early adopters see:\n• 40% reduction in safety delays\n• Zero OSHA non-compliance fines\n• 3x inspection coverage"
        },
        {
            "tweet_number": 5,
            "text": "4/ Claim your Free Jobsite AI Assessment today to evaluate your active sites in minutes:\nhttps://example.com/assess\n#PropTech #BuildTech"
        }
    ],
    "single_post": "Stop letting jobsite safety risks delay your delivery timeline. Physical AI delivers 24/7 automated hazard detection and 40% faster inspection resolution. Claim your free site assessment today: https://example.com/assess #BuildTech"
})


@pytest.mark.asyncio
async def test_twitter_agent_run_success():
    """Test TwitterAgent produces valid thread and single_post."""
    mock_llm = MockLLMProvider(responses=[MOCK_TWITTER_JSON])
    agent = TwitterAgent(llm_provider=mock_llm)

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
        "tone": "Punchy"
    }

    result = await agent.run(master_content_data, campaign_data)

    assert isinstance(result, TwitterOutput)
    assert len(result.thread) == 5
    assert result.thread[0].tweet_number == 1
    assert "🧵👇" in result.thread[0].text
    assert len(result.single_post) <= 280
    assert mock_llm.call_count == 1
