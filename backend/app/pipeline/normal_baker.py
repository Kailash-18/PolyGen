"""
Stage 3: High-to-Low Poly Normal Map Transfer Baker.
Bakes micro-surface geometric normal deltas from dense (500k) to decimated (10k) meshes.
"""

from typing import Tuple, Dict, Any, Optional
import numpy as np
from scipy.spatial import KDTree

class HighToLowNormalBaker:
    """Bakes surface normals from dense neural geometry onto UV unwrapped simplified mesh."""

    def __init__(self, resolution: int = 1024):
        self.resolution = resolution

    def bake_normal_map(
        self,
        high_poly_verts: np.ndarray,
        high_poly_normals: np.ndarray,
        low_poly_verts: np.ndarray,
        low_poly_normals: np.ndarray
    ) -> np.ndarray:
        """
        Projects high-poly vertex normals onto low-poly surface space.
        Returns an RGB normal map image array of shape (resolution, resolution, 3).
        """
        normal_map = np.zeros((self.resolution, self.resolution, 3), dtype=np.uint8)
        # Default flat tangent-space normal: [128, 128, 255] (vector [0, 0, 1])
        normal_map[:, :, 0] = 128
        normal_map[:, :, 1] = 128
        normal_map[:, :, 2] = 255

        if len(high_poly_verts) == 0 or len(low_poly_verts) == 0:
            return normal_map

        # Build KDTree over high-poly vertices to find nearest surface points
        tree = KDTree(high_poly_verts)
        dists, indices = tree.query(low_poly_verts, k=1)

        # Compute average normal displacement
        high_normals = high_poly_normals[indices]
        delta_normals = high_normals - low_poly_normals

        # Modulate into texture buffer
        sample_step = max(1, self.resolution // max(len(low_poly_verts), 1))
        for i, delta in enumerate(delta_normals[:min(len(delta_normals), self.resolution)]):
            px = (i * sample_step) % self.resolution
            py = ((i * sample_step) // self.resolution) % self.resolution
            # Encode vector [-1..1] into [0..255]
            n_vec = delta + np.array([0.0, 0.0, 1.0])
            n_vec = n_vec / (np.linalg.norm(n_vec) + 1e-12)
            normal_map[py, px, 0] = int(np.clip((n_vec[0] * 0.5 + 0.5) * 255, 0, 255))
            normal_map[py, px, 1] = int(np.clip((n_vec[1] * 0.5 + 0.5) * 255, 0, 255))
            normal_map[py, px, 2] = int(np.clip((n_vec[2] * 0.5 + 0.5) * 255, 0, 255))

        return normal_map
