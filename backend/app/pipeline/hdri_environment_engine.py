"""
Stage 3: HDRI Environmental Lighting & Cubemap Engine.
Projects 360 equirectangular HDR maps onto cubemaps and computes PMREM specular reflections.
"""

from typing import Tuple, Dict, Any, List, Optional
import numpy as np

class HDRIEnvironmentEngine:
    """Computes IBL cubemaps and spherical harmonics from 360-degree equirectangular maps."""

    def __init__(self, cubemap_resolution: int = 256):
        self.cubemap_resolution = cubemap_resolution

    def cartesian_to_equirectangular_uv(self, dir_vec: np.ndarray) -> Tuple[float, float]:
        """
        Converts 3D Cartesian direction vector [x, y, z] to normalized equirectangular UV [u, v].
        u in [0, 1], v in [0, 1].
        """
        norm = np.linalg.norm(dir_vec)
        if norm < 1e-12:
            return 0.5, 0.5
        v = dir_vec / norm

        phi = np.arctan2(v[2], v[0])  # Azimuth: [-pi, pi]
        theta = np.arcsin(np.clip(v[1], -1.0, 1.0))  # Elevation: [-pi/2, pi/2]

        u = float((phi + np.pi) / (2.0 * np.pi))
        v_coord = float((theta + np.pi * 0.5) / np.pi)
        return float(np.clip(u, 0.0, 1.0)), float(np.clip(v_coord, 0.0, 1.0))

    def generate_cubemap_face_directions(self, face_index: int) -> np.ndarray:
        """
        Generates 3D direction vectors for each texel of a specific cubemap face.
        Faces: 0:+X, 1:-X, 2:+Y, 3:-Y, 4:+Z, 5:-Z.
        """
        res = self.cubemap_resolution
        u_coords = np.linspace(-1.0, 1.0, res)
        v_coords = np.linspace(-1.0, 1.0, res)
        uu, vv = np.meshgrid(u_coords, v_coords)

        dirs = np.zeros((res, res, 3), dtype=np.float32)
        if face_index == 0:    # +X
            dirs[:, :, 0] = 1.0; dirs[:, :, 1] = -vv; dirs[:, :, 2] = -uu
        elif face_index == 1:  # -X
            dirs[:, :, 0] = -1.0; dirs[:, :, 1] = -vv; dirs[:, :, 2] = uu
        elif face_index == 2:  # +Y
            dirs[:, :, 0] = uu; dirs[:, :, 1] = 1.0; dirs[:, :, 2] = vv
        elif face_index == 3:  # -Y
            dirs[:, :, 0] = uu; dirs[:, :, 1] = -1.0; dirs[:, :, 2] = -vv
        elif face_index == 4:  # +Z
            dirs[:, :, 0] = uu; dirs[:, :, 1] = -vv; dirs[:, :, 2] = 1.0
        elif face_index == 5:  # -Z
            dirs[:, :, 0] = -uu; dirs[:, :, 1] = -vv; dirs[:, :, 2] = -1.0

        # Normalize direction vectors
        norms = np.linalg.norm(dirs, axis=2, keepdims=True)
        dirs = dirs / np.maximum(norms, 1e-12)
        return dirs
