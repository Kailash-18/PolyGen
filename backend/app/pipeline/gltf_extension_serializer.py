"""
Stage 3: Khronos glTF 2.0 Material Extension Serializer.
Serializes KHR_materials_clearcoat, KHR_materials_ior, KHR_materials_transmission, and volume.
"""

from typing import Dict, Any, List, Tuple, Optional

class GLTFExtensionSerializer:
    """Compiles Khronos extension dictionary for glTF 2.0 materials."""

    def __init__(self):
        pass

    def serialize_clearcoat_extension(
        self,
        clearcoat_factor: float = 1.0,
        clearcoat_roughness: float = 0.05
    ) -> Dict[str, Any]:
        """Encodes KHR_materials_clearcoat extension structure."""
        return {
            "clearcoatFactor": float(max(0.0, min(1.0, clearcoat_factor))),
            "clearcoatRoughnessFactor": float(max(0.0, min(1.0, clearcoat_roughness)))
        }

    def serialize_ior_extension(self, ior: float = 1.5) -> Dict[str, Any]:
        """Encodes KHR_materials_ior extension structure."""
        return {
            "ior": float(max(1.0, min(3.0, ior)))
        }

    def serialize_transmission_extension(self, transmission_factor: float = 1.0) -> Dict[str, Any]:
        """Encodes KHR_materials_transmission extension structure."""
        return {
            "transmissionFactor": float(max(0.0, min(1.0, transmission_factor)))
        }

    def serialize_volume_extension(
        self,
        thickness_factor: float = 0.5,
        attenuation_distance: float = 1.0,
        attenuation_color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    ) -> Dict[str, Any]:
        """Encodes KHR_materials_volume extension structure."""
        return {
            "thicknessFactor": float(max(0.0, thickness_factor)),
            "attenuationDistance": float(max(1e-4, attenuation_distance)),
            "attenuationColor": [float(c) for c in attenuation_color]
        }

    def serialize_emissive_strength_extension(self, emissive_strength: float = 2.5) -> Dict[str, Any]:
        """Encodes KHR_materials_emissive_strength extension for HDR glowing surfaces."""
        return {
            "emissiveStrength": float(max(0.0, emissive_strength))
        }

    def compile_all_extensions(self, material_params: Dict[str, Any]) -> Dict[str, Any]:
        """Aggregates all enabled KHR extensions into single extensions dictionary."""
        exts = {}
        if material_params.get("clearcoat", 0.0) > 0.0:
            exts["KHR_materials_clearcoat"] = self.serialize_clearcoat_extension(
                clearcoat_factor=material_params["clearcoat"],
                clearcoat_roughness=material_params.get("clearcoat_roughness", 0.05)
            )

        if "ior" in material_params:
            exts["KHR_materials_ior"] = self.serialize_ior_extension(material_params["ior"])

        if material_params.get("transmission", 0.0) > 0.0:
            exts["KHR_materials_transmission"] = self.serialize_transmission_extension(
                material_params["transmission"]
            )
            exts["KHR_materials_volume"] = self.serialize_volume_extension(
                thickness_factor=material_params.get("thickness", 0.5),
                attenuation_color=material_params.get("attenuation_color", (1.0, 1.0, 1.0))
            )

        if material_params.get("emissive_strength", 0.0) > 1.0:
            exts["KHR_materials_emissive_strength"] = self.serialize_emissive_strength_extension(
                material_params["emissive_strength"]
            )

        return exts
