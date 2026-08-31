"""
AI Marketing Content Engine — Blog Agent Unit Tests

Tests for BlogAgent SEO post generation, meta descriptions, and Markdown formatting.
"""

import json
import pytest

from app.agents.blog_agent import BlogAgent
from app.schemas.blog import BlogOutput
from tests.test_llm_provider import MockLLMProvider

MOCK_BLOG_JSON = json.dumps({
    "title": "Eliminating Commercial Construction Jobsite Safety Delays with Physical AI",
    "meta_description": "Discover how Physical AI and computer vision eliminate site inspection bottlenecks, reduce OSHA penalties, and prevent project delays in commercial construction.",
    "slug": "eliminating-jobsite-safety-delays-physical-ai",
    "target_keywords": [
        "Construction Site Safety AI",
        "Jobsite Computer Vision",
        "OSHA Compliance Automation",
        "Physical AI Construction"
    ],
    "markdown_content": """# Eliminating Commercial Construction Jobsite Safety Delays with Physical AI

Commercial construction leaders face an ongoing dilemma: maintaining strict safety standards without delaying critical path timelines.

In 2026, manual safety inspections remain one of the biggest hidden sources of project delays and budget overruns.

## The Cost of Manual Safety Inspections

Traditional safety management relies on paper checklists and periodic physical walkthroughs. This status quo introduces three severe vulnerabilities:

1. **Reporting Lag:** Hazard reports take 48+ hours to reach project directors.
2. **Coverage Gaps:** Manual inspectors can only view a fraction of an active jobsite at any given time.
3. **Retroactive Penalties:** OSHA non-compliance issues are caught after violations occur, resulting in heavy fines.

## The Solution: Autonomous Physical AI Inspection

Physical AI integrates high-resolution computer vision cameras across active jobsites to provide 24/7 automated hazard detection.

### Key Business Value Drivers:
- **40% Delay Reduction:** Proactively fix hazards before work is halted.
- **Zero OSHA Penalties:** Real-time compliance logging prevents costly fines.
- **Enhanced Worker Safety:** Automated alerts ensure site crews remain protected.

## Frequently Asked Questions (FAQ)

### How quickly can Physical AI be deployed on site?
Most commercial sites can be onboarded in less than 48 hours with zero disruption to active trade crews.

### Does the system replace safety officers?
No. Physical AI acts as a force multiplier for safety officers, providing instant alerts and automated paperless reporting.

## Conclusion

Transforming jobsite safety from a reactive cost center into a proactive operational efficiency driver is no longer optional.

[Schedule your Free Jobsite AI Assessment today](https://example.com/assess) to evaluate your site.
"""
})


@pytest.mark.asyncio
async def test_blog_agent_run_success():
    """Test BlogAgent produces valid title, meta_description, slug, keywords, and markdown_content."""
    mock_llm = MockLLMProvider(responses=[MOCK_BLOG_JSON])
    agent = BlogAgent(llm_provider=mock_llm)

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
        "tone": "Authoritative"
    }

    result = await agent.run(master_content_data, campaign_data)

    assert isinstance(result, BlogOutput)
    assert result.slug == "eliminating-jobsite-safety-delays-physical-ai"
    assert len(result.target_keywords) == 4
    assert "# Eliminating Commercial Construction" in result.markdown_content
    assert mock_llm.call_count == 1
