"""
Unit tests for GLTFExtensionSerializer and MultiUVGenerator.
"""

import numpy as np
from app.pipeline.gltf_extension_serializer import GLTFExtensionSerializer
from app.pipeline.multi_uv_generator import MultiUVGenerator
from app.pipeline.radiance_probe import RadianceProbe

def test_clearcoat_and_ior_serialization():
    serializer = GLTFExtensionSerializer()
    cc_ext = serializer.serialize_clearcoat_extension(0.8, 0.03)
    assert cc_ext["clearcoatFactor"] == 0.8
    assert cc_ext["clearcoatRoughnessFactor"] == 0.03

    ior_ext = serializer.serialize_ior_extension(1.77)
    assert ior_ext["ior"] == 1.77

def test_compile_all_extensions():
    serializer = GLTFExtensionSerializer()
    params = {
        "clearcoat": 0.9,
        "ior": 1.77,
        "transmission": 0.85,
        "emissive_strength": 3.0
    }
    exts = serializer.compile_all_extensions(params)
    assert "KHR_materials_clearcoat" in exts
    assert "KHR_materials_ior" in exts
    assert "KHR_materials_transmission" in exts
    assert "KHR_materials_emissive_strength" in exts

def test_multi_uv_generator():
    uv_gen = MultiUVGenerator()
    verts = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float32)
    faces = np.array([[0, 1, 2]], dtype=np.int32)
    uv1 = uv_gen.generate_lightmap_uv1(verts, faces)
    assert uv1.shape == (3, 2)
    assert np.all(uv1 >= 0.0) and np.all(uv1 <= 1.0)

def test_radiance_probe_sh_and_brdf_lut():
    probe = RadianceProbe()
    normal = np.array([0.0, 1.0, 0.0])
    irradiance = probe.evaluate_sh_irradiance(normal)
    assert irradiance > 0.0

    lut = probe.generate_brdf_lut(resolution=32)
    assert lut.shape == (32, 32, 2)
