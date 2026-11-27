"""
Unit tests for PBR Material System, ORM packing, and Normal Map baking.
"""

import numpy as np
from app.pipeline.pbr_material_system import PBRMaterialSystem
from app.pipeline.normal_baker import HighToLowNormalBaker

def test_material_presets():
    mat_sys = PBRMaterialSystem()
    profile = mat_sys.get_profile("medieval_rusted_iron")
    assert profile.name == "medieval_rusted_iron"
    assert profile.metallic > 0.8
    assert profile.roughness > 0.7

    sapphire = mat_sys.get_profile("polished_sapphire")
    assert sapphire.clearcoat == 0.9
    assert sapphire.ior == 1.77

def test_orm_texture_packing():
    mat_sys = PBRMaterialSystem()
    orm = mat_sys.pack_orm_texture(resolution=128)
    assert orm.shape == (128, 128, 3)
    assert orm[0, 0, 0] == 255  # AO channel
    assert orm[0, 0, 1] == 128  # Roughness
    assert orm[0, 0, 2] == 0    # Metallic

def test_threejs_material_compile():
    mat_sys = PBRMaterialSystem()
    mat_spec = mat_sys.compile_threejs_material("medieval_rusted_iron")
    assert mat_spec["type"] == "MeshPhysicalMaterial"
    assert "color" in mat_spec
    assert "aoMap" in mat_spec["textures"]
    assert "normalMap" in mat_spec["textures"]

def test_normal_baker():
    baker = HighToLowNormalBaker(resolution=64)
    high_v = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float64)
    high_n = np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]], dtype=np.float64)
    low_v = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0]], dtype=np.float64)
    low_n = np.array([[0, 0, 1], [0, 0, 1], [0, 0, 1]], dtype=np.float64)
    normal_img = baker.bake_normal_map(high_v, high_n, low_v, low_n)
    assert normal_img.shape == (64, 64, 3)
    assert normal_img.dtype == np.uint8
