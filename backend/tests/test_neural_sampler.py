"""
Unit tests for TripoSR Neural Latent Sampler and Voxel Pruning.
"""
import pytest
import numpy as np
from app.pipeline.neural_sampler import NeuralLatentSampler

def test_sampler_initialization():
    sampler = NeuralLatentSampler(resolution=32, feature_dim=16)
    assert sampler.resolution == 32
    assert sampler.feature_dim == 16
    assert 'xy' in sampler.planes
    assert sampler.planes['xy'].shape == (16, 32, 32)

def test_sample_point_and_density():
    sampler = NeuralLatentSampler(resolution=32, feature_dim=16)
    feat = sampler.sample_point(0.0, 0.0, 0.0)
    assert feat.shape == (16,)
    
    density_center = sampler.evaluate_density(0.0, 0.0, 0.0)
    density_edge = sampler.evaluate_density(1.5, 1.5, 1.5)
    assert density_center > density_edge

def test_prune_empty_voxels():
    sampler = NeuralLatentSampler(resolution=16, feature_dim=8)
    active = sampler.prune_empty_voxels(threshold=0.0)
    assert isinstance(active, list)
    assert len(active) > 0
