"""
PBR Texture Color Space & Physical Property Linearizer.
Converts non-linear gamma sRGB textures to linear Rec.709 photometric space.
"""
from typing import Dict, Any, List, Tuple
import numpy as np

class PBRColorSpaceLinearizer:
    """Manages color space gamma transformations for PBR textures."""
    
    @staticmethod
    def srgb_to_linear(value: float) -> float:
        """Convert single channel sRGB value in [0, 1] to linear radiometric space."""
        if value <= 0.04045:
            return float(value / 12.92)
        else:
            return float(((value + 0.055) / 1.055) ** 2.4)

    @staticmethod
    def linear_to_srgb(value: float) -> float:
        """Convert single channel linear value in [0, 1] to display sRGB."""
        if value <= 0.0031308:
            return float(value * 12.92)
        else:
            return float(1.055 * (value ** (1.0 / 2.4)) - 0.055)

    def process_albedo_buffer(self, rgb_array: np.ndarray) -> np.ndarray:
        """Linearize a complete 2D/3D RGB texture array."""
        norm = np.clip(rgb_array.astype(np.float32) / 255.0, 0.0, 1.0)
        mask = norm <= 0.04045
        linear = np.where(mask, norm / 12.92, ((norm + 0.055) / 1.055) ** 2.4)
        return (linear * 255.0).astype(np.uint8)
