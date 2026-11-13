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
