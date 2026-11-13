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
        """Repairs topological defects, eliminates degenerate triangles, and ensures manifoldness"""
        cleaned = mesh.copy()
        if hasattr(cleaned, "process"):
            cleaned.process(validate=True)

        if not cleaned.is_watertight:
            trimesh.repair.fill_holes(cleaned)
            trimesh.repair.fix_winding(cleaned)
            trimesh.repair.fix_inversion(cleaned)

        return cleaned
