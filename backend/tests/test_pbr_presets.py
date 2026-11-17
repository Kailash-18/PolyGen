"""
Unit Tests for PBR Material Presets Engine
"""

import pytest
from PIL import Image
from app.pipeline.pbr_presets import PBRMaterialPresetEngine


def test_list_presets():
    presets = PBRMaterialPresetEngine.list_presets()
    assert len(presets) == 6
    preset_ids = [p["id"] for p in presets]
    assert "cyberpunk_neon" in preset_ids
    assert "weathered_rust" in preset_ids
    assert "scifi_matte" in preset_ids
    assert "anodized_titanium" in preset_ids
    assert "obsidian_glass" in preset_ids
    assert "gold_leaf" in preset_ids


def test_get_valid_preset():
    preset = PBRMaterialPresetEngine.get_preset("cyberpunk_neon")
    assert preset is not None
    assert preset.roughness == 0.18
    assert preset.metalness == 0.85
    assert preset.emissive_intensity > 0.0


def test_get_invalid_preset():
    preset = PBRMaterialPresetEngine.get_preset("non_existent_id")
    assert preset is None


def test_bake_preset_maps():
    maps = PBRMaterialPresetEngine.bake_preset_maps("weathered_rust", resolution=128)
    assert "albedo" in maps
    assert "roughness" in maps
    assert "metalness" in maps
    assert "normal" in maps

    assert maps["albedo"].size == (128, 128)
    assert maps["roughness"].size == (128, 128)
    assert maps["metalness"].size == (128, 128)
    assert maps["normal"].size == (128, 128)


def test_bake_preset_with_base_albedo():
    base = Image.new("RGB", (64, 64), color=(100, 100, 100))
    maps = PBRMaterialPresetEngine.bake_preset_maps("gold_leaf", resolution=64, base_albedo=base)
    assert maps["albedo"].size == (64, 64)
