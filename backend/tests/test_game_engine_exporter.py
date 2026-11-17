"""
Unit Tests for Game Engine Asset Exporters (Unreal Engine 5 & Unity)
"""

import pytest
import zipfile
import trimesh
from PIL import Image
from pathlib import Path
from app.pipeline.game_engine_exporter import UnrealEngineExporter, UnityPrefabExporter


@pytest.fixture
def sample_mesh():
    return trimesh.creation.icosphere(subdivisions=2, radius=1.0)


@pytest.fixture
def sample_maps():
    return {
        "albedo": Image.new("RGB", (64, 64), color=(200, 150, 100)),
        "normal": Image.new("RGB", (64, 64), color=(128, 128, 255)),
        "roughness": Image.new("L", (64, 64), color=120),
        "metalness": Image.new("L", (64, 64), color=210)
    }


def test_unreal_package_creation(tmp_path, sample_mesh, sample_maps):
    res = UnrealEngineExporter.create_package(
        mesh=sample_mesh,
        asset_name="CyberKatana",
        output_dir=tmp_path,
        pbr_maps=sample_maps,
        generate_lods=True,
        generate_collision=True
    )

    zip_file = Path(res["package_path"])
    assert zip_file.exists()

    with zipfile.ZipFile(zip_file, "r") as zf:
        namelist = zf.namelist()
        assert any("SM_CyberKatana.glb" in n for n in namelist)
        assert any("UCX_CyberKatana_01.obj" in n for n in namelist)
        assert any("T_CyberKatana_D.png" in n for n in namelist)
        assert any("UnrealAssetManifest.json" in n for n in namelist)


def test_unity_package_creation(tmp_path, sample_mesh, sample_maps):
    res = UnityPrefabExporter.create_package(
        mesh=sample_mesh,
        asset_name="AegisShield",
        output_dir=tmp_path,
        pbr_maps=sample_maps,
        generate_lods=True
    )

    zip_file = Path(res["package_path"])
    assert zip_file.exists()

    with zipfile.ZipFile(zip_file, "r") as zf:
        namelist = zf.namelist()
        assert any("AegisShield.glb" in n for n in namelist)
        assert any("AegisShield_Albedo.png" in n for n in namelist)
        assert any("AegisShield_MetallicSmoothness.png" in n for n in namelist)
        assert any("UnityPackageManifest.json" in n for n in namelist)


def test_unity_metallic_smoothness_packing(sample_maps):
    packed = UnityPrefabExporter.pack_metallic_smoothness(
        roughness_img=sample_maps["roughness"],
        metalness_img=sample_maps["metalness"],
        resolution=32
    )

    assert packed.mode == "RGBA"
    assert packed.size == (32, 32)
