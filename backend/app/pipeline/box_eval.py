"""
PolyGen - 3D Bounding Box & Collision Clearance Evaluation Engine
Implements Axis-Aligned Bounding Box (AABB) intersection, 3D IoU calculation,
continuous trajectory collision checks, and minimum clearance safety verification.
"""

from __future__ import annotations
import math
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

class Box3D(BaseModel):
    id: str
    min_pt: Tuple[float, float, float] = Field(..., description="(xmin, ymin, zmin)")
    max_pt: Tuple[float, float, float] = Field(..., description="(xmax, ymax, zmax)")

    @property
    def dimensions(self) -> Tuple[float, float, float]:
        return (
            max(0.0, self.max_pt[0] - self.min_pt[0]),
            max(0.0, self.max_pt[1] - self.min_pt[1]),
            max(0.0, self.max_pt[2] - self.min_pt[2])
        )

    @property
    def volume(self) -> float:
        d = self.dimensions
        return d[0] * d[1] * d[2]

    @property
    def center(self) -> Tuple[float, float, float]:
        return (
            (self.min_pt[0] + self.max_pt[0]) * 0.5,
            (self.min_pt[1] + self.max_pt[1]) * 0.5,
            (self.min_pt[2] + self.max_pt[2]) * 0.5
        )

def aabb_intersects(box_a: Box3D, box_b: Box3D, margin: float = 0.0) -> bool:
    """
    Tests if two 3D AABBs intersect with optional protective safety margin.
    """
    for i in range(3):
        if (box_a.max_pt[i] + margin < box_b.min_pt[i]) or (box_b.max_pt[i] + margin < box_a.min_pt[i]):
            return False
    return True

def box3d_iou(box_a: Box3D, box_b: Box3D) -> float:
    """
    Calculates volumetric 3D Intersection-over-Union (IoU).
    """
    ix = max(0.0, min(box_a.max_pt[0], box_b.max_pt[0]) - max(box_a.min_pt[0], box_b.min_pt[0]))
    iy = max(0.0, min(box_a.max_pt[1], box_b.max_pt[1]) - max(box_a.min_pt[1], box_b.min_pt[1]))
    iz = max(0.0, min(box_a.max_pt[2], box_b.max_pt[2]) - max(box_a.min_pt[2], box_b.min_pt[2]))
    inter_vol = ix * iy * iz
    if inter_vol <= 0.0:
        return 0.0

    union_vol = box_a.volume + box_b.volume - inter_vol
    return round(inter_vol / union_vol, 4) if union_vol > 0.0 else 0.0

def box3d_distance(box_a: Box3D, box_b: Box3D) -> float:
    """
    Calculates Euclidean surface-to-surface separation distance between two disjoint 3D boxes.
    """
    dx = max(0.0, max(box_a.min_pt[0] - box_b.max_pt[0], box_b.min_pt[0] - box_a.max_pt[0]))
    dy = max(0.0, max(box_a.min_pt[1] - box_b.max_pt[1], box_b.min_pt[1] - box_a.max_pt[1]))
    dz = max(0.0, max(box_a.min_pt[2] - box_b.max_pt[2], box_b.min_pt[2] - box_a.max_pt[2]))
    return round(math.sqrt(dx*dx + dy*dy + dz*dz), 3)


def evaluate_timeline_clearance(
    components: List[Dict[str, Any]],
    progress_steps: int = 15,
    min_clearance_mm: float = 3.0
) -> Dict[str, Any]:
    """
    Simulates exploded view trajectory over t in [0.0, 1.0], verifying non-collision
    and ensuring minimum clearance between adjacent mechanical parts.
    """
    time_points = [i / max(1, progress_steps - 1) for i in range(progress_steps)]
    min_distance_overall = float("inf")
    critical_pair = None
    critical_time = 0.0
    collision_events = []

    for t in time_points:
        boxes_at_t = []
        for c in components:
            cid = c.get("id", "part")
            center = c.get("center", [0.0, 0.0, 0.0])
            size = c.get("size", [10.0, 10.0, 10.0])
            dir_vec = c.get("explosion_direction", [0.0, 1.0, 0.0])
            dist = c.get("explosion_distance", 20.0)

            mag = math.sqrt(sum(x*x for x in dir_vec)) or 1.0
            shift = [x / mag * dist * t for x in dir_vec]
            cur_center = [center[i] + shift[i] for i in range(3)]

            half_w = size[0] * 0.5
            half_h = size[1] * 0.5
            half_d = size[2] * 0.5

            b = Box3D(
                id=cid,
                min_pt=(cur_center[0] - half_w, cur_center[1] - half_h, cur_center[2] - half_d),
                max_pt=(cur_center[0] + half_w, cur_center[1] + half_h, cur_center[2] + half_d)
            )
            boxes_at_t.append(b)

        # Check all unique pairs
        n = len(boxes_at_t)
        for i in range(n):
            for j in range(i + 1, n):
                b1 = boxes_at_t[i]
                b2 = boxes_at_t[j]
                if t > 0.0 and aabb_intersects(b1, b2):
                    overlap_iou = box3d_iou(b1, b2)
                    if overlap_iou > 0.01:
                        collision_events.append({
                            "time": round(t, 2),
                            "part_a": b1.id,
                            "part_b": b2.id,
                            "iou": overlap_iou
                        })
                dist_val = box3d_distance(b1, b2)
                if dist_val < min_distance_overall and t > 0.05:
                    min_distance_overall = dist_val
                    critical_pair = (b1.id, b2.id)
                    critical_time = t

    is_safe = len(collision_events) == 0 and (min_distance_overall >= min_clearance_mm or min_distance_overall == float("inf"))

    return {
        "status": "PASS" if is_safe else "WARNING",
        "is_collision_free": len(collision_events) == 0,
        "min_clearance_mm": round(min_distance_overall, 2) if min_distance_overall != float("inf") else 0.0,
        "critical_time": round(critical_time, 2),
        "critical_pair": critical_pair,
        "collision_count": len(collision_events),
        "collision_events": collision_events[:5]
    }
