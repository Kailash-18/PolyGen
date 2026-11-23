"""
Stage 3: Unified PBR Material Compilation Pipeline.
Integrates PBRShaderEngine, MultiUVGenerator, RadianceProbe, and GLTFExtensionSerializer.
"""

from typing import Dict, Any, List, Optional
import numpy as np

from app.pipeline.pbr_shader_engine import PBRShaderEngine
from app.pipeline.multi_uv_generator import MultiUVGenerator
from app.pipeline.radiance_probe import RadianceProbe
from app.pipeline.gltf_extension_serializer import GLTFExtensionSerializer
from app.pipeline.threejs_material_bridge import ThreeJSMaterialBridge

class UnifiedPBRPipeline:
    """Orchestrates comprehensive PBR compilation for generated 3D assets."""

    def __init__(self):
        self.shader_engine = PBRShaderEngine()
        self.uv_gen = MultiUVGenerator()
        self.radiance_probe = RadianceProbe()
        self.extension_serializer = GLTFExtensionSerializer()
        self.bridge = ThreeJSMaterialBridge()

    def compile_asset_materials(
        self,
        asset_id: str,
        material_params: Dict[str, Any],
        vertices: Optional[np.ndarray] = None,
        faces: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """Executes full PBR compilation pass: optical models, glTF extensions, and Three.js bridge."""
        f0 = self.shader_engine.compute_f0_from_ior(material_params.get("ior", 1.5))
        extensions = self.extension_serializer.compile_all_extensions(material_params)

        threejs_mat = {
            "type": "MeshPhysicalMaterial",
            "color": material_params.get("color", "#aaaaaa"),
            "roughness": material_params.get("roughness", 0.5),
            "metalness": material_params.get("metalness", 0.0),
            "clearcoat": material_params.get("clearcoat", 0.0),
            "ior": material_params.get("ior", 1.5),
            "transmission": material_params.get("transmission", 0.0),
            "extensions": extensions
        }

        self.bridge.register_material(asset_id, threejs_mat)

        return {
            "asset_id": asset_id,
            "fresnel_f0": round(f0, 4),
            "gltf_extensions": extensions,
            "threejs_material": threejs_mat
        }
