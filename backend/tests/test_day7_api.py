"""
Unit tests for Week 1 Generative 3D AI and Pipeline REST Endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_neural_sampler_api():
    resp = client.post("/api/v1/neural/sample", json={"x": 0.1, "y": -0.2, "z": 0.3})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert "density" in data
    assert data["coordinates"] == [0.1, -0.2, 0.3]

def test_dual_contour_api():
    resp = client.post("/api/v1/geometry/dual-contour", json={"grid_size": 8})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert "mesh" in data

def test_asset_manifest_api():
    resp = client.post("/api/v1/assets/manifest", json={
        "asset_id": "test_arm_01",
        "name": "Robotic Arm Assembly",
        "poly_count": 8500,
        "vertex_count": 4200
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["manifest"]["asset_id"] == "test_arm_01"

def test_queue_submit_api():
    resp = client.post("/api/v1/queue/submit", json={
        "prompt": "heavy industrial hydraulic actuator",
        "priority": 2
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "queued"
    assert "job_id" in data
