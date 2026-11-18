import pytest
from app.pipeline.advanced_pbr import ADVANCED_PBR_CATALOG, AdvancedPBRMaterial

def test_clearcoat_gltf_export():
    mat = AdvancedPBRMaterial(name="TestClearcoat", clearcoat=0.9, clearcoat_roughness=0.05)
    gltf_dict = mat.to_gltf_pbr_dict()
    assert "extensions" in gltf_dict
    assert "KHR_materials_clearcoat" in gltf_dict["extensions"]

def test_transmission_gltf_export():
    mat = AdvancedPBRMaterial(name="TestGlass", transmission=0.95, ior=1.52)
    gltf_dict = mat.to_gltf_pbr_dict()
    assert "KHR_materials_transmission" in gltf_dict["extensions"]
