"""
Stage 3: Real-Time HDR Tone Mapping & Dynamic Range Operators.
Applies ACES Filmic, AgX, and Reinhard dynamic range compression.
"""

from typing import Tuple, Dict, Any, List
import numpy as np

class Tonemapper:
    """Tone mapping curves for converting HDR scene radiance into SDR monitor color space."""

    def __init__(self, exposure: float = 1.0, bloom_threshold: float = 1.2):
        self.exposure = exposure
        self.bloom_threshold = bloom_threshold

    def apply_aces_filmic(self, color_rgb: np.ndarray) -> np.ndarray:
        """Narkowicz ACES Filmic tone mapping operator."""
        x = np.maximum(color_rgb * self.exposure, 0.0)
        a = 2.51
        b = 0.03
        c = 2.43
        d = 0.59
        e = 0.14
        mapped = (x * (a * x + b)) / (x * (c * x + d) + e)
        return np.clip(mapped, 0.0, 1.0)

    def apply_reinhard(self, color_rgb: np.ndarray) -> np.ndarray:
        """Simple Reinhard tone mapping: y = x / (1 + x)."""
        x = np.maximum(color_rgb * self.exposure, 0.0)
        return x / (1.0 + x)

    def apply_agx(self, color_rgb: np.ndarray) -> np.ndarray:
        """AgX neutral color tone curve with smooth highlight rolloff."""
        x = np.maximum(color_rgb * self.exposure, 0.0)
        log_val = np.log2(np.maximum(x, 1e-4))
        norm_log = (log_val + 10.0) / 16.5
        clamped_log = np.clip(norm_log, 0.0, 1.0)
        agx_curve = clamped_log * clamped_log * (3.0 - 2.0 * clamped_log)
        return np.clip(agx_curve, 0.0, 1.0)

    def extract_bloom_mask(self, hdr_image: np.ndarray) -> np.ndarray:
        """
        Isolates bright pixels exceeding bloom luminance threshold:
        Luminance = 0.2126*R + 0.7152*G + 0.0722*B.
        """
        lum = (
            0.2126 * hdr_image[:, :, 0] +
            0.7152 * hdr_image[:, :, 1] +
            0.0722 * hdr_image[:, :, 2]
        )
        mask = lum > self.bloom_threshold
        bloom_pixels = np.zeros_like(hdr_image)
        bloom_pixels[mask] = hdr_image[mask] - self.bloom_threshold
        return bloom_pixels
