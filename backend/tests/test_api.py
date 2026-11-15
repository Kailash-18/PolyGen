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

def test_list_physical_samples(client):
    res = client.get("/api/physical/samples")
    assert res.status_code == 200
    data = res.json()
    assert "samples" in data
    assert len(data["samples"]) >= 5
    sample_ids = [s["id"] for s in data["samples"]]
    assert "iphone-17" in sample_ids
    assert "game-boy" in sample_ids

def test_get_physical_sample_detail(client):
    res = client.get("/api/physical/samples/iphone-17")
    assert res.status_code == 200
    data = res.json()
    assert "components" in data
    assert "scene" in data
    assert "assembly" in data["scene"]
    assert len(data["scene"]["assembly"]["parts"]) >= 10

def test_viewer_static_mount(client):
    res = client.get("/viewer/")
    assert res.status_code == 200
    assert "<title>" in res.text or "html" in res.text

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
