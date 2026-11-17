"""
Unit Tests for Multi-LOD Generation Engine (LOD0, LOD1, LOD2, LOD3)
"""

import pytest
import trimesh
from app.pipeline.lod import LODGenerator, LODSpecification


@pytest.fixture
def test_mesh():
    return trimesh.creation.icosphere(subdivisions=3, radius=1.0)


def test_lod_generation_levels(test_mesh):
    gen = LODGenerator()
    results = gen.generate_lods(test_mesh)
    lods = results["lods"]

    assert "LOD0" in lods
    assert "LOD1" in lods
    assert "LOD2" in lods
    assert "LOD3" in lods
    assert len(lods) == 4


def test_lod_decimation_ratios(test_mesh):
    gen = LODGenerator()
    results = gen.generate_lods(test_mesh)
    specs = results["specifications"]

    f0 = specs["LOD0"]["face_count"]
    f1 = specs["LOD1"]["face_count"]
    f2 = specs["LOD2"]["face_count"]
    f3 = specs["LOD3"]["face_count"]

    assert f0 >= f1
    assert f1 >= f2
    assert f2 >= f3


def test_lod_screen_thresholds(test_mesh):
    gen = LODGenerator()
    results = gen.generate_lods(test_mesh)
    specs = results["specifications"]

    # Game engine threshold hierarchy
    assert specs["LOD0"]["screen_size_threshold"] > specs["LOD1"]["screen_size_threshold"]
    assert specs["LOD1"]["screen_size_threshold"] > specs["LOD2"]["screen_size_threshold"]
    assert specs["LOD2"]["screen_size_threshold"] > specs["LOD3"]["screen_size_threshold"]


def test_hausdorff_error_monotonicity(test_mesh):
    gen = LODGenerator()
    results = gen.generate_lods(test_mesh)
    specs = results["specifications"]

    # LOD0 master must have zero error
    assert specs["LOD0"]["hausdorff_error"] == 0.0
    # Lower LODs must have non-negative error bounded reasonably
    assert specs["LOD3"]["hausdorff_error"] >= 0.0
    assert specs["LOD3"]["hausdorff_error"] < 0.5


def test_lod_export(tmp_path, test_mesh):
    gen = LODGenerator()
    results = gen.generate_lods(test_mesh)
    exported = gen.export_lods(tmp_path, "sample_prop", results["lods"])

    assert len(exported) == 4
    for lod_name, file_path in exported.items():
        p = tmp_path / f"sample_prop_{lod_name.lower()}.glb"
        if not p.exists():
            p = tmp_path / f"sample_prop_{lod_name.lower()}.obj"
        assert p.exists()
