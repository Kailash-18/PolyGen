"""USD and USDZ Apple AR QuickLook Exporter."""
import os
import zipfile
from typing import List, Optional, Dict, Any

class USDZExporter:
    @staticmethod
    def generate_usda(model_id: str, vertices: List[List[float]], faces: List[List[int]], normals: Optional[List[List[float]]] = None, material_name: str = "PBR_Material") -> str:
        points_str = ", ".join(f"({v[0]:.4f}, {v[1]:.4f}, {v[2]:.4f})" for v in vertices)
        counts_str = ", ".join("3" for _ in faces)
        indices_flat = []
        for f in faces: indices_flat.extend(f)
        indices_str = ", ".join(str(idx) for idx in indices_flat)
        normals_sec = ""
        if normals and len(normals) == len(vertices):
            norm_str = ", ".join(f"({n[0]:.4f}, {n[1]:.4f}, {n[2]:.4f})" for n in normals)
            normals_sec = f'\n        normal3f[] normals = [{norm_str}] (interpolation = "vertex")'

        return f"""#usda 1.0
(
    defaultPrim = "{model_id}"
    metersPerUnit = 1.0
    upAxis = "Y"
)

def Xform "{model_id}" (kind = "component")
{{
    def Mesh "GeomMesh"
    {{
        int[] faceVertexCounts = [{counts_str}]
        int[] faceVertexIndices = [{indices_str}]
        point3f[] points = [{points_str}]{normals_sec}
        rel material:binding = </{model_id}/Materials/{material_name}>
    }}

    def Scope "Materials"
    {{
        def Material "{material_name}"
        {{
            token outputs:surface.connect = </{model_id}/Materials/{material_name}/PBRShader.outputs:surface>
            def Shader "PBRShader"
            {{
                uniform token info:id = "UsdPreviewSurface"
                color3f inputs:diffuseColor = (0.7, 0.7, 0.7)
                float inputs:metallic = 0.1
                float inputs:roughness = 0.4
                token outputs:surface
            }}
        }}
    }}
}}
"""

    @classmethod
    def create_usdz_package(cls, output_path: str, model_id: str, vertices: List[List[float]], faces: List[List[int]], normals: Optional[List[List[float]]] = None) -> Dict[str, Any]:
        usda_text = cls.generate_usda(model_id, vertices, faces, normals)
        usda_bytes = usda_text.encode("utf-8")
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_STORED) as zf:
            zf.writestr(f"{model_id}.usda", usda_bytes)
        file_size = os.path.getsize(output_path)
        return {
            "model_id": model_id,
            "usdz_path": output_path,
            "file_size_bytes": file_size,
            "vertex_count": len(vertices),
            "face_count": len(faces),
            "format": "USDZ",
            "ar_compatibility": ["iOS", "iPadOS", "visionOS", "macOS QuickLook"]
        }
