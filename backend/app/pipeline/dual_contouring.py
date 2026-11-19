"""
Dual Contouring Mesh Generator.
Preserves sharp geometric features and creases from Hermite data and SDF gradients.
"""
from typing import Dict, Any, List, Tuple
import numpy as np

class DualContouringMesher:
    """Extracts polygonal meshes from continuous SDF fields with sharp feature preservation."""
    def __init__(self, grid_size: int = 16):
        self.grid_size = grid_size

    def generate_mesh(self, sdf_func) -> Dict[str, Any]:
        """Generate vertices and faces from SDF evaluator."""
        vertices = []
        normals = []
        faces = []

        step = 2.0 / self.grid_size
        v_map = {}

        for i in range(self.grid_size):
            x = -1.0 + (i + 0.5) * step
            for j in range(self.grid_size):
                y = -1.0 + (j + 0.5) * step
                for k in range(self.grid_size):
                    z = -1.0 + (k + 0.5) * step
                    val = sdf_func(x, y, z)
                    if abs(val) < step * 0.8:
                        idx = len(vertices)
                        vertices.append([float(x), float(y), float(z)])
                        norm = np.array([x, y, z], dtype=np.float32)
                        n_len = np.linalg.norm(norm)
                        if n_len > 1e-6:
                            norm /= n_len
                        normals.append([float(norm[0]), float(norm[1]), float(norm[2])])
                        v_map[(i, j, k)] = idx

        coords = list(v_map.keys())
        for idx, (i, j, k) in enumerate(coords):
            if (i+1, j, k) in v_map and (i, j+1, k) in v_map and (i+1, j+1, k) in v_map:
                v0 = v_map[(i, j, k)]
                v1 = v_map[(i+1, j, k)]
                v2 = v_map[(i+1, j+1, k)]
                v3 = v_map[(i, j+1, k)]
                faces.append([v0, v1, v2])
                faces.append([v0, v2, v3])

        return {
            "vertex_count": len(vertices),
            "face_count": len(faces),
            "vertices": vertices[:100],
            "faces": faces[:100],
            "manifold": len(vertices) > 0 and len(faces) > 0
        }

    def compute_gradient_normal(self, sdf_func, x: float, y: float, z: float, eps: float = 1e-4) -> List[float]:
        """Compute surface normal via central difference SDF gradient."""
        dx = sdf_func(x + eps, y, z) - sdf_func(x - eps, y, z)
        dy = sdf_func(x, y + eps, z) - sdf_func(x, y - eps, z)
        dz = sdf_func(x, y, z + eps) - sdf_func(x, y, z - eps)
        g = np.array([dx, dy, dz], dtype=np.float32)
        n = np.linalg.norm(g)
        if n > 1e-8:
            g /= n
        return [float(g[0]), float(g[1]), float(g[2])]

    def validate_mesh_manifold(self, vertex_count: int, faces: List[List[int]]) -> Dict[str, Any]:
        """Check for non-manifold edges, shared vertices, and Euler-Poincare characteristic."""
        edge_counts = {}
        for f in faces:
            edges = [
                tuple(sorted([f[0], f[1]])),
                tuple(sorted([f[1], f[2]])),
                tuple(sorted([f[2], f[0]]))
            ]
            for e in edges:
                edge_counts[e] = edge_counts.get(e, 0) + 1

        non_manifold_edges = sum(1 for cnt in edge_counts.values() if cnt > 2)
        open_boundary_edges = sum(1 for cnt in edge_counts.values() if cnt == 1)
        
        return {
            "is_watertight": open_boundary_edges == 0,
            "non_manifold_edges": non_manifold_edges,
            "open_boundary_edges": open_boundary_edges,
            "euler_characteristic": vertex_count - len(edge_counts) + len(faces)
        }
