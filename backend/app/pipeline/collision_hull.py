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

    def generate_oriented_bounding_box(self, mesh: trimesh.Trimesh) -> Tuple[trimesh.Trimesh, CollisionPrimitiveSpec]:
        """
        Computes minimal oriented bounding box (OBB) aligned with principal geometric axes.
        """
        obb = mesh.bounding_box_oriented
        vol = float(obb.volume)
        area = float(obb.area)
        com = [float(x) for x in obb.center_mass]
        extents = [float(x) for x in obb.extents]

        spec = CollisionPrimitiveSpec(
            collider_type="oriented_box",
            volume=round(vol, 5),
            surface_area=round(area, 5),
            vertex_count=len(obb.vertices),
            face_count=len(obb.faces),
            center_of_mass=com,
            extents=extents,
            engine_identifier="UBX_OrientedBox_01"
        )
        return obb, spec

    def generate_axis_aligned_box(self, mesh: trimesh.Trimesh) -> Tuple[trimesh.Trimesh, CollisionPrimitiveSpec]:
        """
        Computes world-axis aligned bounding box (AABB).
        """
        aabb = mesh.bounding_box
        vol = float(aabb.volume)
        area = float(aabb.area)
        com = [float(x) for x in aabb.center_mass]
        extents = [float(x) for x in aabb.extents]

        spec = CollisionPrimitiveSpec(
            collider_type="axis_aligned_box",
            volume=round(vol, 5),
            surface_area=round(area, 5),
            vertex_count=len(aabb.vertices),
            face_count=len(aabb.faces),
            center_of_mass=com,
            extents=extents,
            engine_identifier="UBX_AABB_01"
        )
        return aabb, spec

    def generate_bounding_capsule(self, mesh: trimesh.Trimesh) -> Tuple[trimesh.Trimesh, CollisionPrimitiveSpec]:
        """
        Approximates character/prop capsule collider along the dominant principal axis (Z).
        """
        extents = mesh.extents
        # Dominant height along Z
        height = float(extents[2])
        # Radius from max lateral extent
        radius = float(max(extents[0], extents[1]) / 2.0)
        cylinder_height = max(0.01, height - (2.0 * radius))

        capsule_mesh = trimesh.creation.capsule(height=cylinder_height, radius=radius, count=[16, 16])
        capsule_mesh.apply_translation(mesh.center_mass)

        vol = float(capsule_mesh.volume)
        area = float(capsule_mesh.area)

        spec = CollisionPrimitiveSpec(
            collider_type="capsule",
            volume=round(vol, 5),
            surface_area=round(area, 5),
            vertex_count=len(capsule_mesh.vertices),
            face_count=len(capsule_mesh.faces),
            center_of_mass=[float(x) for x in capsule_mesh.center_mass],
            extents=[radius * 2.0, radius * 2.0, height],
            engine_identifier="UCP_Capsule_01"
        )
        return capsule_mesh, spec

    def generate_all_colliders(self, mesh: trimesh.Trimesh) -> Dict[str, Any]:
        """
        Generates full collision manifest with convex hull, OBB, AABB, and capsule.
        """
        hull_mesh, hull_spec = self.generate_convex_hull(mesh)
        obb_mesh, obb_spec = self.generate_oriented_bounding_box(mesh)
        aabb_mesh, aabb_spec = self.generate_axis_aligned_box(mesh)
        cap_mesh, cap_spec = self.generate_bounding_capsule(mesh)

        return {
            "meshes": {
                "convex_hull": hull_mesh,
                "oriented_box": obb_mesh,
                "axis_aligned_box": aabb_mesh,
                "capsule": cap_mesh
            },
            "manifest": {
                "convex_hull": asdict(hull_spec),
                "oriented_box": asdict(obb_spec),
                "axis_aligned_box": asdict(aabb_spec),
                "capsule": asdict(cap_spec)
            },
            "recommended_primary": "convex_hull" if hull_spec.vertex_count <= 48 else "oriented_box"
        }

    def export_unreal_collision_file(
        self,
        output_dir: Path,
        asset_name: str,
        colliders: Dict[str, trimesh.Trimesh]
    ) -> str:
        """
        Exports collision meshes using Unreal Engine convention:
          UCX_AssetName_01.obj (Convex Hull)
          UBX_AssetName_01.obj (Box)
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        primary_hull = colliders.get("convex_hull") or colliders.get("oriented_box")
        collision_path = output_dir / f"UCX_{asset_name}_01.obj"
        if primary_hull:
            primary_hull.export(str(collision_path), file_type="obj")
        return str(collision_path)
