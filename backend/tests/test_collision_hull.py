"""
Unit Tests for Physics Collision Hull Generator
"""

import pytest
import trimesh
from app.pipeline.collision_hull import CollisionHullGenerator


@pytest.fixture
def box_mesh():
    return trimesh.creation.box(extents=(2.0, 1.0, 4.0))


def test_convex_hull_volume(box_mesh):
    gen = CollisionHullGenerator()
    hull_mesh, spec = gen.generate_convex_hull(box_mesh)

    assert hull_mesh.is_watertight
    # Box volume is 2 * 1 * 4 = 8.0
    assert abs(spec.volume - 8.0) < 0.2
    assert spec.collider_type == "convex_hull"
    assert spec.engine_identifier.startswith("UCX_")


def test_oriented_bounding_box(box_mesh):
    gen = CollisionHullGenerator()
    obb_mesh, spec = gen.generate_oriented_bounding_box(box_mesh)

    assert spec.collider_type == "oriented_box"
    assert len(spec.extents) == 3
    # Extents should match dimensions sorted
    exts = sorted(spec.extents)
    assert abs(exts[0] - 1.0) < 0.1
    assert abs(exts[1] - 2.0) < 0.1
    assert abs(exts[2] - 4.0) < 0.1


def test_axis_aligned_box(box_mesh):
    gen = CollisionHullGenerator()
    aabb_mesh, spec = gen.generate_axis_aligned_box(box_mesh)

    assert spec.collider_type == "axis_aligned_box"
    assert spec.vertex_count == 8
    assert spec.face_count == 12


def test_bounding_capsule(box_mesh):
    gen = CollisionHullGenerator()
    cap_mesh, spec = gen.generate_bounding_capsule(box_mesh)

    assert spec.collider_type == "capsule"
    assert spec.volume > 0.0
    assert len(spec.extents) == 3


def test_all_colliders_manifest(box_mesh):
    gen = CollisionHullGenerator()
    res = gen.generate_all_colliders(box_mesh)

    assert "convex_hull" in res["manifest"]
    assert "oriented_box" in res["manifest"]
    assert "axis_aligned_box" in res["manifest"]
    assert "capsule" in res["manifest"]
    assert res["recommended_primary"] in ["convex_hull", "oriented_box"]


def test_unreal_collision_export(tmp_path, box_mesh):
    gen = CollisionHullGenerator()
    res = gen.generate_all_colliders(box_mesh)
    ucx_path = gen.export_unreal_collision_file(tmp_path, "CyberBlade", res["meshes"])

    assert (tmp_path / "UCX_CyberBlade_01.obj").exists()
