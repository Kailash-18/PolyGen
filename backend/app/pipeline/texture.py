"""
Stage 3: PBR Texture Generation & Material Parameterization Engine
Synthesizes high-fidelity multi-map PBR textures: Albedo, Tangent Normal, Roughness, Metalness.
"""

import math
import hashlib
import numpy as np
from PIL import Image, ImageFilter
import trimesh

class TextureEngine:
    def __init__(self, resolution: int = 1024):
        self.resolution = resolution

    def _analyze_palette(self, prompt: str) -> tuple[np.ndarray, np.ndarray, float, float]:
        """
        Determines base color, accent color, target roughness, and metalness from natural language prompt.
        """
        p = prompt.lower()

        # Defaults: Polished Gunmetal Steel
        base_col = np.array([160, 168, 180], dtype=np.float32)
        accent_col = np.array([218, 175, 55], dtype=np.float32)  # Gold trim
        roughness = 0.28
        metalness = 0.90

        # Palette & material overrides
        if any(w in p for w in ["gold", "golden", "brass", "bronze", "gilded"]):
            base_col = np.array([225, 182, 50], dtype=np.float32)
            accent_col = np.array([245, 215, 110], dtype=np.float32)
            roughness = 0.22
            metalness = 0.95
        elif any(w in p for w in ["silver", "chrome", "platinum", "titanium", "mirror"]):
            base_col = np.array([230, 235, 242], dtype=np.float32)
            accent_col = np.array([250, 252, 255], dtype=np.float32)
            roughness = 0.12
            metalness = 0.98
        elif any(w in p for w in ["obsidian", "dark", "shadow", "black", "carbon", "stealth"]):
            base_col = np.array([32, 35, 42], dtype=np.float32)
            accent_col = np.array([65, 70, 82], dtype=np.float32)
            roughness = 0.35
            metalness = 0.70
        elif any(w in p for w in ["blue", "sapphire", "azure", "cobalt", "ice", "frost"]):
            base_col = np.array([35, 115, 235], dtype=np.float32)
            accent_col = np.array([120, 215, 255], dtype=np.float32)
            roughness = 0.20
            metalness = 0.50
        elif any(w in p for w in ["red", "crimson", "ruby", "scarlet", "blood", "fire"]):
            base_col = np.array([215, 32, 55], dtype=np.float32)
            accent_col = np.array([255, 95, 115], dtype=np.float32)
            roughness = 0.30
            metalness = 0.40
        elif any(w in p for w in ["green", "emerald", "jade", "forest", "toxic", "poison"]):
            base_col = np.array([35, 175, 75], dtype=np.float32)
            accent_col = np.array([110, 240, 140], dtype=np.float32)
            roughness = 0.25
            metalness = 0.45
        elif any(w in p for w in ["purple", "violet", "amethyst", "void", "royal"]):
            base_col = np.array([145, 45, 225], dtype=np.float32)
            accent_col = np.array([215, 120, 255], dtype=np.float32)
            roughness = 0.22
            metalness = 0.65
        elif any(w in p for w in ["wood", "wooden", "oak", "mahogany", "bark", "cedar"]):
            base_col = np.array([118, 72, 42], dtype=np.float32)
            accent_col = np.array([82, 48, 26], dtype=np.float32)
            roughness = 0.75
            metalness = 0.02
        elif any(w in p for w in ["stone", "marble", "rock", "granite", "concrete"]):
            base_col = np.array([195, 192, 188], dtype=np.float32)
            accent_col = np.array([140, 138, 134], dtype=np.float32)
            roughness = 0.80
            metalness = 0.05
        elif any(w in p for w in ["leather"]):
            base_col = np.array([92, 58, 38], dtype=np.float32)
            accent_col = np.array([68, 40, 24], dtype=np.float32)
            roughness = 0.68
            metalness = 0.05
        elif any(w in p for w in ["cyber", "neon", "sci-fi", "futuristic"]):
            base_col = np.array([24, 28, 36], dtype=np.float32)
            accent_col = np.array([0, 240, 255], dtype=np.float32)
            roughness = 0.20
            metalness = 0.85

        return base_col, accent_col, roughness, metalness

    def _generate_albedo_map(self, prompt: str) -> Image.Image:
        res = self.resolution
        base_col, accent_col, _, _ = self._analyze_palette(prompt)

        # Coordinate grid for procedural gradient / panel patterning
        y, x = np.ogrid[:res, :res]

        # Subtle vignette / ambient darkening toward UV borders
        center_dist = np.sqrt(((x - res / 2) / (res / 2)) ** 2 + ((y - res / 2) / (res / 2)) ** 2)
        vignette = 1.0 - np.clip(center_dist * 0.15, 0.0, 0.25)

        # Multi-frequency procedural surface noise
        np.random.seed(int(hashlib.md5(prompt.encode("utf-8")).hexdigest()[:8], 16))
        fine_noise = np.random.normal(0, 7.0, (res, res, 1))
        macro_noise = np.random.normal(0, 12.0, (res // 8, res // 8, 1))
        macro_img = Image.fromarray(macro_noise[:, :, 0]).resize((res, res), resample=Image.Resampling.BILINEAR)
        macro_arr = np.array(macro_img)[:, :, np.newaxis]

        # Decorative panel bands
        panel_stripe = (np.sin(y / 32.0) * 0.5 + 0.5) ** 8.0 * 25.0

        # Combine base + accent highlights
        img_arr = base_col + fine_noise + macro_arr + panel_stripe
        img_arr = img_arr * vignette[:, :, np.newaxis]

        # Inset glowing accent lines for sci-fi/cyberpunk
        if any(w in prompt.lower() for w in ["cyber", "neon", "sci-fi", "plasma"]):
            laser_lines = ((np.sin(x / 48.0) > 0.96) | (np.sin(y / 48.0) > 0.96)).astype(np.float32)
            img_arr = img_arr * (1.0 - laser_lines[:, :, np.newaxis]) + accent_col * laser_lines[:, :, np.newaxis]

        img_arr = np.clip(img_arr, 0, 255).astype(np.uint8)
        return Image.fromarray(img_arr, mode="RGB")

    def _generate_normal_map(self) -> Image.Image:
        res = self.resolution
        # Base flat normal (tangent space: 128, 128, 255)
        normals = np.zeros((res, res, 3), dtype=np.float32)
        normals[:, :, 0] = 128.0
        normals[:, :, 1] = 128.0
        normals[:, :, 2] = 255.0

        # Subtle micro-surface bumps
        bump_noise = np.random.normal(0, 6.0, (res, res, 2))
        normals[:, :, :2] += bump_noise

        # Panel groove bevels
        y, x = np.ogrid[:res, :res]
        bevel_x = np.sin(x / 32.0) * 14.0
        bevel_y = np.cos(y / 32.0) * 14.0
        normals[:, :, 0] += bevel_x
        normals[:, :, 1] += bevel_y

        normals = np.clip(normals, 0, 255).astype(np.uint8)
        norm_img = Image.fromarray(normals, mode="RGB")
        return norm_img.filter(ImageFilter.SMOOTH)

    def _generate_roughness_map(self, prompt: str) -> Image.Image:
        res = self.resolution
        _, _, roughness, _ = self._analyze_palette(prompt)
        base_val = int(roughness * 255.0)

        rough_arr = np.full((res, res), base_val, dtype=np.float32)
        noise = np.random.normal(0, 10.0, (res, res))
        rough_arr = np.clip(rough_arr + noise, 10, 245).astype(np.uint8)
        return Image.fromarray(rough_arr, mode="L")

    def _generate_metalness_map(self, prompt: str) -> Image.Image:
        res = self.resolution
        _, _, _, metalness = self._analyze_palette(prompt)
        base_val = int(metalness * 255.0)

        metal_arr = np.full((res, res), base_val, dtype=np.uint8)
        return Image.fromarray(metal_arr, mode="L")

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
