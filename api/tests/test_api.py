from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_services():
    response = client.get("/api/services")
    assert response.status_code == 200
    assert "services" in response.json()
    assert len(response.json()["services"]) > 0
