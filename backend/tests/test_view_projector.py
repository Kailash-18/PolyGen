"""Unit tests for MultiViewProjector and Occlusion Culling."""
import pytest
import numpy as np
from app.pipeline.view_projector import MultiViewProjector

def test_project_point_to_camera():
    proj = MultiViewProjector(texture_size=256)
    view_mat = np.eye(4, dtype=np.float32)
    u, v, z = proj.project_point_to_camera(np.array([0.0, 0.0, 1.0]), view_mat)
    assert 0.0 <= u <= 1.0
    assert 0.0 <= v <= 1.0

def test_cosine_normal_weight():
    proj = MultiViewProjector(texture_size=256)
    n = np.array([0.0, 0.0, 1.0])
    cam = np.array([0.0, 0.0, 1.0])
    w = proj.compute_view_normal_weight(n, cam)
    assert w == pytest.approx(1.0, abs=1e-3)
    
    # Perpendicular grazing angle
    n_perp = np.array([1.0, 0.0, 0.0])
    w_perp = proj.compute_view_normal_weight(n_perp, cam)
    assert w_perp == 0.0
