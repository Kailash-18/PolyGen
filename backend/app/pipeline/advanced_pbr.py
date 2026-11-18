"""Advanced PBR Material Parameters and glTF Extension Generator."""
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class AdvancedPBRMaterial:
    name: str
    base_color: List[float] = field(default_factory=lambda: [0.8, 0.8, 0.8, 1.0])
    metallic: float = 0.0
    roughness: float = 0.5
    clearcoat: float = 0.0
    clearcoat_roughness: float = 0.03
    transmission: float = 0.0
    ior: float = 1.5
    thickness: float = 0.0
    attenuation_color: List[float] = field(default_factory=lambda: [1.0, 1.0, 1.0])
    attenuation_distance: float = 1.0
    sheen_color: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    sheen_roughness: float = 0.2
    emissive_factor: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    emissive_strength: float = 1.0
