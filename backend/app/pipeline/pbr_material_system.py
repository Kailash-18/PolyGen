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
        self._profiles["medieval_rusted_iron"] = PBRMaterialProfile(
            name="medieval_rusted_iron",
            base_color=(0.35, 0.32, 0.30),
            roughness=0.75,
            metallic=0.85,
            normal_scale=1.5
        )
        self._profiles["polished_sapphire"] = PBRMaterialProfile(
            name="polished_sapphire",
            base_color=(0.08, 0.25, 0.85),
            roughness=0.12,
            metallic=0.05,
            clearcoat=0.9,
            ior=1.77
        )
        self._profiles["aged_oak_wood"] = PBRMaterialProfile(
            name="aged_oak_wood",
            base_color=(0.42, 0.28, 0.16),
            roughness=0.65,
            metallic=0.0,
            normal_scale=0.8
        )
        self._profiles["weathered_bronze"] = PBRMaterialProfile(
            name="weathered_bronze",
            base_color=(0.55, 0.45, 0.30),
            roughness=0.48,
            metallic=0.92,
            normal_scale=1.2
        )
        self._profiles["damaged_leather"] = PBRMaterialProfile(
            name="damaged_leather",
            base_color=(0.32, 0.18, 0.12),
            roughness=0.80,
            metallic=0.02,
            normal_scale=1.1
        )

    def get_profile(self, name: str) -> PBRMaterialProfile:
        """Retrieves PBR material profile or default fallback."""
        return self._profiles.get(name, self._profiles["default"])

    def pack_orm_texture(
        self,
        ao_map: Optional[np.ndarray] = None,
        roughness_map: Optional[np.ndarray] = None,
        metallic_map: Optional[np.ndarray] = None,
        resolution: int = 1024
    ) -> np.ndarray:
        """Packs AO (R), Roughness (G), and Metallic (B) into a 3-channel map."""
        orm = np.zeros((resolution, resolution, 3), dtype=np.uint8)
        orm[:, :, 0] = ao_map if ao_map is not None else 255
        orm[:, :, 1] = roughness_map if roughness_map is not None else 128
        orm[:, :, 2] = metallic_map if metallic_map is not None else 0
        return orm
