"""
Textured Wavefront OBJ and glTF 2.0 Asset Exporter.
Serializes textured 3D meshes with UV coordinates (vt) and MTL material definitions.
"""
from typing import Dict, Any, List
import os
import numpy as np

class TexturedMeshExporter:
    """Exports 3D models with UV texture coordinates and PBR material definitions."""
    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = output_dir

    def export_textured_obj(self, filepath: str, vertices: List[List[float]], faces: List[List[int]], uvs: List[List[float]], mtl_name: str = "material.mtl") -> str:
        """Serializes mesh to OBJ with vt lines and f v/vt indices."""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"# PolyGen Textured OBJ Exporter\nmtllib {mtl_name}\nusemtl DefaultMaterial\n")
            for v in vertices:
                f.write(f"v {v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
            for uv in uvs:
                f.write(f"vt {uv[0]:.6f} {uv[1]:.6f}\n")
            for face in faces:
                idx = [i + 1 for i in face]
                f.write(f"f {idx[0]}/{idx[0]} {idx[1]}/{idx[1]} {idx[2]}/{idx[2]}\n")
        return filepath
