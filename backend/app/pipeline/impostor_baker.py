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
