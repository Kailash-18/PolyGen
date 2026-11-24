"""
Integration tests for Week 3 Day 12 HDRI staging and tone mapping REST routes.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_hdri_stage():
    payload = {
        "asset_id": "sword_01",
        "preset_id": "sunset_warm",
        "exposure": 0.9,
        "background_blur": 0.2
    }
    resp = client.post("/api/v1/environment/hdri-stage", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["stage"]["asset_id"] == "sword_01"
    assert data["stage"]["environment"]["environmentPreset"] == "sunset_warm"

def test_api_tonemap_config():
    payload = {
        "tonemapping_type": "ACESFilmicToneMapping",
        "exposure": 1.25,
        "bloom_enabled": True
    }
    resp = client.post("/api/v1/environment/tonemap-config", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["postprocessing"]["toneMappingExposure"] == 1.25

def test_api_environment_presets_catalog():
    resp = client.get("/api/v1/environment/presets-catalog")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert len(data["presets"]) >= 5
