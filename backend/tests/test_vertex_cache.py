import pytest
from app.pipeline.vertex_cache_optimizer import VertexCacheOptimizer

def test_vertex_cache_acmr_calculation():
    faces = [[0, 1, 2], [1, 2, 3], [2, 3, 4]]
    acmr = VertexCacheOptimizer.compute_acmr(faces, cache_size=32)
    assert 0.0 < acmr <= 3.0

def test_vertex_cache_optimization():
    faces = [[0, 1, 2], [10, 11, 12], [1, 2, 3], [20, 21, 22], [2, 3, 4]]
    opt_faces, stats = VertexCacheOptimizer.optimize_faces(faces, vertex_count=30, cache_size=16)
    assert len(opt_faces) == len(faces)
