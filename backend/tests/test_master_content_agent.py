"""
AI Marketing Content Engine — Master Content Agent Unit Tests

Tests for MasterContentAgent execution and prompt synthesis using MockLLMProvider.
"""

import json
import pytest

from app.agents.master_content_agent import MasterContentAgent
from app.schemas.master_content import MasterContentOutput
from tests.test_llm_provider import MockLLMProvider

MOCK_MASTER_CONTENT_JSON = json.dumps({
    "title": "Eliminating Jobsite Safety Penalties and Delays with Autonomous Inspection AI",
    "core_idea": "Commercial construction leaders can eliminate inspection bottlenecks and safety hazards by deploying computer vision AI.",
    "problem": "Manual safety inspections are slow, prone to human error, and cause project delays, leading to OSHA fines and labor shortages.",
    "solution": "Physical AI provides 24/7 automated hazard detection and compliance reporting directly on active construction jobsites.",
    "business_value": [
        "Up to 40% reduction in safety-related project delays",
        "Elimination of manual paper-based inspection overhead",
        "95%+ accuracy in proactive OSHA compliance hazard detection"
    ],
    "target_personas": [
        "Chief Executive Officer (CEO)",
        "Chief Operating Officer (COO)",
        "Head of Safety"
    ],
    "key_message": "Transform jobsite safety from a reactive compliance cost into a proactive operational efficiency advantage.",
    "cta": {
        "primary": "Schedule your Free Jobsite AI Assessment",
        "secondary": "Download the AI Construction Benchmark Report"
    }
})


@pytest.mark.asyncio
async def test_master_content_agent_run_success():
    """Test MasterContentAgent produces platform-neutral MasterContentOutput."""
    mock_llm = MockLLMProvider(responses=[MOCK_MASTER_CONTENT_JSON])
    agent = MasterContentAgent(llm_provider=mock_llm)

    campaign_data = {
        "name": "Construction AI Leads",
        "objective": "Generate MQLs",
        "industry": "Construction",
        "product_service": "Physical AI Solutions",
        "target_audience": "Construction Companies",
        "target_personas": ["CEO", "COO", "Head of Safety"],
        "pain_points": ["Safety issues", "Construction delays"],
        "offer": "Free AI Assessment",
        "tone": "Professional",
    }

    strategy_data = {
        "audience_insights": ["CEOs prioritize margin protection."],
        "content_pillars": ["Autonomous Site Safety"],
        "key_messages": ["Eliminate jobsite risks."],
        "topics": ["OSHA penalty reduction"],
        "content_angles": ["Myth-busting tech adoption"],
        "cta": {"primary": "Schedule Free AI Assessment", "secondary": "Download Report"}
    }

    result = await agent.run(campaign_data, strategy_data)

    assert isinstance(result, MasterContentOutput)
    assert result.title.startswith("Eliminating Jobsite Safety")
    assert len(result.business_value) == 3
    assert len(result.target_personas) == 3
    assert result.cta.primary == "Schedule your Free Jobsite AI Assessment"
    assert mock_llm.call_count == 1
