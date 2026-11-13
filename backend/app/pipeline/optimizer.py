"""
Stage 2: Mesh Processing & Optimization Engine
Performs Quadric Error Metrics (QEM) Decimation, normal repair,
and UV parameterization using Trimesh.
"""

import trimesh
import numpy as np

class MeshOptimizer:
    def __init__(self, target_polycount: int = 10000):
        self.default_target = target_polycount

    def get_mesh_stats(self, mesh: trimesh.Trimesh) -> dict:
        return {
            "vertices": int(len(mesh.vertices)),
            "faces": int(len(mesh.faces)),
            "is_watertight": bool(mesh.is_watertight),
            "bounds": mesh.bounds.tolist() if mesh.bounds is not None else None,
            "volume": float(mesh.volume) if mesh.is_watertight else 0.0,
            "center_of_mass": mesh.center_mass.tolist() if mesh.bounds is not None else [0, 0, 0],
        }

    def clean_and_repair(self, mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Fix non-manifold geometry, duplicate vertices, and inverted normals"""
        mesh.process(validate=True)
        mesh.fix_normals()
        return mesh

    def decimate(self, mesh: trimesh.Trimesh, target_faces: int = None) -> tuple[trimesh.Trimesh, dict]:
        """
        Reduce high-density geometry down to target polygon count using
        Quadric Error Metrics (QEM).
        """
        target = target_faces or self.default_target
        original_faces = len(mesh.faces)

        if original_faces <= target:
            stats = {
                "before_faces": original_faces,
                "after_faces": original_faces,
                "decimation_ratio": 1.0,
                "reduction_percentage": "0.0%"
            }
            return mesh, stats

        try:
            # Quadric Error Metrics decimation via trimesh
            simplified = mesh.simplify_quadric_decimation(face_count=target)
        except Exception as e:
            print(f"[MeshOptimizer] Fallback decimation due to: {e}")
            simplified = mesh

        stats = {
            "before_faces": original_faces,
            "after_faces": len(simplified.faces),
            "decimation_ratio": round(len(simplified.faces) / original_faces, 4),
            "reduction_percentage": f"{round((1 - (len(simplified.faces) / original_faces)) * 100, 1)}%"
        }
        return simplified, stats

    def compute_uv_unwrapping(self, mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """
        Compute conformal / spherical UV parameterization so textures
        can wrap around the 3D geometry seamlessly.
        """
        if not hasattr(mesh.visual, "uv") or mesh.visual.uv is None or len(mesh.visual.uv) == 0:
            centered = mesh.vertices - mesh.center_mass
            r = np.linalg.norm(centered, axis=1) + 1e-8
            u = 0.5 + (np.arctan2(centered[:, 2], centered[:, 0]) / (2 * np.pi))
            v = 0.5 - (np.arcsin(np.clip(centered[:, 1] / r, -1.0, 1.0)) / np.pi)
            uvs = np.column_stack([u, v])
            mesh.visual = trimesh.visual.TextureVisuals(uv=uvs)
        return mesh
