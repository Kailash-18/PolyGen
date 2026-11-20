"""
Multi-View 3D-to-2D Back-Projection Engine.
Projects 2D diffusion textures back onto 3D mesh surface vertices.
"""
from typing import Dict, Any, List, Tuple
import numpy as np

class MultiViewProjector:
    """Maps multi-camera 2D textures onto 3D triangle mesh vertices."""
    def __init__(self, texture_size: int = 512):
        self.texture_size = texture_size

    def project_point_to_camera(self, vertex: np.ndarray, view_matrix: np.ndarray) -> Tuple[float, float, float]:
        """Projects single 3D world coordinate into camera UV screen space and depth."""
        homo = np.array([vertex[0], vertex[1], vertex[2], 1.0], dtype=np.float32)
        cam = homo @ view_matrix.T
        u = (cam[0] + 1.0) * 0.5
        v = (cam[1] + 1.0) * 0.5
        depth = cam[2]
        return float(u), float(v), float(depth)

    def compute_view_normal_weight(self, normal: np.ndarray, camera_dir: np.ndarray) -> float:
        """Evaluates cosine incident angle between surface normal and camera ray."""
        norm_n = normal / max(1e-6, np.linalg.norm(normal))
        norm_c = camera_dir / max(1e-6, np.linalg.norm(camera_dir))
        dot = float(np.dot(norm_n, norm_c))
        # Clamp grazing angles to prevent projection stretching
        return max(0.0, dot) if dot > 0.1 else 0.0
