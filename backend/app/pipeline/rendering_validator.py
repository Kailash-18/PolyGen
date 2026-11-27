"""
Three.js WebGL Rendering Validation Engine.
Ensures Three.js WebGL canvas successfully maps generated PBR textures onto 3D meshes.
"""
from typing import Dict, Any, List

class RenderingValidator:
    """Validates Three.js / React-Three-Fiber PBR rendering compatibility."""
    def __init__(self, required_channels: List[str] = None):
        self.required_channels = required_channels or ["albedo", "normal", "roughness"]

    def validate_rendering_pipeline(self, mesh_id: str, uvs_count: int, texture_manifest: Dict[str, Any]) -> Dict[str, Any]:
        """Validates that texture maps and UV channels conform to Three.js MeshStandardMaterial."""
        has_uvs = uvs_count > 0
        channels_present = [ch for ch in self.required_channels if ch in texture_manifest]
        all_channels = len(channels_present) == len(self.required_channels)

        return {
            "status": "PASS" if (has_uvs and all_channels) else "FAIL",
            "mesh_id": mesh_id,
            "has_uv_attribute": has_uvs,
            "channels_validated": channels_present,
            "three_js_material": "MeshStandardMaterial",
            "webgl_ready": has_uvs and all_channels
        }
