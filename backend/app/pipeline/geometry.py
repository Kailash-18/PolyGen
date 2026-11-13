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
        print(f"[GeometryEngine] Initialized on device: {self.device}")

    def _marching_cubes_sdf(self, sdf_func, bounds=((-1, 1), (-1, 1), (-1, 1)), resolution=48) -> trimesh.Trimesh:
        """Extracts triangular isosurface from volumetric Signed Distance Function grid"""
        x = np.linspace(bounds[0][0], bounds[0][1], resolution)
        y = np.linspace(bounds[1][0], bounds[1][1], resolution)
        z = np.linspace(bounds[2][0], bounds[2][1], resolution)
        X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
        values = sdf_func(X, Y, Z)

        try:
            from skimage import measure
            verts, faces, normals, _ = measure.marching_cubes(values, level=0.0, spacing=(
                (bounds[0][1] - bounds[0][0]) / (resolution - 1),
                (bounds[1][1] - bounds[1][0]) / (resolution - 1),
                (bounds[2][1] - bounds[2][0]) / (resolution - 1),
            ))
            verts[:, 0] += bounds[0][0]
            verts[:, 1] += bounds[1][0]
            verts[:, 2] += bounds[2][0]
            return trimesh.Trimesh(vertices=verts, faces=faces, vertex_normals=normals)
        except ImportError:
            return trimesh.creation.icosphere(subdivisions=3, radius=1.0)
