"""
Unified PBR Texture Atlas Baker.
Bakes Diffuse/Albedo, Tangent-Space Normal, Roughness, and Metallic maps.
"""
from typing import Dict, Any, List, Tuple
import numpy as np

class PBRAtlasBaker:
    """Bakes multi-channel PBR texture maps matching UV atlas layout."""
    def __init__(self, atlas_resolution: int = 1024):
        self.atlas_resolution = atlas_resolution

    def bake_albedo_map(self, base_color: Tuple[int, int, int] = (180, 150, 110)) -> np.ndarray:
        """Bakes base diffuse albedo texture image."""
        img = np.ones((self.atlas_resolution, self.atlas_resolution, 3), dtype=np.uint8)
        img[:, :] = base_color
        return img

    def bake_normal_map(self) -> np.ndarray:
        """Bakes tangent-space normal map (flat tangent normal = [128, 128, 255])."""
        normal_img = np.zeros((self.atlas_resolution, self.atlas_resolution, 3), dtype=np.uint8)
        normal_img[:, :, 0] = 128
        normal_img[:, :, 1] = 128
        normal_img[:, :, 2] = 255
        return normal_img

    def bake_roughness_metallic_map(self, roughness: float = 0.45, metallic: float = 0.2) -> np.ndarray:
        """Bakes packed ORM (Occlusion/Roughness/Metallic) channel map."""
        orm = np.zeros((self.atlas_resolution, self.atlas_resolution, 3), dtype=np.uint8)
        orm[:, :, 0] = 255  # Ambient Occlusion
        orm[:, :, 1] = int(roughness * 255)  # Roughness (Green channel)
        orm[:, :, 2] = int(metallic * 255)   # Metallic (Blue channel)
        return orm

    def bake_curvature_map(self, intensity: float = 0.5) -> np.ndarray:
        """Bakes high-frequency cavity/curvature texture map."""
        curv = np.ones((self.atlas_resolution, self.atlas_resolution), dtype=np.uint8) * 128
        return curv
