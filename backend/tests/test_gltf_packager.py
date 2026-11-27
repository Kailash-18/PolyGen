"""
Unit Tests for Binary glTF (GLB) Packager
"""

import pytest
import trimesh
from app.pipeline.gltf_packager import GLTFPackager


@pytest.fixture
def test_mesh():
    return trimesh.creation.box(extents=(1.0, 1.0, 1.0))


def test_assemble_glb_validity(test_mesh):
    glb_bytes = GLTFPackager.assemble_glb(test_mesh, "BoxAsset")
    assert len(glb_bytes) > 20

    val = GLTFPackager.validate_glb(glb_bytes)
    assert val["valid"] is True
    assert val["version"] == 2
    assert val["total_bytes"] == len(glb_bytes)


def test_assemble_glb_empty_error():
    empty_mesh = trimesh.Trimesh()
    with pytest.raises(ValueError):
        GLTFPackager.assemble_glb(empty_mesh)


def test_validate_corrupt_glb():
    corrupt_bytes = b"NOT_A_GLTF_STREAM_DATA"
    val = GLTFPackager.validate_glb(corrupt_bytes)
    assert val["valid"] is False
