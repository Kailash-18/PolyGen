"""
2D UV Island Atlas Bin-Packing Optimizer.
Packs multiple UV chart islands into unified square texture atlas layout.
"""
from typing import Dict, Any, List, Tuple
import numpy as np

class AtlasBinPacker:
    """Packs 2D UV chart bounding boxes into [0.0, 1.0] texture atlas with gutter margins."""
    def __init__(self, atlas_size: int = 2048, gutter_pixels: int = 8):
        self.atlas_size = atlas_size
        self.gutter_pixels = gutter_pixels
        self.gutter_uv = gutter_pixels / atlas_size

    def pack_uv_charts(self, chart_uvs: List[np.ndarray]) -> Tuple[List[np.ndarray], float]:
        """Packs multiple UV coordinate arrays into non-overlapping atlas space."""
        if not chart_uvs:
            return [], 1.0

        packed = []
        n_charts = len(chart_uvs)
        grid_dim = int(np.ceil(np.sqrt(n_charts)))
        cell_size = (1.0 - (grid_dim + 1) * self.gutter_uv) / max(1, grid_dim)

        for idx, chart in enumerate(chart_uvs):
            row = idx // grid_dim
            col = idx % grid_dim
            offset_x = self.gutter_uv + col * (cell_size + self.gutter_uv)
            offset_y = self.gutter_uv + row * (cell_size + self.gutter_uv)
            
            # Scale chart to fit cell
            norm_chart = chart.copy()
            norm_chart[:, 0] = offset_x + chart[:, 0] * cell_size
            norm_chart[:, 1] = offset_y + chart[:, 1] * cell_size
            packed.append(norm_chart)

        packing_efficiency = float(n_charts * (cell_size ** 2))
        return packed, packing_efficiency

    def apply_gutter_margin(self, uvs: np.ndarray, margin: float = 0.01) -> np.ndarray:
        """Scales UV coordinates inward to guarantee safe boundary margins."""
        res = uvs.copy()
        res[:, 0] = margin + res[:, 0] * (1.0 - 2.0 * margin)
        res[:, 1] = margin + res[:, 1] * (1.0 - 2.0 * margin)
        return np.clip(res, 0.0, 1.0)

    def normalize_uvs(self, uvs: np.ndarray) -> np.ndarray:
        """Normalizes arbitrary bounding box UVs into canonical [0.0, 1.0] coordinates."""
        min_u, max_u = np.min(uvs[:, 0]), np.max(uvs[:, 0])
        min_v, max_v = np.min(uvs[:, 1]), np.max(uvs[:, 1])
        range_u = max(1e-6, max_u - min_u)
        range_v = max(1e-6, max_v - min_v)
        
        norm = np.zeros_like(uvs)
        norm[:, 0] = (uvs[:, 0] - min_u) / range_u
        norm[:, 1] = (uvs[:, 1] - min_v) / range_v
        return norm
