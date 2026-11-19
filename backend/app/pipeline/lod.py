"""
Stage 4: Multi-LOD Generation Engine (LOD0, LOD1, LOD2, LOD3)
Generates discrete Level of Detail hierarchies for Unreal Engine 5 Nanite/LOD groups and Unity URP/HDRP.
"""

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any, List, Optional
import math
import numpy as np
import trimesh

from app.pipeline.optimizer import MeshOptimizer


@dataclass
class LODSpecification:
    level: str
    target_ratio: float
    screen_size_threshold: float
    face_count: int
    vertex_count: int
    hausdorff_error: float
    reduction_percentage: str
    is_master: bool = False


class LODGenerator:
    """
    Multi-LOD generator creating cascaded level-of-detail meshes from master 3D assets.
    Default screen size thresholds correspond to industry-standard game engine settings:
      LOD0: 1.00 (Full fidelity, hero closeup, screen size >= 0.70)
      LOD1: 0.50 (50% polycount, mid-range view, screen size >= 0.40)
      LOD2: 0.25 (25% polycount, distance view, screen size >= 0.15)
      LOD3: 0.10 (10% polycount, far background proxy, screen size >= 0.05)
    """

    DEFAULT_LOD_CONFIG = {
        "LOD0": {"ratio": 1.00, "screen_threshold": 0.70},
        "LOD1": {"ratio": 0.50, "screen_threshold": 0.40},
        "LOD2": {"ratio": 0.25, "screen_threshold": 0.15},
        "LOD3": {"ratio": 0.10, "screen_threshold": 0.05},
    }

    def __init__(self, optimizer: Optional[MeshOptimizer] = None):
        self.optimizer = optimizer or MeshOptimizer()

    def compute_hausdorff_error(self, master_mesh: trimesh.Trimesh, decimated_mesh: trimesh.Trimesh) -> float:
        """
        Approximates one-sided Hausdorff geometric distance between master and decimated mesh vertices.
        Returns normalized error relative to the master mesh bounding box diagonal.
        """
        if master_mesh is None or decimated_mesh is None:
            return 0.0
        if len(master_mesh.vertices) == 0 or len(decimated_mesh.vertices) == 0:
            return 0.0

        # Sample points on master vertices against decimated surface
        try:
            sample_pts = master_mesh.vertices[:min(500, len(master_mesh.vertices))]
            _, distances, _ = trimesh.proximity.closest_point(decimated_mesh, sample_pts)
            max_dist = float(np.max(distances))
        except Exception:
            # Fallback simple bounding box difference
            max_dist = float(np.linalg.norm(master_mesh.bounds[1] - decimated_mesh.bounds[1]))

        diagonal = float(np.linalg.norm(master_mesh.bounds[1] - master_mesh.bounds[0]))
        if diagonal > 1e-6:
            return round(max_dist / diagonal, 5)
        return round(max_dist, 5)

    def generate_lods(
        self,
        master_mesh: trimesh.Trimesh,
        custom_ratios: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Generates full LOD hierarchy for a given trimesh object.
        Returns dictionary containing mesh instances, metadata, and engine export thresholds.
        """
        clean_master = self.optimizer.clean_and_repair(master_mesh)
        initial_faces = len(clean_master.faces)
        initial_verts = len(clean_master.vertices)

        config = {}
        for lod_name, defaults in self.DEFAULT_LOD_CONFIG.items():
            ratio = defaults["ratio"]
            if custom_ratios and lod_name in custom_ratios:
                ratio = custom_ratios[lod_name]
            config[lod_name] = {
                "ratio": ratio,
                "screen_threshold": defaults["screen_threshold"]
            }

        lods: Dict[str, trimesh.Trimesh] = {}
        specs: Dict[str, LODSpecification] = {}

        for lod_name, cfg in config.items():
            target_ratio = cfg["ratio"]
            screen_threshold = cfg["screen_threshold"]

            if lod_name == "LOD0" or target_ratio >= 1.0:
                lod_mesh = clean_master.copy()
                error = 0.0
                specs[lod_name] = LODSpecification(
                    level=lod_name,
                    target_ratio=1.0,
                    screen_size_threshold=screen_threshold,
                    face_count=initial_faces,
                    vertex_count=initial_verts,
                    hausdorff_error=0.0,
                    reduction_percentage="0.0%",
                    is_master=True
                )
            else:
                target_faces = max(12, int(initial_faces * target_ratio))
                decimated, meta = self.optimizer.decimate(clean_master, target_faces=target_faces)
                error = self.compute_hausdorff_error(clean_master, decimated)
                reduction_pct = meta.get("reduction_percentage", "0.0%")
                specs[lod_name] = LODSpecification(
                    level=lod_name,
                    target_ratio=target_ratio,
                    screen_size_threshold=screen_threshold,
                    face_count=len(decimated.faces),
                    vertex_count=len(decimated.vertices),
                    hausdorff_error=error,
                    reduction_percentage=reduction_pct,
                    is_master=False
                )
                lod_mesh = decimated

            lods[lod_name] = lod_mesh

        return {
            "lods": lods,
            "specifications": {k: asdict(v) for k, v in specs.items()},
            "summary": {
                "master_faces": initial_faces,
                "lod_count": len(lods),
                "max_reduction": specs["LOD3"].reduction_percentage,
                "max_hausdorff_error": specs["LOD3"].hausdorff_error
            }
        }

    def export_lods(
        self,
        output_dir: Path,
        model_id: str,
        lods: Dict[str, trimesh.Trimesh]
    ) -> Dict[str, str]:
        """
        Saves individual LOD meshes as standard .obj and .glb files in the model output directory.
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        paths: Dict[str, str] = {}

        for lod_name, mesh in lods.items():
            filename = f"{model_id}_{lod_name.lower()}.glb"
            file_path = output_dir / filename
            try:
                mesh.export(str(file_path), file_type="glb")
            except Exception:
                # Fallback to obj
                filename = f"{model_id}_{lod_name.lower()}.obj"
                file_path = output_dir / filename
                mesh.export(str(file_path), file_type="obj")

            paths[lod_name] = str(file_path)

        return paths


class ContinuousLODMorpher:
    """Computes geomorph vertex displacement vectors between discrete LOD hierarchies."""
    def __init__(self, base_vertices: List[List[float]], target_vertices: List[List[float]]):
        self.base_vertices = base_vertices
        self.target_vertices = target_vertices

    def interpolate_positions(self, t: float) -> List[List[float]]:
        """Compute morphed positions at continuous transition parameter t in [0.0, 1.0]."""
        t = float(np.clip(t, 0.0, 1.0))
        morphed = []
        n = min(len(self.base_vertices), len(self.target_vertices))
        for i in range(n):
            v0 = self.base_vertices[i]
            v1 = self.target_vertices[i]
            morphed.append([
                float((1.0 - t) * v0[0] + t * v1[0]),
                float((1.0 - t) * v0[1] + t * v1[1]),
                float((1.0 - t) * v0[2] + t * v1[2])
            ])
        return morphed
