"""
Unit tests for PBRShaderEngine optical models and Beer-Lambert attenuation.
"""

import numpy as np
from app.pipeline.pbr_shader_engine import PBRShaderEngine

def test_compute_f0_from_ior():
    engine = PBRShaderEngine()
    # Water n=1.33 -> F0 ~ 0.02
    f0_water = engine.compute_f0_from_ior(1.33)
    assert 0.019 < f0_water < 0.022

    # Sapphire n=1.77 -> F0 ~ 0.077
    f0_sapphire = engine.compute_f0_from_ior(1.77)
    assert 0.07 < f0_sapphire < 0.08

def test_evaluate_fresnel_schlick():
    engine = PBRShaderEngine()
    f0 = 0.04
    # At grazing angle (cos_theta=0), F -> 1.0
    f_grazing = engine.evaluate_fresnel_schlick(f0, 0.0)
    assert np.isclose(f_grazing, 1.0)

    # At normal incidence (cos_theta=1), F -> F0
    f_normal = engine.evaluate_fresnel_schlick(f0, 1.0)
    assert np.isclose(f_normal, f0)

def test_evaluate_clearcoat_layer():
    engine = PBRShaderEngine()
    total_spec = engine.evaluate_clearcoat_layer(
        base_reflectance=0.5,
        clearcoat_factor=1.0,
        clearcoat_roughness=0.05,
        cos_theta=0.8
    )
    assert 0.0 <= total_spec <= 1.0
    assert total_spec > 0.04

def test_beer_lambert_attenuation():
    engine = PBRShaderEngine()
    trans = engine.compute_beer_lambert_attenuation(
        thickness=0.5,
        attenuation_distance=1.0,
        attenuation_color=(0.1, 0.5, 0.9)
    )
    assert len(trans) == 3
    assert all(0.0 <= c <= 1.0 for c in trans)
