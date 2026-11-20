"""
ControlNet Depth Map Normalization and Preprocessing Pipeline.
Encodes raw floating point depth buffers into uint8 grayscale representations.
"""
from typing import Dict, Any, List
import numpy as np

class ControlNetDepthPreprocessor:
    """Preprocesses depth buffers for Stable Diffusion ControlNet conditioning."""
    def __init__(self, target_resolution: int = 512):
        self.target_resolution = target_resolution

    def encode_depth_map_uint8(self, depth_float: np.ndarray) -> np.ndarray:
        """Converts normalized float32 depth map into 8-bit grayscale image."""
        clipped = np.clip(depth_float, 0.0, 1.0)
        # Invert so near geometry is white (255) and far/background is black (0)
        inverted = 1.0 - clipped
        return (inverted * 255.0).astype(np.uint8)

    def extract_depth_features(self, depth_uint8: np.ndarray) -> Dict[str, Any]:
        """Extracts statistical depth histogram and edge gradient metrics."""
        return {
            "mean_depth": float(np.mean(depth_uint8)),
            "std_depth": float(np.std(depth_uint8)),
            "foreground_ratio": float(np.count_nonzero(depth_uint8 > 5) / depth_uint8.size),
            "resolution": depth_uint8.shape
        }
