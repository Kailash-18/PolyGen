"""
Stage 3: Garland-Heckbert Quadric Error Metrics (QEM) Decimation Engine.
Simplifies dense AI-generated 3D meshes (500k -> 10k polygons) with boundary preservation.
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import trimesh

class QEMDecimator:
    """Production-grade Quadric Error Metric (QEM) mesh simplifier."""

    def __init__(self, target_faces: int = 10000, boundary_weight: float = 1000.0):
        self.target_faces = target_faces
        self.boundary_weight = boundary_weight

    def compute_face_quadric(self, v0: np.ndarray, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
        """
        Computes fundamental error quadric K_p = p * p^T for triangle plane.
        Plane equation: ax + by + cz + d = 0, with normalized normal vector.
        """
        edge1 = v1 - v0
        edge2 = v2 - v0
        normal = np.cross(edge1, edge2)
        norm_len = np.linalg.norm(normal)
        if norm_len < 1e-12:
            return np.zeros((4, 4), dtype=np.float64)

        n = normal / norm_len
        d = -float(np.dot(n, v0))
        plane = np.array([n[0], n[1], n[2], d], dtype=np.float64)
        return np.outer(plane, plane)

    def compute_vertex_quadrics(self, vertices: np.ndarray, faces: np.ndarray) -> List[np.ndarray]:
        """Accumulates incident triangle face quadrics for every vertex in the mesh."""
        num_verts = len(vertices)
        quadrics = [np.zeros((4, 4), dtype=np.float64) for _ in range(num_verts)]
        for f in faces:
            v0, v1, v2 = vertices[f[0]], vertices[f[1]], vertices[f[2]]
            Kp = self.compute_face_quadric(v0, v1, v2)
            quadrics[f[0]] += Kp
            quadrics[f[1]] += Kp
            quadrics[f[2]] += Kp
        return quadrics

    def evaluate_edge_collapse(
        self,
        v1_pos: np.ndarray,
        v2_pos: np.ndarray,
        Q1: np.ndarray,
        Q2: np.ndarray
    ) -> Tuple[np.ndarray, float]:
        """
        Calculates optimal target vertex position v_bar and associated quadric cost Delta(v_bar).
        Uses closed-form linear system inversion with midpoint fallback.
        """
        Q = Q1 + Q2
        A = np.copy(Q)
        A[3, :3] = 0.0
        A[3, 3] = 1.0

        target_b = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float64)
        try:
            cond = np.linalg.cond(A)
            if cond < 1e5:
                v_bar_hom = np.linalg.solve(A, target_b)
                v_bar = v_bar_hom[:3]
            else:
                raise np.linalg.LinAlgError("Ill-conditioned quadric matrix")
        except (np.linalg.LinAlgError, ValueError):
            # Fallback to midpoint or endpoints minimizing cost
            mid = (v1_pos + v2_pos) * 0.5
            candidates = [v1_pos, v2_pos, mid]
            best_cand = mid
            min_cand_cost = float("inf")
            for c in candidates:
                c_hom = np.array([c[0], c[1], c[2], 1.0], dtype=np.float64)
                cost = float(c_hom.T @ Q @ c_hom)
                if cost < min_cand_cost:
                    min_cand_cost = cost
                    best_cand = c
            return best_cand, max(0.0, min_cand_cost)

        v_hom = np.array([v_bar[0], v_bar[1], v_bar[2], 1.0], dtype=np.float64)
        cost = float(v_hom.T @ Q @ v_hom)
        return v_bar, max(0.0, cost)
