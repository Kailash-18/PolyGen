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
