"""
Stage 3: Image-Based Lighting (IBL) & Radiance Probe Engine.
Evaluates 9-coefficient Spherical Harmonics (SH) irradiance and split-sum specular BRDF LUT.
"""

from typing import Tuple, Dict, Any, List, Optional
import numpy as np

class RadianceProbe:
    """Computes diffuse and specular ambient environmental lighting for Three.js WebGL scenes."""

    def __init__(self):
        # Default neutral outdoor studio 9-coefficient SH basis
        self.default_sh = np.array([
            0.79, 0.44, 0.54, -0.38, -0.34, -0.29,
            -0.11, -0.26, -0.16
        ], dtype=np.float32)

    def evaluate_sh_irradiance(
        self,
        normal: np.ndarray,
        sh_coefficients: Optional[np.ndarray] = None
    ) -> float:
        """
        Evaluates diffuse irradiance from unit surface normal using L0, L1, L2 Spherical Harmonics:
        E(n) = c1*L00 + c2*(L1-1*y + L10*z + L11*x) + c3*L20*(3z^2 - 1) + ...
        """
        sh = sh_coefficients if sh_coefficients is not None else self.default_sh
        norm_len = np.linalg.norm(normal)
        if norm_len < 1e-12:
            n = np.array([0.0, 1.0, 0.0], dtype=np.float64)
        else:
            n = normal / norm_len

        x, y, z = n[0], n[1], n[2]

        # 9 SH basis functions evaluation constants
        c1 = 0.282095
        c2 = 0.488603
        c3 = 0.315392
        c4 = 1.092548
        c5 = 0.546274

        irradiance = (
            c1 * sh[0] +
            c2 * (sh[1] * y + sh[2] * z + sh[3] * x) +
            c3 * sh[4] * (3.0 * z * z - 1.0) +
            c4 * (sh[5] * x * y + sh[6] * y * z + sh[7] * x * z) +
            c5 * sh[8] * (x * x - y * y)
        )

        return float(np.clip(irradiance, 0.0, 5.0))
