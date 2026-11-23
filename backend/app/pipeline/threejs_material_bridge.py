"""
Stage 3: Real-Time Three.js WebGL Material Bridge.
Maintains live parameter state and serializes updates for the interactive 3D canvas viewer.
"""

from typing import Dict, Any, List, Optional
import json

class ThreeJSMaterialBridge:
    """Manages dynamic WebGL shader material parameters and live canvas telemetry."""

    def __init__(self):
        self._active_materials: Dict[str, Dict[str, Any]] = {}

    def register_material(self, material_id: str, material_data: Dict[str, Any]) -> Dict[str, Any]:
        """Registers material in active runtime state."""
        self._active_materials[material_id] = dict(material_data)
        return self._active_materials[material_id]

    def get_material(self, material_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves active material configuration."""
        return self._active_materials.get(material_id)

    def serialize_threejs_payload(self, material_id: str) -> Dict[str, Any]:
        """Constructs JSON payload for direct ingestion by Three.js Material Loader."""
        mat = self.get_material(material_id)
        if not mat:
            mat = {"type": "MeshStandardMaterial", "color": "#cccccc", "roughness": 0.5, "metalness": 0.0}

        return {
            "version": "1.0",
            "material_id": material_id,
            "threejs_material": mat
        }
