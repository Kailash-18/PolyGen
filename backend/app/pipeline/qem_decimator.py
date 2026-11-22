"""
Stage 3: Garland-Heckbert Quadric Error Metrics (QEM) Decimation Engine.
Simplifies dense AI-generated 3D meshes (500k -> 10k polygons) with boundary preservation.
"""

from typing import List, Tuple, Dict, Any, Optional, Set
import heapq
from collections import defaultdict
import numpy as np
import trimesh

class QEMDecimator:
    """Production-grade Quadric Error Metric (QEM) mesh simplifier."""

    def __init__(self, target_faces: int = 10000, boundary_weight: float = 1000.0, min_normal_cos: float = 0.2):
        self.target_faces = target_faces
        self.boundary_weight = boundary_weight
        self.min_normal_cos = min_normal_cos

    def compute_face_quadric(self, v0: np.ndarray, v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
        """Computes fundamental error quadric K_p = p * p^T for triangle plane."""
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

    def identify_boundary_edges(self, faces: np.ndarray) -> Set[Tuple[int, int]]:
        """Identifies open topological boundaries."""
        edge_counts = defaultdict(int)
        for f in faces:
            for i in range(3):
                u, v = int(f[i]), int(f[(i + 1) % 3])
                edge = (min(u, v), max(u, v))
                edge_counts[edge] += 1
        return {edge for edge, count in edge_counts.items() if count == 1}

    def compute_vertex_quadrics(
        self,
        vertices: np.ndarray,
        faces: np.ndarray,
        preserve_boundaries: bool = True
    ) -> List[np.ndarray]:
        """Accumulates face quadrics plus boundary constraint penalties."""
        num_verts = len(vertices)
        quadrics = [np.zeros((4, 4), dtype=np.float64) for _ in range(num_verts)]
        for f in faces:
            v0, v1, v2 = vertices[f[0]], vertices[f[1]], vertices[f[2]]
            Kp = self.compute_face_quadric(v0, v1, v2)
            quadrics[f[0]] += Kp
            quadrics[f[1]] += Kp
            quadrics[f[2]] += Kp

        if preserve_boundaries:
            boundary_edges = self.identify_boundary_edges(faces)
            for u, v in boundary_edges:
                edge_vec = vertices[v] - vertices[u]
                edge_len = np.linalg.norm(edge_vec)
                if edge_len > 1e-12:
                    e_norm = edge_vec / edge_len
                    ortho = np.array([-e_norm[1], e_norm[0], 0.0])
                    if np.linalg.norm(ortho) < 1e-6:
                        ortho = np.array([0.0, -e_norm[2], e_norm[1]])
                    ortho = ortho / (np.linalg.norm(ortho) + 1e-12)
                    d = -float(np.dot(ortho, vertices[u]))
                    p = np.array([ortho[0], ortho[1], ortho[2], d], dtype=np.float64)
                    K_b = np.outer(p, p) * self.boundary_weight
                    quadrics[u] += K_b
                    quadrics[v] += K_b
        return quadrics

    def check_normal_inversion(
        self,
        v_idx: int,
        target_pos: np.ndarray,
        incident_faces: List[Tuple[int, int, int]],
        vertices: np.ndarray
    ) -> bool:
        """
        Validates that collapsing a vertex does not invert (flip) incident triangle normals.
        Returns True if safe (no flip), False if normal would invert.
        """
        for f in incident_faces:
            pts = [vertices[f[0]], vertices[f[1]], vertices[f[2]]]
            orig_norm = np.cross(pts[1] - pts[0], pts[2] - pts[0])
            orig_len = np.linalg.norm(orig_norm)
            if orig_len < 1e-12:
                continue
            orig_n = orig_norm / orig_len

            # New triangle points with v_idx substituted
            new_pts = [target_pos if idx == v_idx else vertices[idx] for idx in f]
            new_norm = np.cross(new_pts[1] - new_pts[0], new_pts[2] - new_pts[0])
            new_len = np.linalg.norm(new_norm)
            if new_len < 1e-12:
                return False
            new_n = new_norm / new_len

            if float(np.dot(orig_n, new_n)) < self.min_normal_cos:
                return False  # Normal inverted / flipped
        return True

    def evaluate_edge_collapse(
        self,
        v1_pos: np.ndarray,
        v2_pos: np.ndarray,
        Q1: np.ndarray,
        Q2: np.ndarray
    ) -> Tuple[np.ndarray, float]:
        """Calculates optimal target vertex position and cost."""
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
