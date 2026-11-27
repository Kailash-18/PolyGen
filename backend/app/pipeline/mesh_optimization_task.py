"""
Stage 3: Asynchronous Mesh Optimization Task Runner.
Coordinates QEM decimation, normal map baking, and PBR material synthesis with progress events.
"""

from typing import Dict, Any, List, Optional
import time
import numpy as np

from app.pipeline.qem_decimator import QEMDecimator
from app.pipeline.pbr_material_system import PBRMaterialSystem
from app.pipeline.normal_baker import HighToLowNormalBaker

class MeshOptimizationRunner:
    """Orchestrates end-to-end 500k -> 10k decimation and PBR material binding."""

    def __init__(self):
        self.decimator = QEMDecimator(target_faces=10000)
        self.material_system = PBRMaterialSystem()
        self.normal_baker = HighToLowNormalBaker(resolution=1024)

    def run_optimization(
        self,
        vertices: np.ndarray,
        faces: np.ndarray,
        target_faces: int = 10000,
        preset_name: str = "medieval_rusted_iron"
    ) -> Dict[str, Any]:
        """
        Executes full pipeline:
        1. QEM edge collapse simplification
        2. Normal map delta generation
        3. Three.js PBR material compilation
        """
        start_time = time.time()
        dec_v, dec_f, metrics = self.decimator.decimate_mesh(
            vertices=vertices,
            faces=faces,
            target_faces=target_faces
        )

        high_normals = np.zeros_like(vertices)
        low_normals = np.zeros_like(dec_v)

        normal_map = self.normal_baker.bake_normal_map(
            high_poly_verts=vertices,
            high_poly_normals=high_normals,
            low_poly_verts=dec_v,
            low_poly_normals=low_normals
        )

        pbr_material = self.material_system.compile_threejs_material(preset_name=preset_name)
        elapsed_sec = round(time.time() - start_time, 4)

        return {
            "status": "completed",
            "execution_time_sec": elapsed_sec,
            "metrics": metrics,
            "material": pbr_material,
            "normal_map_resolution": list(normal_map.shape)
        }
