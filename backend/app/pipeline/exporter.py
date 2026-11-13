"""
Stage 4: Packaging and 3D Asset Export Engine
Converts meshes and materials into standard .glb, .gltf, and .obj formats
ready for Unreal Engine, Unity, and Three.js.
"""

from pathlib import Path
import trimesh

class AssetExporter:
    def __init__(self, output_root: Path):
        self.output_root = output_root

    def export_asset(self, mesh: trimesh.Trimesh, model_id: str) -> dict:
        """
        Export 3D mesh into standard GLB and OBJ formats.
        """
        model_dir = self.output_root / model_id
        model_dir.mkdir(parents=True, exist_ok=True)

        glb_path = model_dir / "model.glb"
        obj_path = model_dir / "model.obj"

        # 1. Export binary GLB (standard for WebGL, Unreal, Unity)
        glb_data = trimesh.exchange.gltf.export_glb(mesh)
        with open(glb_path, "wb") as f:
            f.write(glb_data)

        # 2. Export standard Wavefront OBJ
        obj_data = trimesh.exchange.obj.export_obj(mesh)
        with open(obj_path, "w", encoding="utf-8") as f:
            f.write(obj_data)

        return {
            "model_id": model_id,
            "glb_path": str(glb_path),
            "obj_path": str(obj_path),
            "glb_url": f"/outputs/{model_id}/model.glb",
            "obj_url": f"/outputs/{model_id}/model.obj",
            "glb_size_bytes": glb_path.stat().st_size,
            "obj_size_bytes": obj_path.stat().st_size,
        }
