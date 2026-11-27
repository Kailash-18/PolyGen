"""
Stage 3: PBR Texture Generation & Material Parameterization Engine
"""

import math
import numpy as np
from PIL import Image
import trimesh

class TextureEngine:
    def __init__(self, resolution: int = 512):
        self.resolution = resolution

    def _generate_albedo_map(self, prompt: str) -> Image.Image:
        p = prompt.lower()
        res = self.resolution

        if "sword" in p or "blade" in p:
            base_col = np.array([210, 215, 225], dtype=np.uint8)
            noise = np.random.randint(-15, 15, (res, res, 3), dtype=np.int16)
        elif "shield" in p:
            base_col = np.array([160, 110, 60], dtype=np.uint8)
            noise = np.random.randint(-20, 20, (res, res, 3), dtype=np.int16)
        elif "crystal" in p:
            base_col = np.array([80, 200, 240], dtype=np.uint8)
            noise = np.random.randint(-25, 25, (res, res, 3), dtype=np.int16)
        else:
            base_col = np.array([180, 175, 170], dtype=np.uint8)
            noise = np.random.randint(-18, 18, (res, res, 3), dtype=np.int16)

        img_arr = np.clip(base_col + noise, 0, 255).astype(np.uint8)
        return Image.fromarray(img_arr, mode="RGB")

    def _generate_normal_map(self) -> Image.Image:
        res = self.resolution
        normals = np.zeros((res, res, 3), dtype=np.uint8)
        normals[:, :, 0] = 128
        normals[:, :, 1] = 128
        normals[:, :, 2] = 255

        perturbation = np.random.randint(-8, 8, (res, res, 2), dtype=np.int16)
        normals[:, :, :2] = np.clip(normals[:, :, :2] + perturbation, 0, 255).astype(np.uint8)
        return Image.fromarray(normals, mode="RGB")

    def _generate_roughness_map(self, prompt: str) -> Image.Image:
        p = prompt.lower()
        val = 45 if ("sword" in p or "metal" in p) else 140
        arr = np.full((self.resolution, self.resolution), val, dtype=np.uint8)
        noise = np.random.randint(-12, 12, (self.resolution, self.resolution), dtype=np.int16)
        return Image.fromarray(np.clip(arr + noise, 0, 255).astype(np.uint8), mode="L")

    def _generate_metalness_map(self, prompt: str) -> Image.Image:
        p = prompt.lower()
        val = 220 if ("sword" in p or "metal" in p or "shield" in p) else 15
        arr = np.full((self.resolution, self.resolution), val, dtype=np.uint8)
        return Image.fromarray(arr, mode="L")

    def synthesize_pbr_maps(self, prompt: str, mesh: trimesh.Trimesh = None) -> dict[str, Image.Image]:
        return {
            "albedo": self._generate_albedo_map(prompt),
            "normal": self._generate_normal_map(),
            "roughness": self._generate_roughness_map(prompt),
            "metalness": self._generate_metalness_map(prompt)
        }

    def apply_textures_to_mesh(self, mesh: trimesh.Trimesh, pbr_maps: dict[str, Image.Image]) -> trimesh.Trimesh:
        textured = mesh.copy()
        albedo = pbr_maps["albedo"]
        textured.visual = trimesh.visual.TextureVisuals(
            uv=mesh.visual.uv if hasattr(mesh.visual, "uv") and mesh.visual.uv is not None else None,
            image=albedo
        )
        return textured
