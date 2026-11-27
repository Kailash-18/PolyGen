import pytest
import trimesh
from app.pipeline.optimizer import MeshOptimizer

@pytest.fixture
def optimizer():
    return MeshOptimizer(target_polycount=500)

def test_clean_and_repair(optimizer):
    box = trimesh.creation.box(extents=[1, 1, 1])
    cleaned = optimizer.clean_and_repair(box)
    assert isinstance(cleaned, trimesh.Trimesh)
    assert len(cleaned.vertices) > 0

def test_decimate_mesh(optimizer):
    sphere = trimesh.creation.icosphere(subdivisions=4, radius=1.0)
    initial_faces = len(sphere.faces)
    decimated, stats = optimizer.decimate(sphere, target_faces=400)
    assert len(decimated.faces) <= initial_faces
    assert stats["after_faces"] <= initial_faces

def test_uv_unwrapping(optimizer):
    sphere = trimesh.creation.icosphere(subdivisions=2, radius=1.0)
    uv_mesh = optimizer.compute_uv_unwrapping(sphere)
    assert hasattr(uv_mesh.visual, "uv")
    assert uv_mesh.visual.uv is not None
    assert len(uv_mesh.visual.uv) == len(uv_mesh.vertices)
