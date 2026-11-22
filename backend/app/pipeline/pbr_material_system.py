"""
Stage 3: Enterprise PBR Material System & Texture Packing Engine.
Compiles Three.js WebGL shader parameters and packs ORM (Occlusion/Roughness/Metallic) textures.
"""

from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass, asdict
import numpy as np

@dataclass
class PBRMaterialProfile:
    """Standardized Physically Based Rendering material specification."""
    name: str
    base_color: Tuple[float, float, float]
    roughness: float
    metallic: float
    clearcoat: float = 0.0
    ior: float = 1.5
    emissive: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    normal_scale: float = 1.0

class PBRMaterialSystem:
    """Enterprise PBR Material Management and Three.js Shader Compiler."""

    def __init__(self):
        self._profiles: Dict[str, PBRMaterialProfile] = {}
        self._register_default_profiles()

    def _register_default_profiles(self):
        self._profiles["default"] = PBRMaterialProfile(
            name="default",
            base_color=(0.8, 0.8, 0.8),
            roughness=0.5,
            metallic=0.1
        )

    def pack_orm_texture(
        self,
        ao_map: Optional[np.ndarray] = None,
        roughness_map: Optional[np.ndarray] = None,
        metallic_map: Optional[np.ndarray] = None,
        resolution: int = 1024
    ) -> np.ndarray:
        """
        Packs Ambient Occlusion (R), Roughness (G), and Metallic (B) into a single 3-channel map.
        Optimizes WebGL GPU texture sampler bandwidth.
        """
        orm = np.zeros((resolution, resolution, 3), dtype=np.uint8)
        if ao_map is not None:
            orm[:, :, 0] = ao_map
        else:
            orm[:, :, 0] = 255  # Default full ambient lighting

        if roughness_map is not None:
            orm[:, :, 1] = roughness_map
        else:
            orm[:, :, 1] = 128  # Default 0.5 roughness

        if metallic_map is not None:
            orm[:, :, 2] = metallic_map
        else:
            orm[:, :, 2] = 0    # Default dielectric (non-metallic)

        return orm
