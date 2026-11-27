"""Unit tests for Canonical Depth Renderer & Z-Buffer Normalization."""
import pytest
import numpy as np
from app.pipeline.depth_renderer import CanonicalDepthRenderer

def test_canonical_views_matrices():
    renderer = CanonicalDepthRenderer(resolution=128)
    for view in renderer.CANONICAL_VIEWS:
        mat = renderer.get_view_matrix(view)
        assert mat.shape == (4, 4)
        assert mat[3, 3] == 1.0

def test_rasterize_depth():
    renderer = CanonicalDepthRenderer(resolution=64)
    verts = [[0.0, 0.0, 0.0], [0.5, 0.5, 0.5], [-0.5, -0.5, -0.5]]
    faces = [[0, 1, 2]]
    dmap = renderer.rasterize_depth(verts, faces, "front")
    assert dmap.shape == (64, 64)
    assert np.min(dmap) >= 0.0
    assert np.max(dmap) <= 1.0

def test_render_all_canonical_views():
    renderer = CanonicalDepthRenderer(resolution=64)
    verts = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    faces = [[0, 1, 2]]
    maps = renderer.render_all_canonical_views(verts, faces)
    assert len(maps) == 6
    assert "front" in maps and "top" in maps
