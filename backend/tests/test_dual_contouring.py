"""
Unit tests for Dual Contouring Mesher and Manifold Topology Validation.
"""
import pytest
from app.pipeline.dual_contouring import DualContouringMesher

def dummy_sphere_sdf(x, y, z):
    return 0.5 - (x**2 + y**2 + z**2)**0.5

def test_dual_contouring_mesh_generation():
    mesher = DualContouringMesher(grid_size=12)
    mesh = mesher.generate_mesh(dummy_sphere_sdf)
    assert "vertex_count" in mesh
    assert "face_count" in mesh
    assert mesh["vertex_count"] > 0
    assert mesh["face_count"] > 0

def test_sdf_gradient_normal():
    mesher = DualContouringMesher(grid_size=12)
    normal = mesher.compute_gradient_normal(dummy_sphere_sdf, 0.5, 0.0, 0.0)
    assert len(normal) == 3
    assert abs(normal[0]) > 0.8

def test_manifold_topology_validation():
    mesher = DualContouringMesher(grid_size=12)
    faces = [[0, 1, 2], [0, 2, 3], [1, 2, 4]]
    res = mesher.validate_mesh_manifold(5, faces)
    assert "is_watertight" in res
    assert "non_manifold_edges" in res
