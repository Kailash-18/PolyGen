"""
Stage 3: Enterprise HDRI Environment Presets Library.
Standardized lighting rigs tailored for medieval weapons, industrial components, and sci-fi props.
"""

from typing import Dict, Any, List, Tuple
from dataclasses import dataclass

@dataclass
class HDRIPreset:
    id: str
    name: str
    category: str
    sun_intensity: float
    ambient_lux: float
    color_temperature_k: int
    recommended_exposure: float

class HDRIPresetsCatalog:
    """Catalog of high-dynamic-range panoramic environment lighting setups."""

    def __init__(self):
        self._presets: Dict[str, HDRIPreset] = {}
        self._register_default_presets()

    def _register_default_presets(self):
        self._presets["studio_neutral"] = HDRIPreset(
            id="studio_neutral",
            name="Neutral Product Photography Studio",
            category="Studio",
            sun_intensity=1.0,
            ambient_lux=1200.0,
            color_temperature_k=5500,
            recommended_exposure=1.0
        )
        self._presets["sunset_warm"] = HDRIPreset(
            id="sunset_warm",
            name="Golden Hour Outdoor Sunset",
            category="Outdoor",
            sun_intensity=3.5,
            ambient_lux=3500.0,
            color_temperature_k=3200,
            recommended_exposure=0.85
        )
        self._presets["medieval_courtyard"] = HDRIPreset(
            id="medieval_courtyard",
            name="Overcast Medieval Stone Courtyard",
            category="Environment",
            sun_intensity=1.8,
            ambient_lux=2400.0,
            color_temperature_k=6500,
            recommended_exposure=1.15
        )
        self._presets["cyberpunk_hangar"] = HDRIPreset(
            id="cyberpunk_hangar",
            name="Industrial Hangar with Neon Accents",
            category="SciFi",
            sun_intensity=0.8,
            ambient_lux=900.0,
            color_temperature_k=7200,
            recommended_exposure=1.30
        )
        self._presets["dark_dungeon"] = HDRIPreset(
            id="dark_dungeon",
            name="Torchlit Underground Crypt",
            category="Atmospheric",
            sun_intensity=0.4,
            ambient_lux=450.0,
            color_temperature_k=2200,
            recommended_exposure=1.60
        )

    def get_preset(self, preset_id: str) -> HDRIPreset:
        return self._presets.get(preset_id, self._presets["studio_neutral"])

    def list_presets(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": p.id,
                "name": p.name,
                "category": p.category,
                "ambient_lux": p.ambient_lux,
                "recommended_exposure": p.recommended_exposure
            }
            for p in self._presets.values()
        ]
