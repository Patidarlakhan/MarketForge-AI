"""
AI Marketing Content Engine — Instagram Agent Unit Tests

Tests for InstagramAgent caption, image prompt, and Reel script generation.
"""

import json
import pytest

from app.agents.instagram_agent import InstagramAgent
from app.schemas.instagram import InstagramOutput
from tests.test_llm_provider import MockLLMProvider

MOCK_INSTAGRAM_JSON = json.dumps({
    "caption": """🚨 15% of commercial construction project margins are lost to preventable site safety delays.

Manual paper inspections simply cannot keep pace with fast-moving active jobsites. 🏗️

Here is how Physical AI transforms site safety:
⚡ 24/7 automated hazard detection
⚡ Instant digital alert logs
⚡ 40% reduction in safety-related project delays

Ready to eliminate inspection bottlenecks?

👉 Click the link in bio to claim your Free Jobsite AI Assessment!

.
.
#ConstructionAI #JobsiteSafety #PropTech #ConstructionTech #SafetyFirst #PhysicalAI #BuildTech #SmartConstruction #SiteManagement #ConTech #SafetyCulture #CommercialConstruction #B2BTech #Automation""",
    "image_prompt": "Futuristic commercial construction site at sunset, high-tech computer vision bounding boxes highlighting jobsite workers and safety equipment, ultra-detailed 8k resolution, cinematic dramatic lighting, photo realistic style, --ar 4:5 --style raw",
    "reel_script": [
        {
            "scene_number": 1,
            "visual_direction": "Fast-paced montage of busy construction site with red warning icons popping over safety hazards.",
            "audio_cue": "Tense cinematic alarm tone fading into modern upbeat beat.",
            "spoken_text": "Still relying on paper checklists to inspect your jobsites?"
        },
        {
            "scene_number": 2,
            "visual_direction": "Split screen: left side slow manual clipboard inspection vs right side instant AI computer vision scanner.",
            "audio_cue": "Futuristic digital scanning sound effect.",
            "spoken_text": "Manual checks miss 80% of real-time site hazards."
        },
        {
            "scene_number": 3,
            "visual_direction": "Close up of site manager tapping green approved alert on tablet screen.",
            "audio_cue": "Upbeat victory chime.",
            "spoken_text": "Physical AI spots risks instantly, keeping projects on schedule and OSHA-compliant."
        },
        {
            "scene_number": 4,
            "visual_direction": "On-screen text overlay: Claim your Free Jobsite AI Assessment + arrow pointing down.",
            "audio_cue": "Confident voiceover outro.",
            "spoken_text": "Tap the link in bio to get your free site assessment today!"
        }
    ]
})


@pytest.mark.asyncio
async def test_instagram_agent_run_success():
    """Test InstagramAgent produces valid caption, image_prompt, and reel_script."""
    mock_llm = MockLLMProvider(responses=[MOCK_INSTAGRAM_JSON])
    agent = InstagramAgent(llm_provider=mock_llm)

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
        "tone": "Engaging"
    }

    result = await agent.run(master_content_data, campaign_data)

    assert isinstance(result, InstagramOutput)
    assert "#ConstructionAI" in result.caption
    assert "--ar 4:5" in result.image_prompt
    assert len(result.reel_script) == 4
    assert result.reel_script[0].scene_number == 1
    assert mock_llm.call_count == 1
