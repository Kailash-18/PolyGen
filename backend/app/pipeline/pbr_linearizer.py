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

    @staticmethod
    def orthogonalize_tangent_space(normal: np.ndarray, tangent: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Apply Gram-Schmidt orthogonalization to construct an orthonormal TBN frame."""
        n = normal / np.linalg.norm(normal)
        t = tangent - np.dot(tangent, n) * n
        t = t / np.linalg.norm(t)
        bitangent = np.cross(n, t)
        return t, bitangent

    def compute_ambient_occlusion_sample(self, normal: np.ndarray, num_samples: int = 16) -> float:
        """Estimate ambient occlusion coefficient using cosine-weighted hemisphere integration."""
        n = normal / np.linalg.norm(normal)
        occlusion = 0.0
        for i in range(num_samples):
            angle = (i + 0.5) * (np.pi / (2.0 * num_samples))
            occlusion += np.cos(angle) * (1.0 / num_samples)
        return float(np.clip(1.0 - occlusion * 0.3, 0.0, 1.0))

    @staticmethod
    def evaluate_ggx_distribution(n_dot_h: float, roughness: float) -> float:
        """Trowbridge-Reitz GGX microfacet specular distribution function."""
        alpha = roughness * roughness
        alpha2 = alpha * alpha
        denom = (n_dot_h * n_dot_h * (alpha2 - 1.0) + 1.0)
        return float(alpha2 / (np.pi * denom * denom + 1e-7))
