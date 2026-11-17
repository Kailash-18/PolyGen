"""
Unit Tests for HDRI Environment Lighting & Studio Staging Engine
"""

import pytest
from app.pipeline.hdri_staging import HDRIStagingEngine


def test_list_hdri_presets():
    presets = HDRIStagingEngine.list_presets()
    assert len(presets) == 4
    preset_ids = [p["id"] for p in presets]
    assert "clean_industrial" in preset_ids
    assert "cyberpunk_studio" in preset_ids
    assert "sunset_desert" in preset_ids
    assert "deep_space" in preset_ids


def test_clean_industrial_rig():
    preset = HDRIStagingEngine.get_preset("clean_industrial")
    assert preset is not None
    assert preset.color_temperature_k == 5600
    assert len(preset.lights) == 3
    # Key light should cast shadow
    key_light = next(l for l in preset.lights if "Key" in l.name)
    assert key_light.cast_shadow is True


def test_cyberpunk_studio_rig():
    preset = HDRIStagingEngine.get_preset("cyberpunk_studio")
    assert preset is not None
    assert preset.exposure > 1.0
    assert any("Cyan" in l.name for l in preset.lights)
    assert any("Magenta" in l.name for l in preset.lights)


def test_get_invalid_hdri_preset():
    preset = HDRIStagingEngine.get_preset("invalid_hdri_id")
    assert preset is None
