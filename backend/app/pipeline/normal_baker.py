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

    def compute_tangent_basis(
        self,
        vertices: np.ndarray,
        faces: np.ndarray,
        uvs: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Calculates per-vertex tangent and bitangent vectors from UV parameterization."""
        num_verts = len(vertices)
        tangents = np.zeros((num_verts, 3), dtype=np.float64)
        bitangents = np.zeros((num_verts, 3), dtype=np.float64)

        if len(uvs) < num_verts:
            tangents[:, 0] = 1.0
            bitangents[:, 1] = 1.0
            return tangents, bitangents

        for f in faces:
            i0, i1, i2 = f[0], f[1], f[2]
            v0, v1, v2 = vertices[i0], vertices[i1], vertices[i2]
            w0, w1, w2 = uvs[i0], uvs[i1], uvs[i2]

            e1 = v1 - v0
            e2 = v2 - v0
            du1, dv1 = w1[0] - w0[0], w1[1] - w0[1]
            du2, dv2 = w2[0] - w0[0], w2[1] - w0[1]

            det = du1 * dv2 - du2 * dv1
            if abs(det) > 1e-12:
                inv_det = 1.0 / det
                t = (e1 * dv2 - e2 * dv1) * inv_det
                b = (e2 * du1 - e1 * du2) * inv_det
                tangents[i0] += t; tangents[i1] += t; tangents[i2] += t
                bitangents[i0] += b; bitangents[i1] += b; bitangents[i2] += b

        # Orthonormalize tangents
        for i in range(num_verts):
            t_len = np.linalg.norm(tangents[i])
            if t_len > 1e-12:
                tangents[i] /= t_len
            else:
                tangents[i] = np.array([1.0, 0.0, 0.0])

            b_len = np.linalg.norm(bitangents[i])
            if b_len > 1e-12:
                bitangents[i] /= b_len
            else:
                bitangents[i] = np.array([0.0, 1.0, 0.0])

        return tangents, bitangents

    def bake_normal_map(
        self,
        high_poly_verts: np.ndarray,
        high_poly_normals: np.ndarray,
        low_poly_verts: np.ndarray,
        low_poly_normals: np.ndarray
    ) -> np.ndarray:
        """Projects high-poly vertex normals onto low-poly surface space."""
        normal_map = np.zeros((self.resolution, self.resolution, 3), dtype=np.uint8)
        normal_map[:, :, 0] = 128
        normal_map[:, :, 1] = 128
        normal_map[:, :, 2] = 255

        if len(high_poly_verts) == 0 or len(low_poly_verts) == 0:
            return normal_map

        tree = KDTree(high_poly_verts)
        dists, indices = tree.query(low_poly_verts, k=1)
        high_normals = high_poly_normals[indices]
        delta_normals = high_normals - low_poly_normals

        sample_step = max(1, self.resolution // max(len(low_poly_verts), 1))
        for i, delta in enumerate(delta_normals[:min(len(delta_normals), self.resolution)]):
            px = (i * sample_step) % self.resolution
            py = ((i * sample_step) // self.resolution) % self.resolution
            n_vec = delta + np.array([0.0, 0.0, 1.0])
            n_vec = n_vec / (np.linalg.norm(n_vec) + 1e-12)
            normal_map[py, px, 0] = int(np.clip((n_vec[0] * 0.5 + 0.5) * 255, 0, 255))
            normal_map[py, px, 1] = int(np.clip((n_vec[1] * 0.5 + 0.5) * 255, 0, 255))
            normal_map[py, px, 2] = int(np.clip((n_vec[2] * 0.5 + 0.5) * 255, 0, 255))

        return normal_map
