"""
Unit tests for Garland-Heckbert QEM Decimator and boundary preservation.
"""

import numpy as np
import trimesh
from app.pipeline.qem_decimator import QEMDecimator

def test_compute_face_quadric():
    decimator = QEMDecimator()
    v0 = np.array([0.0, 0.0, 0.0])
    v1 = np.array([1.0, 0.0, 0.0])
    v2 = np.array([0.0, 1.0, 0.0])
    Kp = decimator.compute_face_quadric(v0, v1, v2)
    assert Kp.shape == (4, 4)
    # Normal is [0, 0, 1], d=0 -> plane is [0, 0, 1, 0]
    assert np.isclose(Kp[2, 2], 1.0)
    assert np.isclose(Kp[0, 0], 0.0)

def test_compute_vertex_quadrics():
    decimator = QEMDecimator()
    box = trimesh.creation.box()
    quadrics = decimator.compute_vertex_quadrics(box.vertices, box.faces, preserve_boundaries=True)
    assert len(quadrics) == len(box.vertices)
    for Q in quadrics:
        assert Q.shape == (4, 4)
        assert np.all(np.isfinite(Q))

def test_evaluate_edge_collapse():
    decimator = QEMDecimator()
    v1 = np.array([0.0, 0.0, 0.0])
    v2 = np.array([1.0, 0.0, 0.0])
    Q1 = np.eye(4)
    Q2 = np.eye(4)
    v_opt, cost = decimator.evaluate_edge_collapse(v1, v2, Q1, Q2)
    assert len(v_opt) == 3
    assert cost >= 0.0

def test_decimate_mesh_target():
    decimator = QEMDecimator(target_faces=20)
    icosphere = trimesh.creation.icosphere(subdivisions=2)
    assert len(icosphere.faces) > 20
    dec_v, dec_f, metrics = decimator.decimate_mesh(icosphere.vertices, icosphere.faces, target_faces=20)
    assert len(dec_f) <= len(icosphere.faces)
    assert metrics["reduction_ratio"] <= 1.0
    assert "reduction_percentage" in metrics
