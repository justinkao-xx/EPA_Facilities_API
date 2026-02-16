from fastapi.testclient import TestClient
from main import app
import os
from unittest.mock import MagicMock, patch

client = TestClient(app)

# Mock environment variable for API Token
os.environ["INTERNAL_API_TOKEN"] = "test-token"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_enrich_endpoint_auth_failure():
    response = client.post("/enrich", json={"company_name": "Test", "website": "test.com"})
    # Should fail because no token provided
    assert response.status_code == 401

@patch("main.epa_client")
def test_enrich_endpoint_success(mock_epa_client):
    # Mock the EPA client response
    mock_epa_client.search_facilities.return_value = [
        {"name": "TEST FACILITY", "city": "TEST CITY", "state": "TX"}
    ]

    headers = {"X-API-Key": "test-token"}
    payload = {"company_name": "Tesla", "website": "tesla.com"}
    
    response = client.post("/enrich", json=payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify structure - should ONLY have epa_facilities
    assert "epa_facilities" in data
    assert "hq_address" not in data
    assert "ucc_assets" not in data
    
    # Verify content
    assert len(data["epa_facilities"]) == 1
    assert data["epa_facilities"][0]["name"] == "TEST FACILITY"
