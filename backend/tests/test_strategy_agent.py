"""
AI Marketing Content Engine — Strategy Agent Unit Tests

Tests for StrategyAgent execution and prompt handling using MockLLMProvider.
"""

import json
import pytest

from app.agents.strategy_agent import StrategyAgent
from app.schemas.strategy import StrategyOutput
from tests.test_llm_provider import MockLLMProvider

MOCK_STRATEGY_JSON = json.dumps({
    "audience_insights": [
        "CEOs care about overall margin and risk mitigation.",
        "Head of Safety is driven by zero-incident compliance metrics."
    ],
    "content_pillars": [
        "Autonomous Site Safety",
        "Operational Efficiency & Delay Reduction",
        "ROI of Physical AI"
    ],
    "key_messages": [
        "Eliminate jobsite safety risks before they cause costly delays.",
        "Physical AI automates manual safety inspection reporting."
    ],
    "topics": [
        "How AI reduces OSHA safety penalties in commercial construction",
        "5 ways computer vision spots hazards faster than manual inspection",
        "The hidden cost of construction site delays in 2026"
    ],
    "content_angles": [
        "Myth-busting: Why safety technology accelerates projects rather than slowing them down",
        "Data-driven ROI benchmark report"
    ],
    "cta": {
        "primary": "Claim your Free Jobsite AI Assessment",
        "secondary": "Download the 2026 Construction AI Benchmark Report"
    }
})


@pytest.mark.asyncio
async def test_strategy_agent_run_success():
    """Test StrategyAgent returns structured StrategyOutput."""
    mock_llm = MockLLMProvider(responses=[MOCK_STRATEGY_JSON])
    agent = StrategyAgent(llm_provider=mock_llm)

    campaign_data = {
        "name": "Construction AI Leads",
        "objective": "Generate MQLs",
        "industry": "Construction",
        "product_service": "Physical AI Solutions",
        "target_audience": "Construction Companies",
        "target_personas": ["CEO", "COO", "Head of Construction"],
        "pain_points": ["Safety issues", "Construction delays"],
        "offer": "Free AI Construction Assessment",
        "landing_page": "https://example.com/assessment",
        "brand_info": "Leading provider of physical AI solutions",
        "tone": "Professional",
    }

    result = await agent.run(campaign_data)

    assert isinstance(result, StrategyOutput)
    assert len(result.audience_insights) == 2
    assert len(result.content_pillars) == 3
    assert len(result.key_messages) == 2
    assert len(result.topics) == 3
    assert result.cta.primary == "Claim your Free Jobsite AI Assessment"
    assert mock_llm.call_count == 1
