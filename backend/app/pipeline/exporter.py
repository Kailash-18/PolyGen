"""
Stage 4: Multi-Format Asset Packaging & Serialisation Engine (GLB / OBJ / USDZ)
"""

import json
from pathlib import Path
import trimesh
from PIL import Image

class AssetExporter:
    def __init__(self, output_root: Path):
        self.output_root = Path(output_root)
        self.output_root.mkdir(parents=True, exist_ok=True)

    def export_asset(self, mesh: trimesh.Trimesh, model_id: str, pbr_maps: dict[str, Image.Image] = None) -> dict:
        model_dir = self.output_root / model_id
        model_dir.mkdir(parents=True, exist_ok=True)

        glb_path = model_dir / f"{model_id}.glb"
        glb_bytes = trimesh.exchange.gltf.export_glb(mesh)
        with open(glb_path, "wb") as f:
            f.write(glb_bytes)

        obj_path = model_dir / f"{model_id}.obj"
        obj_content = trimesh.exchange.obj.export_obj(mesh)
        with open(obj_path, "w", encoding="utf-8") as f:
            f.write(obj_content)

        if pbr_maps:
            for map_name, img in pbr_maps.items():
                img.save(model_dir / f"{map_name}.png", "PNG")

        return {
            "model_id": model_id,
            "directory": str(model_dir),
            "glb_path": str(glb_path),
            "obj_path": str(obj_path),
            "glb_url": f"/outputs/{model_id}/{model_id}.glb",
            "obj_url": f"/outputs/{model_id}/{model_id}.obj",
            "glb_size_bytes": len(glb_bytes),
            "obj_size_bytes": len(obj_content)
        }

    def save_metadata(self, model_id: str, metadata: dict) -> Path:
        meta_path = self.output_root / model_id / "metadata.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)
        return meta_path
