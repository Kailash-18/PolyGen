"""
Multi-View Texture Blending Engine.
Blends multi-view projected RGB colors across camera overlap boundaries.
"""
from typing import Dict, Any, List
import numpy as np

class MultiViewTextureBlender:
    """Blends multi-view vertex colors and texture patches using weighted Poisson averaging."""
    def __init__(self, blend_power: float = 2.0):
        self.blend_power = blend_power

    def blend_vertex_colors(self, candidate_colors: List[np.ndarray], weights: List[float]) -> np.ndarray:
        """Computes weighted normalized blend of candidate RGB color samples."""
        if not candidate_colors or sum(weights) == 0:
            return np.array([128, 128, 128], dtype=np.uint8)
        
        powered_weights = [w ** self.blend_power for w in weights]
        total_w = sum(powered_weights)
        if total_w < 1e-6:
            return candidate_colors[0].astype(np.uint8)

        accum = np.zeros(3, dtype=np.float32)
        for c, w in zip(candidate_colors, powered_weights):
            accum += c.astype(np.float32) * w
        blended = np.clip(accum / total_w, 0, 255)
        return blended.astype(np.uint8)
