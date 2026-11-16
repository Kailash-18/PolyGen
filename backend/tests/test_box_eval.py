"""
Unit tests for PolyGen 3D Bounding Box & Collision Clearance Evaluator
"""
from app.pipeline.box_eval import (
    Box3D,
    aabb_intersects,
    box3d_iou,
    box3d_distance,
    evaluate_timeline_clearance
)

def test_aabb_intersection_disjoint():
    box_a = Box3D(id="a", min_pt=(0, 0, 0), max_pt=(10, 10, 10))
    box_b = Box3D(id="b", min_pt=(15, 15, 15), max_pt=(25, 25, 25))
    assert not aabb_intersects(box_a, box_b)
    assert box3d_iou(box_a, box_b) == 0.0

def test_aabb_intersection_overlapping():
    box_a = Box3D(id="a", min_pt=(0, 0, 0), max_pt=(10, 10, 10))
    box_b = Box3D(id="b", min_pt=(5, 5, 5), max_pt=(15, 15, 15))
    assert aabb_intersects(box_a, box_b)
    iou = box3d_iou(box_a, box_b)
    assert iou > 0.0
    assert iou < 1.0

def test_box3d_iou_identical():
    box_a = Box3D(id="a", min_pt=(0, 0, 0), max_pt=(10, 10, 10))
    box_b = Box3D(id="b", min_pt=(0, 0, 0), max_pt=(10, 10, 10))
    assert box3d_iou(box_a, box_b) == 1.0

def test_box3d_distance():
    box_a = Box3D(id="a", min_pt=(0, 0, 0), max_pt=(10, 10, 10))
    box_b = Box3D(id="b", min_pt=(14, 0, 0), max_pt=(24, 10, 10))
    assert box3d_distance(box_a, box_b) == 4.0

def test_evaluate_timeline_clearance():
    components = [
        {"id": "part_left", "center": [-10, 0, 0], "size": [8, 8, 8], "explosion_direction": [-1, 0, 0], "explosion_distance": 20.0},
        {"id": "part_right", "center": [10, 0, 0], "size": [8, 8, 8], "explosion_direction": [1, 0, 0], "explosion_distance": 20.0}
    ]
    report = evaluate_timeline_clearance(components, progress_steps=10, min_clearance_mm=2.0)
    assert report["is_collision_free"] is True
    assert report["status"] == "PASS"
