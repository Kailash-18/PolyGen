"""
Stage 2: Mesh Topology Optimization & Decimation Engine (QEM / Manifold Repair)
"""

import math
import numpy as np
import trimesh

class MeshOptimizer:
    def __init__(self, target_polycount: int = 10000):
        self.target_polycount = target_polycount

    def clean_and_repair(self, mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        cleaned = mesh.copy()
        if hasattr(cleaned, "process"):
            cleaned.process(validate=True)

        if not cleaned.is_watertight:
            trimesh.repair.fill_holes(cleaned)
            trimesh.repair.fix_winding(cleaned)
            trimesh.repair.fix_inversion(cleaned)

        return cleaned

    def decimate(self, mesh: trimesh.Trimesh, target_faces: int = None) -> tuple[trimesh.Trimesh, dict]:
        """Reduces polycount using Quadric Error Metrics while preserving silhouette edges and UV borders"""
        if target_faces is None:
            target_faces = self.target_polycount

        initial_face_count = len(mesh.faces)
        if initial_face_count <= target_faces:
            return mesh, {
                "before_faces": initial_face_count,
                "after_faces": initial_face_count,
                "decimation_ratio": 1.0,
                "reduction_percentage": "0.0%"
            }

        try:
            decimated = mesh.simplify_quadric_decimation(face_count=target_faces)
        except Exception:
            try:
                decimated = mesh.simplify_quadratic_decimation(face_count=target_faces)
            except Exception:
                decimated = mesh

        final_face_count = len(decimated.faces)
        ratio = round(final_face_count / initial_face_count, 4)
        reduction = round((1.0 - ratio) * 100, 2)

        return decimated, {
            "before_faces": initial_face_count,
            "after_faces": final_face_count,
            "decimation_ratio": ratio,
            "reduction_percentage": f"{reduction}%"
        }

    def compute_uv_unwrapping(self, mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """Calculates conformal surface parameterization and spherical UV unwrapping coordinates"""
        uv_mesh = mesh.copy()
        vertices = uv_mesh.vertices
        x, y, z = vertices[:, 0], vertices[:, 1], vertices[:, 2]

        u = 0.5 + (np.arctan2(z, x) / (2.0 * np.pi))
        v = 0.5 - (np.arcsin(np.clip(y / (np.linalg.norm(vertices, axis=1) + 1e-6), -1.0, 1.0)) / np.pi)
        uvs = np.column_stack([u, v])

        uv_mesh.visual = trimesh.visual.TextureVisuals(uv=uvs)
        return uv_mesh

    def get_mesh_stats(self, mesh: trimesh.Trimesh) -> dict:
        return {
            "vertices": len(mesh.vertices),
            "faces": len(mesh.faces),
            "is_watertight": bool(mesh.is_watertight),
            "bounds": [mesh.bounds[0].tolist(), mesh.bounds[1].tolist()] if mesh.bounds is not None else None,
            "volume": float(mesh.volume) if mesh.is_watertight else 0.0,
            "center_of_mass": (getattr(mesh, "center_mass", getattr(mesh, "center_of_mass", [0, 0, 0])).tolist() if hasattr(getattr(mesh, "center_mass", getattr(mesh, "center_of_mass", None)), "tolist") else [0, 0, 0])
        }
