"""
Unit tests for Tonemapper curves and bloom thresholding.
"""

import numpy as np
from app.pipeline.tonemapper import Tonemapper

def test_aces_filmic_curve():
    tm = Tonemapper(exposure=1.0)
    hdr_color = np.array([0.5, 2.0, 10.0])  # Overbright pixel
    sdr_color = tm.apply_aces_filmic(hdr_color)
    assert sdr_color.shape == (3,)
    assert np.all(sdr_color >= 0.0)
    assert np.all(sdr_color <= 1.0)
    # Higher input yields higher output but strictly bounded
    assert sdr_color[0] < sdr_color[1] < sdr_color[2]

def test_reinhard_and_agx():
    tm = Tonemapper(exposure=1.2)
    val = np.array([1.5, 3.0, 6.0])
    r_val = tm.apply_reinhard(val)
    agx_val = tm.apply_agx(val)
    assert np.all(r_val < 1.0)
    assert np.all(agx_val <= 1.0)

def test_bloom_mask_extraction():
    tm = Tonemapper(bloom_threshold=1.0)
    img = np.zeros((4, 4, 3), dtype=np.float32)
    img[0, 0] = [2.0, 2.0, 2.0]  # Super bright pixel
    img[1, 1] = [0.5, 0.5, 0.5]  # Normal pixel
    mask = tm.extract_bloom_mask(img)
    assert np.all(mask[0, 0] > 0.0)
    assert np.all(mask[1, 1] == 0.0)
