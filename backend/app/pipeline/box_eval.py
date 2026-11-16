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
