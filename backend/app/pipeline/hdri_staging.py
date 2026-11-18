"""
Stage 4: HDRI Environment Lighting & Studio Staging Engine
Generates physical Three.js environment lighting rigs, color-temperature calibrated directional keys,
and PMREM environment map presets for realistic material inspection.
"""

from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
import math


@dataclass
class LightSourceSpec:
    name: str
    type: str  # directional, ambient, point, hemisphere
    color_hex: str
    intensity: float
    position: List[float]
    cast_shadow: bool = False


@dataclass
class HDRIScenePreset:
    id: str
    name: str
    category: str
    description: str
    color_temperature_k: int
    exposure: float
    background_color: str
    ambient_intensity: float
    lights: List[LightSourceSpec]
    ground_reflection: bool = True
    ground_roughness: float = 0.4


class HDRIStagingEngine:
    """
    Synthesizes multi-source photometric studio lighting rigs for WebGL PBR scenes.
    """

    PRESETS: Dict[str, HDRIScenePreset] = {
        "clean_industrial": HDRIScenePreset(
            id="clean_industrial",
            name="Neutral Industrial Studio",
            category="Studio / Neutral",
            description="High-CRI 5600K 3-point key/fill/back studio rig with soft neutral floor reflection.",
            color_temperature_k=5600,
            exposure=1.0,
            background_color="#121519",
            ambient_intensity=0.45,
            lights=[
                LightSourceSpec(
                    name="Key Light (North-East)",
                    type="directional",
                    color_hex="#F4F8FF",
                    intensity=1.8,
                    position=[5.0, 8.0, 5.0],
                    cast_shadow=True
                ),
                LightSourceSpec(
                    name="Fill Light (West)",
                    type="directional",
                    color_hex="#E0E8F5",
                    intensity=0.8,
                    position=[-6.0, 4.0, 3.0],
                    cast_shadow=False
                ),
                LightSourceSpec(
                    name="Rim Light (South)",
                    type="directional",
                    color_hex="#FFFFFF",
                    intensity=1.2,
                    position=[0.0, 6.0, -8.0],
                    cast_shadow=False
                )
            ],
            ground_reflection=True,
            ground_roughness=0.3
        ),
        "cyberpunk_studio": HDRIScenePreset(
            id="cyberpunk_studio",
            name="Neo-Tokyo Cyberpunk Rig",
            category="Dramatic / Stylized",
            description="Complementary electric cyan key and hot magenta rim with high-contrast specular bounce.",
            color_temperature_k=8500,
            exposure=1.25,
            background_color="#080811",
            ambient_intensity=0.25,
            lights=[
                LightSourceSpec(
                    name="Cyan Key",
                    type="directional",
                    color_hex="#00E5FF",
                    intensity=2.2,
                    position=[6.0, 7.0, 4.0],
                    cast_shadow=True
                ),
                LightSourceSpec(
                    name="Magenta Rim",
                    type="directional",
                    color_hex="#FF007F",
                    intensity=2.6,
                    position=[-5.0, 5.0, -6.0],
                    cast_shadow=False
                ),
                LightSourceSpec(
                    name="Deep Indigo Floor Bounce",
                    type="hemisphere",
                    color_hex="#1E0850",
                    intensity=0.6,
                    position=[0.0, -2.0, 0.0],
                    cast_shadow=False
                )
            ],
            ground_reflection=True,
            ground_roughness=0.15
        ),
        "sunset_desert": HDRIScenePreset(
            id="sunset_desert",
            name="Golden Hour Sunset",
            category="Outdoor / Natural",
            description="Warm low-angle 3200K sunlight with deep azure atmospheric skylight fill.",
            color_temperature_k=3200,
            exposure=1.1,
            background_color="#181315",
            ambient_intensity=0.4,
            lights=[
                LightSourceSpec(
                    name="Low-Angle Sun",
                    type="directional",
                    color_hex="#FFA858",
                    intensity=2.8,
                    position=[8.0, 3.0, 6.0],
                    cast_shadow=True
                ),
                LightSourceSpec(
                    name="Sky Dome Fill",
                    type="hemisphere",
                    color_hex="#6C8CD5",
                    intensity=0.9,
                    position=[0.0, 10.0, 0.0],
                    cast_shadow=False
                )
            ],
            ground_reflection=False,
            ground_roughness=0.8
        ),
        "deep_space": HDRIScenePreset(
            id="deep_space",
            name="Void Deep Space Sun",
            category="Cosmic / High-Contrast",
            description="Pure harsh vacuum direct solar illumination with ultra-dim cold nebula bounce.",
            color_temperature_k=6500,
            exposure=1.35,
            background_color="#030407",
            ambient_intensity=0.1,
            lights=[
                LightSourceSpec(
                    name="Direct Stellar Beam",
                    type="directional",
                    color_hex="#FFFFFF",
                    intensity=3.4,
                    position=[10.0, 12.0, 2.0],
                    cast_shadow=True
                ),
                LightSourceSpec(
                    name="Nebula Ambient Fill",
                    type="ambient",
                    color_hex="#0A1838",
                    intensity=0.25,
                    position=[0.0, 0.0, 0.0],
                    cast_shadow=False
                )
            ],
            ground_reflection=False,
            ground_roughness=0.9
        )
    }

    @classmethod
    def list_presets(cls) -> List[Dict[str, Any]]:
        return [asdict(p) for p in cls.PRESETS.values()]

    @classmethod
    def get_preset(cls, preset_id: str) -> Optional[HDRIScenePreset]:
        return cls.PRESETS.get(preset_id)
