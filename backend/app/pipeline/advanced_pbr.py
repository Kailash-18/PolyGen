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

    def to_gltf_pbr_dict(self) -> Dict[str, Any]:
        pbr_mr: Dict[str, Any] = {
            "baseColorFactor": self.base_color,
            "metallicFactor": self.metallic,
            "roughnessFactor": self.roughness,
        }
        extensions: Dict[str, Any] = {}
        if self.clearcoat > 0.0:
            extensions["KHR_materials_clearcoat"] = {
                "clearcoatFactor": self.clearcoat,
                "clearcoatRoughnessFactor": self.clearcoat_roughness,
            }
        if self.transmission > 0.0:
            extensions["KHR_materials_transmission"] = {
                "transmissionFactor": self.transmission,
            }
            extensions["KHR_materials_volume"] = {
                "thicknessFactor": self.thickness,
                "attenuationColor": self.attenuation_color,
                "attenuationDistance": self.attenuation_distance,
            }
        if self.ior != 1.5:
            extensions["KHR_materials_ior"] = {"ior": self.ior}
        if any(c > 0.0 for c in self.sheen_color):
            extensions["KHR_materials_sheen"] = {
                "sheenColorFactor": self.sheen_color,
                "sheenRoughnessFactor": self.sheen_roughness,
            }
        mat_dict: Dict[str, Any] = {
            "name": self.name,
            "pbrMetallicRoughness": pbr_mr,
            "emissiveFactor": self.emissive_factor,
        }
        if extensions:
            mat_dict["extensions"] = extensions
        return mat_dict

ADVANCED_PBR_CATALOG: Dict[str, AdvancedPBRMaterial] = {
    "Automotive_Obsidian_Clearcoat": AdvancedPBRMaterial(
        name="Automotive_Obsidian_Clearcoat",
        base_color=[0.05, 0.05, 0.06, 1.0],
        metallic=0.2, roughness=0.15, clearcoat=1.0, clearcoat_roughness=0.02, ior=1.58
    ),
    "Refractive_Flint_Glass": AdvancedPBRMaterial(
        name="Refractive_Flint_Glass",
        base_color=[0.95, 0.98, 1.0, 1.0],
        metallic=0.0, roughness=0.02, transmission=0.96, ior=1.62, thickness=0.05
    ),
    "Velvet_Royal_Purple": AdvancedPBRMaterial(
        name="Velvet_Royal_Purple",
        base_color=[0.25, 0.02, 0.45, 1.0],
        metallic=0.0, roughness=0.85, sheen_color=[0.6, 0.2, 0.8], sheen_roughness=0.35
    )
}
