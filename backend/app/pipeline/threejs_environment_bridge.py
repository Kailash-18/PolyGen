"""
Stage 3: Three.js WebGL Scene Environment Serializer.
Packages PMREM environment maps, background blur, and lighting rigs for WebGL canvases.
"""

from typing import Dict, Any, List, Optional
from app.pipeline.hdri_presets import HDRIPresetsCatalog

class ThreeJSEnvironmentBridge:
    """Serializes scene-level lighting and background parameters for Three.js."""

    def __init__(self):
        self.catalog = HDRIPresetsCatalog()

    def build_scene_environment_config(
        self,
        preset_id: str = "studio_neutral",
        background_blur: float = 0.15,
        rotation_y_deg: float = 0.0
    ) -> Dict[str, Any]:
        """Constructs JSON payload for direct binding into Three.js Scene."""
        preset = self.catalog.get_preset(preset_id)
        return {
            "environmentPreset": preset.id,
            "environmentName": preset.name,
            "environmentIntensity": 1.0,
            "backgroundBlurriness": float(max(0.0, min(1.0, background_blur))),
            "backgroundRotation": [0.0, float(rotation_y_deg), 0.0],
            "lighting": {
                "ambientLux": preset.ambient_lux,
                "colorTemperature": preset.color_temperature_k,
                "sunIntensity": preset.sun_intensity
            }
        }

    def compile_postprocessing_manifest(
        self,
        tonemapping_type: str = "ACESFilmicToneMapping",
        exposure: float = 1.0,
        bloom_enabled: bool = True
    ) -> Dict[str, Any]:
        """Compiles post-processing pass parameters (tone mapping + unreal bloom)."""
        return {
            "toneMapping": tonemapping_type,
            "toneMappingExposure": float(max(0.1, min(5.0, exposure))),
            "bloom": {
                "enabled": bloom_enabled,
                "threshold": 1.2,
                "strength": 0.45,
                "radius": 0.85
            }
        }
