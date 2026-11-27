import pytest
from PIL import Image
from app.pipeline.texture import TextureEngine

@pytest.fixture
def tex_engine():
    return TextureEngine(resolution=128)

def test_pbr_maps_synthesis(tex_engine):
    maps = tex_engine.synthesize_pbr_maps("cyber broadsword")
    assert "albedo" in maps
    assert "normal" in maps
    assert "roughness" in maps
    assert "metalness" in maps

    for name, img in maps.items():
        assert isinstance(img, Image.Image)
        assert img.size == (128, 128)
