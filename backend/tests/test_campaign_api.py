"""
AI Marketing Content Engine — Campaign API Tests

Integration tests for Campaign CRUD API endpoints.
"""

import uuid
import pytest
from httpx import AsyncClient

SAMPLE_CAMPAIGN = {
    "name": "Construction AI Leads",
    "objective": "Generate MQLs",
    "industry": "Construction",
    "product_service": "Physical AI Solutions",
    "target_audience": "Construction Companies",
    "target_personas": ["CEO", "COO", "Head of Construction"],
    "pain_points": [
        "Construction delays",
        "Safety issues",
        "Manual inspections",
        "Labor shortage",
    ],
    "offer": "Free AI Construction Assessment",
    "landing_page": "https://example.com/assessment",
    "brand_info": "Leading provider of physical AI solutions",
    "tone": "Professional",
}


@pytest.mark.asyncio
async def test_create_campaign_api(client: AsyncClient):
    """Test POST /api/v1/campaigns creates a campaign."""
    response = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == SAMPLE_CAMPAIGN["name"]
    assert data["status"] == "draft"
    assert "id" in data
    assert len(data["target_personas"]) == 3
    assert len(data["pain_points"]) == 4


@pytest.mark.asyncio
async def test_list_campaigns_api(client: AsyncClient):
    """Test GET /api/v1/campaigns returns a list of campaigns."""
    # Create two campaigns
    await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    c2 = dict(SAMPLE_CAMPAIGN, name="Second Campaign")
    await client.post("/api/v1/campaigns", json=c2)

    response = await client.get("/api/v1/campaigns")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    names = {item["name"] for item in data}
    assert "Construction AI Leads" in names
    assert "Second Campaign" in names


@pytest.mark.asyncio
async def test_get_campaign_api(client: AsyncClient):
    """Test GET /api/v1/campaigns/{id} retrieves a single campaign."""
    create_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = create_res.json()["id"]

    response = await client.get(f"/api/v1/campaigns/{campaign_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == campaign_id
    assert data["name"] == SAMPLE_CAMPAIGN["name"]


@pytest.mark.asyncio
async def test_get_campaign_not_found(client: AsyncClient):
    """Test GET /api/v1/campaigns/{id} with non-existent UUID returns 404."""
    fake_id = str(uuid.uuid4())
    response = await client.get(f"/api/v1/campaigns/{fake_id}")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_update_campaign_api(client: AsyncClient):
    """Test PATCH /api/v1/campaigns/{id} updates campaign fields."""
    create_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = create_res.json()["id"]

    update_payload = {
        "name": "Updated Campaign Name",
        "tone": "Bold & Tech-forward",
    }
    response = await client.patch(f"/api/v1/campaigns/{campaign_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Campaign Name"
    assert data["tone"] == "Bold & Tech-forward"
    assert data["objective"] == SAMPLE_CAMPAIGN["objective"]  # Unchanged field


@pytest.mark.asyncio
async def test_delete_campaign_api(client: AsyncClient):
    """Test DELETE /api/v1/campaigns/{id} deletes a campaign."""
    create_res = await client.post("/api/v1/campaigns", json=SAMPLE_CAMPAIGN)
    campaign_id = create_res.json()["id"]

    # Delete
    del_res = await client.delete(f"/api/v1/campaigns/{campaign_id}")
    assert del_res.status_code == 204

    # Verify 404 on get
    get_res = await client.get(f"/api/v1/campaigns/{campaign_id}")
    assert get_res.status_code == 404
