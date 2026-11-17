"""
Stage 4: Game Engine Asset Exporters for Unreal Engine 5 & Unity
Packages optimized meshes, Multi-LODs, physics collision hulls, and PBR textures
into industry-standard directory layouts, manifests, and ZIP archives.
"""

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any, List, Optional
import io
import json
import zipfile
import numpy as np
import trimesh
from PIL import Image

from app.pipeline.lod import LODGenerator
from app.pipeline.collision_hull import CollisionHullGenerator
from app.pipeline.gltf_packager import GLTFPackager


class UnrealEngineExporter:
    """
    Exports asset packages compliant with Epic Games Unreal Engine 5 standards:
      - Static Mesh naming: SM_<AssetName>
      - Collision Hull naming: UCX_<AssetName>_##
      - Texture naming: T_<AssetName>_D, T_<AssetName>_N, T_<AssetName>_R, T_<AssetName>_M
      - LOD Screen Size auto-transition thresholds
      - Nanite geometry compatibility audit
    """

    @classmethod
    def create_package(
        cls,
        mesh: trimesh.Trimesh,
        asset_name: str,
        output_dir: Path,
        pbr_maps: Optional[Dict[str, Image.Image]] = None,
        generate_lods: bool = True,
        generate_collision: bool = True
    ) -> Dict[str, Any]:
        output_dir = Path(output_dir)
        ue_dir = output_dir / f"Unreal_{asset_name}"
        ue_dir.mkdir(parents=True, exist_ok=True)

        clean_name = asset_name.replace(" ", "_")
        files_created: List[str] = []

        # 1. Main Static Mesh (SM_*)
        mesh_glb = GLTFPackager.assemble_glb(mesh, f"SM_{clean_name}")
        main_mesh_path = ue_dir / f"SM_{clean_name}.glb"
        with open(main_mesh_path, "wb") as f:
            f.write(mesh_glb)
        files_created.append(str(main_mesh_path))

        # 2. Multi-LODs
        lod_data = {}
        if generate_lods:
            lod_gen = LODGenerator()
            res_lods = lod_gen.generate_lods(mesh)
            lod_data = res_lods["specifications"]
            for lod_name, lod_mesh in res_lods["lods"].items():
                if lod_name != "LOD0":
                    lod_glb = GLTFPackager.assemble_glb(lod_mesh, f"SM_{clean_name}_{lod_name}")
                    p = ue_dir / f"SM_{clean_name}_{lod_name}.glb"
                    with open(p, "wb") as f:
                        f.write(lod_glb)
                    files_created.append(str(p))

        # 3. Collision Hulls (UCX_*)
        collision_manifest = {}
        if generate_collision:
            coll_gen = CollisionHullGenerator()
            coll_res = coll_gen.generate_all_colliders(mesh)
            collision_manifest = coll_res["manifest"]
            ucx_path = coll_gen.export_unreal_collision_file(ue_dir, clean_name, coll_res["meshes"])
            files_created.append(ucx_path)

        # 4. Textures (T_*_D, T_*_N, T_*_R, T_*_M)
        if pbr_maps:
            if "albedo" in pbr_maps and pbr_maps["albedo"]:
                p = ue_dir / f"T_{clean_name}_D.png"
                pbr_maps["albedo"].save(p)
                files_created.append(str(p))
            if "normal" in pbr_maps and pbr_maps["normal"]:
                p = ue_dir / f"T_{clean_name}_N.png"
                pbr_maps["normal"].save(p)
                files_created.append(str(p))
            if "roughness" in pbr_maps and pbr_maps["roughness"]:
                p = ue_dir / f"T_{clean_name}_R.png"
                pbr_maps["roughness"].save(p)
                files_created.append(str(p))
            if "metalness" in pbr_maps and pbr_maps["metalness"]:
                p = ue_dir / f"T_{clean_name}_M.png"
                pbr_maps["metalness"].save(p)
                files_created.append(str(p))

        # 5. Unreal Engine Asset Manifest JSON
        nanite_recommended = len(mesh.faces) >= 20000
        manifest = {
            "unreal_engine_version": "5.4+",
            "asset_class": "UStaticMesh",
            "asset_name": f"SM_{clean_name}",
            "vertex_count": len(mesh.vertices),
            "triangle_count": len(mesh.faces),
            "bounds": {
                "box_extent": [float(x) for x in (mesh.bounds[1] - mesh.bounds[0]) / 2.0],
                "sphere_radius": float(np.linalg.norm(mesh.bounds[1] - mesh.bounds[0]) / 2.0)
            },
            "nanite_settings": {
                "enabled_recommended": nanite_recommended,
                "keep_percent_triangles": 1.0,
                "trim_relative_error": 0.04
            },
            "lod_settings": lod_data,
            "collision_settings": {
                "custom_collision": generate_collision,
                "collision_complexity": "UseSimpleAsComplex",
                "primitives": collision_manifest
            },
            "materials": [
                {
                    "slot_index": 0,
                    "material_name": f"M_{clean_name}_PBR",
                    "textures": {
                        "base_color": f"T_{clean_name}_D",
                        "normal": f"T_{clean_name}_N",
                        "roughness": f"T_{clean_name}_R",
                        "metallic": f"T_{clean_name}_M"
                    }
                }
            ]
        }

        manifest_path = ue_dir / "UnrealAssetManifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        files_created.append(str(manifest_path))

        # 6. Package into ZIP
        zip_path = output_dir / f"{clean_name}_UnrealEngine5.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_str in files_created:
                f_path = Path(file_str)
                zf.write(f_path, arcname=f"{ue_dir.name}/{f_path.name}")

        return {
            "package_path": str(zip_path),
            "directory": str(ue_dir),
            "file_count": len(files_created),
            "manifest": manifest
        }
