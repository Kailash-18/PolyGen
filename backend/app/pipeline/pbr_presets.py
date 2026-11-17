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
        return [asdict(p) for p in cls.PRESETS.values()]

    @classmethod
    def get_preset(cls, preset_id: str) -> Optional[PBRMaterialPreset]:
        return cls.PRESETS.get(preset_id)
