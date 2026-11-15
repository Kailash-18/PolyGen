import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "gpu" in data

def test_get_assembly_broadsword(client):
    res = client.get("/api/models/sword-01/assembly")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Cybernetic Broadsword"
    assert len(data["parts"]) >= 5
    assert len(data["relationships"]) >= 3

def test_get_assembly_drone(client):
    res = client.get("/api/models/drone-01/assembly")
    assert res.status_code == 200
    data = res.json()
    assert "Drone" in data["name"]
    assert len(data["parts"]) >= 12

def test_post_assembly_explode(client):
    res = client.post("/api/models/drone-01/assembly/explode", json={"progress": 0.5})
    assert res.status_code == 200
    data = res.json()
    assert data["progress"] == 0.5
    assert len(data["poses"]) >= 12

def test_list_assemblies(client):
    res = client.get("/api/assemblies")
    assert res.status_code == 200
    data = res.json()
    assert len(data["assemblies"]) == 5

def test_generate_asset(client):
    res = client.post("/api/generate", json={
        "prompt": "Cybernetic sword",
        "target_faces": 500,
        "detail_level": "low"
    })
    assert res.status_code == 200
    data = res.json()
    assert "model_id" in data
    assert "urls" in data
    assert data["urls"]["glb"].endswith(".glb")
