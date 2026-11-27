import pytest
import trimesh
from app.pipeline.geometry import GeometryEngine

@pytest.fixture
def geo_engine():
    return GeometryEngine()

def test_sword_geometry(geo_engine):
    mesh = geo_engine.generate_mesh("medieval broadsword")
    assert isinstance(mesh, trimesh.Trimesh)
    assert len(mesh.vertices) > 50
    assert len(mesh.faces) > 50
    assert max(mesh.extents) <= 2.05

def test_shield_geometry(geo_engine):
    mesh = geo_engine.generate_mesh("viking shield")
    assert isinstance(mesh, trimesh.Trimesh)
    assert len(mesh.vertices) > 50

def test_crystal_geometry(geo_engine):
    mesh = geo_engine.generate_mesh("glowing crystal")
    assert isinstance(mesh, trimesh.Trimesh)
    assert len(mesh.vertices) > 20

def test_vase_geometry(geo_engine):
    mesh = geo_engine.generate_mesh("ceramic vase")
    assert isinstance(mesh, trimesh.Trimesh)
    assert len(mesh.vertices) > 50
