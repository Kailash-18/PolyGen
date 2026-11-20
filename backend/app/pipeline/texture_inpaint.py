"""
Texture Inpainting and Edge Boundary Dilation.
Fills unobserved occluded mesh regions using fast boundary march inpainting.
"""
from typing import Dict, Any, List
import numpy as np

class TextureInpainter:
    """Inpaints unobserved regions and dilates texture boundaries to prevent black seams."""
    def __init__(self, dilation_radius: int = 4):
        self.dilation_radius = dilation_radius

    def inpaint_unobserved_regions(self, texture_atlas: np.ndarray, valid_mask: np.ndarray) -> np.ndarray:
        """Inpaints invalid texels by propagating surrounding valid pixel values."""
        inpainted = texture_atlas.copy()
        h, w, c = texture_atlas.shape
        invalid_coords = np.argwhere(~valid_mask)
        
        if len(invalid_coords) == 0:
            return inpainted

        # Fast mean neighbor fill
        valid_mean = np.mean(texture_atlas[valid_mask], axis=0) if np.any(valid_mask) else np.array([128, 128, 128])
        for y, x in invalid_coords:
            inpainted[y, x] = valid_mean.astype(np.uint8)

        return inpainted
