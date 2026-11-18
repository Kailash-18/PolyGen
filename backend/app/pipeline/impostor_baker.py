"""Octahedral Impostor and LOD4 Distant Billboard Generation Module."""
import math
from dataclasses import dataclass
from typing import List, Tuple, Dict, Any, Optional

@dataclass
class ImpostorConfig:
    atlas_resolution: int = 512
    subdivisions: int = 4
    include_depth: bool = True
    include_normals: bool = True
    alpha_cutoff: float = 0.5

class OctahedralProjection:
    """Mathematical conversions between 3D directional vectors and 2D octahedral coordinates."""
    @staticmethod
    def direction_to_uv(direction: Tuple[float, float, float]) -> Tuple[float, float]:
        x, y, z = direction
        l1_norm = abs(x) + abs(y) + abs(z) or 1.0
        ox, oy = x / l1_norm, y / l1_norm
        if z < 0.0:
            ox, oy = (1.0 - abs(oy)) * (1.0 if ox >= 0 else -1.0), (1.0 - abs(ox)) * (1.0 if oy >= 0 else -1.0)
        u = (ox + 1.0) * 0.5
        v = (oy + 1.0) * 0.5
        return (max(0.0, min(1.0, u)), max(0.0, min(1.0, v)))

    @staticmethod
    def uv_to_direction(u: float, v: float) -> Tuple[float, float, float]:
        ox = u * 2.0 - 1.0
        oy = v * 2.0 - 1.0
        oz = 1.0 - abs(ox) - abs(oy)
        if oz < 0.0:
            ox, oy = (1.0 - abs(oy)) * (1.0 if ox >= 0 else -1.0), (1.0 - abs(ox)) * (1.0 if oy >= 0 else -1.0)
        norm = math.sqrt(ox * ox + oy * oy + oz * oz) or 1.0
        return (ox / norm, oy / norm, oz / norm)

class ImpostorBaker:
    """Bakes multi-angle octahedral impostors from 3D meshes."""
    def __init__(self, config: Optional[ImpostorConfig] = None):
        self.config = config or ImpostorConfig()

    def generate_camera_grid(self) -> List[Dict[str, Any]]:
        grid = []
        n = self.config.subdivisions
        for row in range(n):
            for col in range(n):
                u = (col + 0.5) / n
                v = (row + 0.5) / n
                dir_vec = OctahedralProjection.uv_to_direction(u, v)
                grid.append({
                    "tile_index": row * n + col,
                    "row": row, "col": col,
                    "uv_center": (round(u, 4), round(v, 4)),
                    "view_direction": [round(c, 4) for c in dir_vec],
                    "elevation_deg": round(math.degrees(math.asin(max(-1.0, min(1.0, dir_vec[1])))), 2),
                    "azimuth_deg": round(math.degrees(math.atan2(dir_vec[0], dir_vec[2])), 2)
                })
        return grid

    def construct_billboard_quad(self, bounds_min: List[float], bounds_max: List[float]) -> Dict[str, Any]:
        width = bounds_max[0] - bounds_min[0]
        height = bounds_max[1] - bounds_min[1]
        depth = bounds_max[2] - bounds_min[2]
        center = [(bounds_min[0] + bounds_max[0]) * 0.5, (bounds_min[1] + bounds_max[1]) * 0.5, (bounds_min[2] + bounds_max[2]) * 0.5]
        radius = math.sqrt(width * width + height * height + depth * depth) * 0.5
        hw, hh = radius, radius
        quad_vertices = [
            [center[0] - hw, center[1] - hh, center[2]],
            [center[0] + hw, center[1] - hh, center[2]],
            [center[0] + hw, center[1] + hh, center[2]],
            [center[0] - hw, center[1] + hh, center[2]]
        ]
        return {
            "vertices": quad_vertices,
            "faces": [[0, 1, 2], [0, 2, 3]],
            "uvs": [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]],
            "bounding_sphere_radius": round(radius, 4),
            "bounding_center": [round(c, 4) for c in center]
        }

    def bake_impostor_descriptor(self, model_id: str, vertices: List[List[float]], faces: List[List[int]]) -> Dict[str, Any]:
        xs = [v[0] for v in vertices]
        ys = [v[1] for v in vertices]
        zs = [v[2] for v in vertices]
        b_min = [min(xs), min(ys), min(zs)]
        b_max = [max(xs), max(ys), max(zs)]
        camera_grid = self.generate_camera_grid()
        quad = self.construct_billboard_quad(b_min, b_max)
        return {
            "model_id": model_id,
            "lod_level": "LOD4_Impostor",
            "atlas_resolution": self.config.atlas_resolution,
            "tile_grid": f"{self.config.subdivisions}x{self.config.subdivisions}",
            "tile_count": len(camera_grid),
            "camera_angles": camera_grid,
            "billboard_geometry": quad,
            "alpha_cutoff": self.config.alpha_cutoff,
            "features": {
                "depth_encoding": self.config.include_depth,
                "normal_reconstruction": self.config.include_normals,
                "octahedral_hemisphere": True
            }
        }
