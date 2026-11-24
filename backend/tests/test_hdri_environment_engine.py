"""
Unit tests for HDRIEnvironmentEngine and PMREM mip-chain generation.
"""

import numpy as np
from app.pipeline.hdri_environment_engine import HDRIEnvironmentEngine

def test_cartesian_to_equirectangular_uv():
    engine = HDRIEnvironmentEngine()
    # Looking down +Z -> u=0.75, v=0.5
    u, v = engine.cartesian_to_equirectangular_uv(np.array([0.0, 0.0, 1.0]))
    assert 0.0 <= u <= 1.0
    assert 0.0 <= v <= 1.0

    # Looking straight up +Y -> v=1.0
    u_up, v_up = engine.cartesian_to_equirectangular_uv(np.array([0.0, 1.0, 0.0]))
    assert np.isclose(v_up, 1.0, atol=1e-3)

def test_generate_cubemap_face_directions():
    engine = HDRIEnvironmentEngine(cubemap_resolution=16)
    dirs = engine.generate_cubemap_face_directions(face_index=0)
    assert dirs.shape == (16, 16, 3)
    # Check unit vectors
    norms = np.linalg.norm(dirs, axis=2)
    assert np.allclose(norms, 1.0, atol=1e-5)

def test_pmrem_mip_levels():
    engine = HDRIEnvironmentEngine(mip_levels=6)
    mips = engine.compute_pmrem_mip_levels()
    assert len(mips) == 6
    assert mips[0]["roughness"] == 0.0
    assert mips[5]["roughness"] == 1.0
