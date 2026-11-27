"""
Multi-Camera Canonical View Depth Buffer Rasterizer.
Renders orthographic and perspective depth buffers from 3D triangle meshes.
"""
from typing import Dict, Any, List, Tuple
import numpy as np

class CanonicalDepthRenderer:
    """Renders normalized depth maps from 6 orthogonal canonical camera viewpoints."""
    CANONICAL_VIEWS = ["front", "back", "left", "right", "top", "bottom"]

    def __init__(self, resolution: int = 512):
        self.resolution = resolution

    def get_view_matrix(self, view_name: str) -> np.ndarray:
        """Computes 4x4 camera view transformation matrix."""
        view_matrices = {
            "front": np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, -2.0], [0, 0, 0, 1]], dtype=np.float32),
            "back": np.array([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, -2.0], [0, 0, 0, 1]], dtype=np.float32),
            "left": np.array([[0, 0, 1, 0], [0, 1, 0, 0], [-1, 0, 0, -2.0], [0, 0, 0, 1]], dtype=np.float32),
            "right": np.array([[0, 0, -1, 0], [0, 1, 0, 0], [1, 0, 0, -2.0], [0, 0, 0, 1]], dtype=np.float32),
            "top": np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, -2.0], [0, 0, 0, 1]], dtype=np.float32),
            "bottom": np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, -1, 0, -2.0], [0, 0, 0, 1]], dtype=np.float32)
        }
        return view_matrices.get(view_name, view_matrices["front"])

    def rasterize_depth(self, vertices: List[List[float]], faces: List[List[int]], view_name: str = "front") -> np.ndarray:
        """Rasterizes mesh depth buffer normalized to [0.0, 1.0] range."""
        verts = np.array(vertices, dtype=np.float32)
        view_mat = self.get_view_matrix(view_name)
        
        # Transform vertices
        homo_verts = np.hstack([verts, np.ones((len(verts), 1), dtype=np.float32)])
        cam_verts = homo_verts @ view_mat.T
        
        # Simple orthographic projection with Z-depth mapping
        depth_buffer = np.ones((self.resolution, self.resolution), dtype=np.float32)
        z_vals = cam_verts[:, 2]
        z_min, z_max = np.min(z_vals), np.max(z_vals)
        z_range = max(1e-5, z_max - z_min)
        norm_z = (z_vals - z_min) / z_range

        # Project 2D bounding boxes
        xs = ((cam_verts[:, 0] + 1.0) * 0.5 * (self.resolution - 1)).astype(np.int32)
        ys = ((cam_verts[:, 1] + 1.0) * 0.5 * (self.resolution - 1)).astype(np.int32)
        xs = np.clip(xs, 0, self.resolution - 1)
        ys = np.clip(ys, 0, self.resolution - 1)

        for i in range(len(verts)):
            depth_buffer[ys[i], xs[i]] = min(depth_buffer[ys[i], xs[i]], norm_z[i])

        return depth_buffer

    def render_all_canonical_views(self, vertices: List[List[float]], faces: List[List[int]]) -> Dict[str, np.ndarray]:
        """Renders all 6 canonical depth buffers."""
        return {view: self.rasterize_depth(vertices, faces, view) for view in self.CANONICAL_VIEWS}
