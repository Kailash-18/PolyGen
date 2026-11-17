"""
Stage 4: Physics Collision Hull Generation & Primitive Decomposition
Generates game-ready collision proxies (Convex Hull, OBB, AABB, Capsule, Sphere)
following Unreal Engine UCX_* naming conventions and Unity Collider component specs.
"""

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import math
import numpy as np
import trimesh


@dataclass
class CollisionPrimitiveSpec:
    collider_type: str  # convex_hull, oriented_box, axis_aligned_box, capsule, sphere
    volume: float
    surface_area: float
    vertex_count: int
    face_count: int
    center_of_mass: List[float]
    extents: List[float]
    engine_identifier: str


class CollisionHullGenerator:
    """
    Computes game engine physics collision volumes from 3D visual geometry.
    Supports single and compound convex hulls, oriented bounding boxes (OBB),
    axis-aligned bounding boxes (AABB), and capsule colliders.
    """

    def __init__(self, max_hull_vertices: int = 64):
        self.max_hull_vertices = max_hull_vertices

    def generate_convex_hull(self, mesh: trimesh.Trimesh) -> Tuple[trimesh.Trimesh, CollisionPrimitiveSpec]:
        """
        Computes 3D convex hull wrapper around geometry.
        Simplifies hull if vertex count exceeds engine physics limits.
        """
        raw_hull = mesh.convex_hull
        if len(raw_hull.vertices) > self.max_hull_vertices:
            try:
                simplified = raw_hull.simplify_quadric_decimation(face_count=self.max_hull_vertices * 2)
            except Exception:
                simplified = raw_hull
        else:
            simplified = raw_hull

        vol = float(simplified.volume) if hasattr(simplified, "volume") else 0.0
        area = float(simplified.area) if hasattr(simplified, "area") else 0.0
        com = [float(x) for x in simplified.center_mass]
        extents = [float(x) for x in (simplified.bounds[1] - simplified.bounds[0])]

        spec = CollisionPrimitiveSpec(
            collider_type="convex_hull",
            volume=round(vol, 5),
            surface_area=round(area, 5),
            vertex_count=len(simplified.vertices),
            face_count=len(simplified.faces),
            center_of_mass=com,
            extents=extents,
            engine_identifier="UCX_ConvexHull_01"
        )
        return simplified, spec
