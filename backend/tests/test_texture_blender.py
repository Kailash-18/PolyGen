"""Unit tests for MultiViewTextureBlender and TextureInpainter."""
import pytest
import numpy as np
from app.pipeline.texture_blender import MultiViewTextureBlender
from app.pipeline.texture_inpaint import TextureInpainter

def test_vertex_color_blending():
    blender = MultiViewTextureBlender()
    c1 = np.array([255, 0, 0], dtype=np.uint8)
    c2 = np.array([0, 255, 0], dtype=np.uint8)
    blended = blender.blend_vertex_colors([c1, c2], [1.0, 1.0])
    assert blended.shape == (3,)
    assert blended[0] > 0 and blended[1] > 0

def test_texture_inpaint():
    inpainter = TextureInpainter()
    tex = np.zeros((32, 32, 3), dtype=np.uint8)
    mask = np.zeros((32, 32), dtype=bool)
    tex[0:16, 0:16] = [200, 100, 50]
    mask[0:16, 0:16] = True
    result = inpainter.inpaint_unobserved_regions(tex, mask)
    assert np.all(result[20, 20] > 0)
