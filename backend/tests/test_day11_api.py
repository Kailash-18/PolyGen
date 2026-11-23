"""
Integration tests for Week 3 Day 11 REST API routes.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_advanced_material_compile():
    payload = {
        "asset_id": "sword_hilt_sapphire",
        "material_params": {
            "color": "#1144ee",
            "roughness": 0.1,
            "metalness": 0.05,
            "clearcoat": 0.9,
            "ior": 1.77,
            "transmission": 0.95
        }
    }
    resp = client.post("/api/v1/materials/advanced-compile", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert "fresnel_f0" in data
    assert "KHR_materials_clearcoat" in data["gltf_extensions"]

def test_api_material_update_property():
    payload = {
        "material_id": "sword_hilt_sapphire",
        "property_name": "roughness",
        "new_value": 0.25
    }
    resp = client.post("/api/v1/materials/update-property", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["new_value"] == 0.25

def test_api_materials_presets_library():
    resp = client.get("/api/v1/materials/presets-library")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert "presets" in data
    assert len(data["presets"]) >= 5
