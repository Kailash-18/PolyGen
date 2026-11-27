"""Unit tests for AtlasBinPacker and PBR Baker."""
import pytest
import numpy as np
from app.pipeline.atlas_packer import AtlasBinPacker
from app.pipeline.pbr_baker import PBRAtlasBaker

def test_pack_uv_charts():
    packer = AtlasBinPacker(atlas_size=1024, gutter_pixels=4)
    chart1 = np.array([[0.0, 0.0], [1.0, 1.0]])
    chart2 = np.array([[0.0, 0.0], [1.0, 1.0]])
    packed, eff = packer.pack_uv_charts([chart1, chart2])
    assert len(packed) == 2
    assert eff > 0.0

def test_pbr_baker_maps():
    baker = PBRAtlasBaker(atlas_resolution=128)
    albedo = baker.bake_albedo_map()
    normal = baker.bake_normal_map()
    orm = baker.bake_roughness_metallic_map()
    assert albedo.shape == (128, 128, 3)
    assert normal.shape == (128, 128, 3)
    assert orm.shape == (128, 128, 3)
