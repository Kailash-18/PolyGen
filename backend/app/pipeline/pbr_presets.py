"""
Stage 3/4: PBR Material Presets & Shader Parameter Synthesizer
Provides physically-calibrated PBR material configurations (Cyberpunk, Rust, Sci-Fi Matte, Titanium, Obsidian, Gold)
for WebGL Three.js PBR materials, Unreal Engine 5 Material Instances, and Unity URP/HDRP Lit shaders.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
import numpy as np
from PIL import Image


@dataclass
class PBRMaterialPreset:
    id: str
    name: str
    category: str
    description: str
    base_color_rgb: List[int]
    roughness: float
    metalness: float
    emissive_rgb: List[float]
    emissive_intensity: float
    clearcoat: float
    clearcoat_roughness: float
    normal_scale: float


class PBRMaterialPresetEngine:
    """
    Library and map-baker for high-fidelity physically calibrated materials.
    """

    PRESETS: Dict[str, PBRMaterialPreset] = {
        "cyberpunk_neon": PBRMaterialPreset(
            id="cyberpunk_neon",
            name="Cyberpunk Neon Alloy",
            category="Sci-Fi / Futuristic",
            description="High-sheen conductive alloy with electric cyan specular response and electroluminescent trim.",
            base_color_rgb=[0, 229, 255],
            roughness=0.18,
            metalness=0.85,
            emissive_rgb=[0.0, 0.85, 1.0],
            emissive_intensity=2.2,
            clearcoat=0.6,
            clearcoat_roughness=0.1,
            normal_scale=1.2
        ),
        "weathered_rust": PBRMaterialPreset(
            id="weathered_rust",
            name="Weathered Ferrous Rust",
            category="Industrial / Grunge",
            description="Heavy oxidized iron crust with irregular pitting, high roughness, and low surface conductance.",
            base_color_rgb=[139, 58, 28],
            roughness=0.88,
            metalness=0.10,
            emissive_rgb=[0.0, 0.0, 0.0],
            emissive_intensity=0.0,
            clearcoat=0.0,
            clearcoat_roughness=1.0,
            normal_scale=1.8
        ),
        "scifi_matte": PBRMaterialPreset(
            id="scifi_matte",
            name="Aerospace Tactical Matte",
            category="Military / Aerospace",
            description="Anti-reflective carbon-composite tactical coating with satin sheen and subtle amber accents.",
            base_color_rgb=[45, 49, 54],
            roughness=0.45,
            metalness=0.30,
            emissive_rgb=[1.0, 0.6, 0.1],
            emissive_intensity=0.3,
            clearcoat=0.2,
            clearcoat_roughness=0.3,
            normal_scale=1.0
        ),
        "anodized_titanium": PBRMaterialPreset(
            id="anodized_titanium",
            name="Anodized Royal Titanium",
            category="Exotic Metals",
            description="Electrochemically treated Grade 5 titanium exhibiting thin-film chromatic interference.",
            base_color_rgb=[106, 13, 173],
            roughness=0.22,
            metalness=0.94,
            emissive_rgb=[0.0, 0.0, 0.0],
            emissive_intensity=0.0,
            clearcoat=0.8,
            clearcoat_roughness=0.15,
            normal_scale=1.1
        ),
        "obsidian_glass": PBRMaterialPreset(
            id="obsidian_glass",
            name="Volcanic Obsidian Glass",
            category="Vitreous Minerals",
            description="Glossy jet-black natural silicate glass with deep dielectric mirror highlights.",
            base_color_rgb=[12, 13, 14],
            roughness=0.08,
            metalness=0.05,
            emissive_rgb=[0.0, 0.0, 0.0],
            emissive_intensity=0.0,
            clearcoat=1.0,
            clearcoat_roughness=0.05,
            normal_scale=0.6
        ),
        "gold_leaf": PBRMaterialPreset(
            id="gold_leaf",
            name="24-Karat Gilded Gold Leaf",
            category="Precious Metals",
            description="Pure 24k polished gold surface with characteristic spectral reflectance and mirror shine.",
            base_color_rgb=[255, 215, 0],
            roughness=0.12,
            metalness=0.98,
            emissive_rgb=[0.0, 0.0, 0.0],
            emissive_intensity=0.0,
            clearcoat=0.4,
            clearcoat_roughness=0.1,
            normal_scale=0.8
        )
    }

    @classmethod
    def list_presets(cls) -> List[Dict[str, Any]]:
        """Returns all preset metadata for frontend selection."""
        return [asdict(p) for p in cls.PRESETS.values()]

    @classmethod
    def get_preset(cls, preset_id: str) -> Optional[PBRMaterialPreset]:
        return cls.PRESETS.get(preset_id)

    @classmethod
    def bake_preset_maps(
        cls,
        preset_id: str,
        resolution: int = 512,
        base_albedo: Optional[Image.Image] = None
    ) -> Dict[str, Image.Image]:
        """
        Bakes customized PBR texture maps (Albedo, Roughness, Metalness, Normal)
        conforming to the selected material preset.
        """
        preset = cls.PRESETS.get(preset_id, cls.PRESETS["cyberpunk_neon"])
        res = resolution

        # 1. Albedo Map
        if base_albedo is not None:
            # Blend existing albedo with preset color
            albedo_np = np.array(base_albedo.resize((res, res)).convert("RGB"), dtype=np.float32)
            tint = np.array(preset.base_color_rgb, dtype=np.float32)
            blended = np.clip(0.4 * albedo_np + 0.6 * tint, 0, 255).astype(np.uint8)
            albedo_img = Image.fromarray(blended, mode="RGB")
        else:
            base_arr = np.zeros((res, res, 3), dtype=np.float32)
            base_arr[:, :] = preset.base_color_rgb
            noise = np.random.normal(0, 10, (res, res, 3))
            albedo_np = np.clip(base_arr + noise, 0, 255).astype(np.uint8)
            albedo_img = Image.fromarray(albedo_np, mode="RGB")

        # 2. Roughness Map (Grayscale L)
        roughness_val = int(np.clip(preset.roughness * 255, 0, 255))
        r_arr = np.full((res, res), roughness_val, dtype=np.int16)
        r_noise = np.random.randint(-12, 12, (res, res), dtype=np.int16)
        roughness_img = Image.fromarray(np.clip(r_arr + r_noise, 0, 255).astype(np.uint8), mode="L")

        # 3. Metalness Map (Grayscale L)
        metalness_val = int(np.clip(preset.metalness * 255, 0, 255))
        m_arr = np.full((res, res), metalness_val, dtype=np.uint8)
        metalness_img = Image.fromarray(m_arr, mode="L")

        # 4. Normal Map (RGB tangent space)
        normal_arr = np.zeros((res, res, 3), dtype=np.uint8)
        normal_arr[:, :, 0] = 128
        normal_arr[:, :, 1] = 128
        normal_arr[:, :, 2] = 255
        pert_scale = int(8 * preset.normal_scale)
        perturbation = np.random.randint(-pert_scale, pert_scale + 1, (res, res, 2), dtype=np.int16)
        normal_arr[:, :, :2] = np.clip(normal_arr[:, :, :2] + perturbation, 0, 255).astype(np.uint8)
        normal_img = Image.fromarray(normal_arr, mode="RGB")

        return {
            "albedo": albedo_img,
            "roughness": roughness_img,
            "metalness": metalness_img,
            "normal": normal_img
        }
