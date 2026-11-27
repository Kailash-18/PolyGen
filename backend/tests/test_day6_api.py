import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_draco_compress():
    resp = client.post("/api/models/test-sword/compress/draco", json={"position_bits": 14, "normal_bits": 10})
    assert resp.status_code == 200
    data = resp.json()
    assert data["model_id"] == "test-sword"

def test_api_impostor_bake():
    resp = client.post("/api/models/test-sword/impostor")
    assert resp.status_code == 200
    assert resp.json()["lod_level"] == "LOD4_Impostor"

def test_api_physics_rigidbody():
    resp = client.post("/api/models/test-sword/physics/rigidbody?density_kg_m3=1200.0")
    assert resp.status_code == 200
    assert resp.json()["mass_kg"] > 0

def test_api_export_usdz():
    resp = client.get("/api/models/test-sword/export/usdz")
    assert resp.status_code == 200
    assert resp.json()["format"] == "USDZ"

def test_api_batch_pipeline():
    resp = client.post("/api/pipeline/batch", json={"asset_ids": ["sword-01"]})
    assert resp.status_code == 200
    assert resp.json()["status"] == "completed"
