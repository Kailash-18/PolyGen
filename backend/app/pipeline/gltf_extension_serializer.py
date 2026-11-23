"""
Stage 3: Khronos glTF 2.0 Material Extension Serializer.
Serializes KHR_materials_clearcoat, KHR_materials_ior, KHR_materials_transmission, and volume.
"""

from typing import Dict, Any, List, Optional

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
