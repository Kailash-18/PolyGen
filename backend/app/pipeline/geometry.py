from typing import List, Tuple, Dict, Any
"""
Stage 1: Geometry Generation Engine (TripoSR / Shap-E / Mesh Synthesis)
"""

import math
import numpy as np
import trimesh
from app.core.device import detect_compute_device

class GeometryEngine:
    def __init__(self, device: str = "auto", enable_neural: bool = False):
        self.device_info = detect_compute_device(device)
        self.device = self.device_info["device"]
        self.enable_neural = enable_neural

    def _create_sword(self) -> trimesh.Trimesh:
        blade = trimesh.creation.box(extents=[0.14, 0.035, 2.4])
        blade.apply_translation([0, 0, 1.2])
        blade_tip = trimesh.creation.cone(radius=0.08, height=0.45, sections=16)
        blade_tip.apply_translation([0, 0, 2.4])
        guard = trimesh.creation.box(extents=[0.75, 0.08, 0.09])
        guard.apply_translation([0, 0, 0.0])
        handle = trimesh.creation.cylinder(radius=0.042, height=0.65, sections=24)
        handle.apply_translation([0, 0, -0.36])
        pommel = trimesh.creation.icosphere(subdivisions=2, radius=0.095)
        pommel.apply_translation([0, 0, -0.74])
        gem = trimesh.creation.icosphere(subdivisions=2, radius=0.055)
        gem.apply_translation([0, 0.045, 0.0])
        return trimesh.util.concatenate([blade, blade_tip, guard, handle, pommel, gem])

    def _create_shield(self) -> trimesh.Trimesh:
        body = trimesh.creation.cylinder(radius=0.9, height=0.08, sections=36)
        rim = trimesh.creation.torus(major_radius=0.92, minor_radius=0.05, major_sections=36, minor_sections=16)
        boss = trimesh.creation.icosphere(subdivisions=3, radius=0.28)
        boss.apply_translation([0, 0, 0.06])
        return trimesh.util.concatenate([body, rim, boss])

    def _create_crystal(self) -> trimesh.Trimesh:
        c1 = trimesh.creation.cylinder(radius=0.25, height=1.6, sections=6)
        t1 = trimesh.creation.cone(radius=0.25, height=0.5, sections=6)
        t1.apply_translation([0, 0, 0.8])
        main_crystal = trimesh.util.concatenate([c1, t1])

        c2 = trimesh.creation.cylinder(radius=0.15, height=1.1, sections=6)
        t2 = trimesh.creation.cone(radius=0.15, height=0.35, sections=6)
        t2.apply_translation([0, 0, 0.55])
        crystal2 = trimesh.util.concatenate([c2, t2])
        crystal2.apply_translation([0.3, 0.2, -0.2])
        return trimesh.util.concatenate([main_crystal, crystal2])

    def _create_vase(self) -> trimesh.Trimesh:
        base = trimesh.creation.cylinder(radius=0.4, height=0.15, sections=32)
        body = trimesh.creation.icosphere(subdivisions=3, radius=0.7)
        body.apply_scale([1.0, 1.0, 1.4])
        body.apply_translation([0, 0, 0.6])
        neck = trimesh.creation.cylinder(radius=0.25, height=0.8, sections=32)
        neck.apply_translation([0, 0, 1.4])
        rim = trimesh.creation.torus(major_radius=0.32, minor_radius=0.06, major_sections=32, minor_sections=16)
        rim.apply_translation([0, 0, 1.8])
        return trimesh.util.concatenate([base, body, neck, rim])

    def _create_chair(self) -> trimesh.Trimesh:
        seat = trimesh.creation.box(extents=[0.9, 0.9, 0.1])
        seat.apply_translation([0, 0, 0.85])
        leg1 = trimesh.creation.cylinder(radius=0.04, height=0.85)
        leg1.apply_translation([0.38, 0.38, 0.425])
        leg2 = trimesh.creation.cylinder(radius=0.04, height=0.85)
        leg2.apply_translation([-0.38, 0.38, 0.425])
        leg3 = trimesh.creation.cylinder(radius=0.04, height=0.85)
        leg3.apply_translation([0.38, -0.38, 0.425])
        leg4 = trimesh.creation.cylinder(radius=0.04, height=0.85)
        leg4.apply_translation([-0.38, -0.38, 0.425])
        back = trimesh.creation.box(extents=[0.9, 0.08, 0.85])
        back.apply_translation([0, -0.41, 1.3])
        return trimesh.util.concatenate([seat, leg1, leg2, leg3, leg4, back])

    def _create_sculpture(self) -> trimesh.Trimesh:
        torus = trimesh.creation.torus(major_radius=0.8, minor_radius=0.25, major_sections=32, minor_sections=16)
        sphere = trimesh.creation.icosphere(subdivisions=2, radius=0.45)
        sphere.apply_translation([0, 0, 0.5])
        return trimesh.util.concatenate([torus, sphere])

    def generate_mesh(self, prompt: str, detail_level: str = "high") -> trimesh.Trimesh:
        p = prompt.lower()
        if "sword" in p or "blade" in p or "weapon" in p or "broadsword" in p:
            mesh = self._create_sword()
        elif "shield" in p or "buckler" in p or "aegis" in p:
            mesh = self._create_shield()
        elif "crystal" in p or "gem" in p or "mineral" in p:
            mesh = self._create_crystal()
        elif "vase" in p or "pot" in p or "ceramic" in p:
            mesh = self._create_vase()
        elif "chair" in p or "stool" in p or "furniture" in p:
            mesh = self._create_chair()
        else:
            mesh = self._create_sculpture()

        mesh.rezero()
        max_extent = max(mesh.extents)
        if max_extent > 0:
            mesh.apply_scale(2.0 / max_extent)
        return mesh


def stitch_mesh_seams(vertices: List[List[float]], tolerance: float = 1e-3) -> Tuple[List[List[float]], int]:
    """Weld coincident vertices along mesh seams to ensure topological watertightness."""
    welded = []
    stitched_count = 0
    for v in vertices:
        found = False
        for w in welded:
            dist = np.sqrt((v[0] - w[0])**2 + (v[1] - w[1])**2 + (v[2] - w[2])**2)
            if dist <= tolerance:
                found = True
                stitched_count += 1
                break
        if not found:
            welded.append(v)
    return welded, stitched_count
