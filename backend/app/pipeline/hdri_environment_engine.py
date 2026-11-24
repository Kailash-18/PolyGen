"""
Stage 3: HDRI Environmental Lighting & Cubemap Engine.
Projects 360 equirectangular HDR maps onto cubemaps and computes PMREM specular reflections.
"""

from typing import Tuple, Dict, Any, List, Optional
import numpy as np

class HDRIEnvironmentEngine:
    """Computes IBL cubemaps and spherical harmonics from 360-degree equirectangular maps."""

    def __init__(self, cubemap_resolution: int = 256, mip_levels: int = 6):
        self.cubemap_resolution = cubemap_resolution
        self.mip_levels = mip_levels

    def cartesian_to_equirectangular_uv(self, dir_vec: np.ndarray) -> Tuple[float, float]:
        """Converts 3D Cartesian direction vector to normalized equirectangular UV [u, v]."""
        norm = np.linalg.norm(dir_vec)
        if norm < 1e-12:
            return 0.5, 0.5
        v = dir_vec / norm

        phi = np.arctan2(v[2], v[0])
        theta = np.arcsin(np.clip(v[1], -1.0, 1.0))

        u = float((phi + np.pi) / (2.0 * np.pi))
        v_coord = float((theta + np.pi * 0.5) / np.pi)
        return float(np.clip(u, 0.0, 1.0)), float(np.clip(v_coord, 0.0, 1.0))

    def generate_cubemap_face_directions(self, face_index: int) -> np.ndarray:
        """Generates 3D direction vectors for each texel of a specific cubemap face."""
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

        norms = np.linalg.norm(dirs, axis=2, keepdims=True)
        dirs = dirs / np.maximum(norms, 1e-12)
        return dirs

    def compute_pmrem_mip_levels(self) -> Dict[int, Dict[str, Any]]:
        """
        Calculates PMREM mip-chain metadata:
        Mip 0: Roughness 0.0 (mirror specular reflection)
        Mip N: Roughness 1.0 (fully diffuse environmental irradiance)
        """
        mips = {}
        for mip in range(self.mip_levels):
            roughness = round(mip / float(self.mip_levels - 1), 3)
            resolution = max(8, self.cubemap_resolution >> mip)
            mips[mip] = {
                "mip_level": mip,
                "roughness": roughness,
                "resolution": resolution,
                "filter_kernel": "GGX_importance_sampling" if mip > 0 else "unfiltered_mirror"
            }
        return mips
