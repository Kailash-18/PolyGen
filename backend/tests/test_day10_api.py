"""
Integration tests for Week 3 Day 10 REST API routes.
"""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_api_decimate_qem():
    response = client.post("/api/v1/optimize/decimate-qem", json={"model_id": "sword_01", "target_faces": 200})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "metrics" in data
    assert data["metrics"]["after_faces"] <= data["metrics"]["before_faces"]

def test_api_pbr_compile():
    response = client.post("/api/v1/materials/pbr-compile", json={"preset_name": "medieval_rusted_iron"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["material"]["type"] == "MeshPhysicalMaterial"

def test_api_optimize_benchmark():
    response = client.get("/api/v1/optimize/benchmark")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "benchmarks" in data
