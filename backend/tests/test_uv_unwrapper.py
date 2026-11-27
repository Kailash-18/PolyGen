"""Unit tests for MeshUVUnwrapper and Conformal Mapping."""
import pytest
import numpy as np
from app.pipeline.uv_unwrapper import MeshUVUnwrapper

def test_unwrap_mesh():
    unwrapper = MeshUVUnwrapper()
    verts = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.5], [0.5, 1.0, 1.0]]
    faces = [[0, 1, 2]]
    uvs = unwrapper.unwrap_mesh(verts, faces)
    assert uvs.shape == (3, 2)
    assert np.all(uvs >= 0.0) and np.all(uvs <= 1.0)

def test_uv_distortion_metrics():
    unwrapper = MeshUVUnwrapper()
    verts = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    faces = np.array([[0, 1, 2]])
    uvs = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    metrics = unwrapper.evaluate_uv_distortion(verts, faces, uvs)
    assert metrics["area_distortion"] < 0.05
    assert metrics["is_valid"] is True
