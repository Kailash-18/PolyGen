import pytest
from app.pipeline.draco_compression import DracoGeometryCompressor, DracoMeshQuantizer, DracoStreamEncoder

def test_quantizer_roundtrip():
    quantizer = DracoMeshQuantizer(position_bits=14)
    vertices = [[0.0, 0.0, 0.0], [1.0, 2.0, 3.0], [-1.0, 0.5, 2.5]]
    quantized, meta = quantizer.quantize_positions(vertices)
    assert len(quantized) == 3
    reconstructed = quantizer.dequantize_positions(quantized, meta)
    for orig, rec in zip(vertices, reconstructed):
        for o, r in zip(orig, rec):
            assert abs(o - r) < 0.01

def test_stream_encoder_delta():
    vals = [100, 105, 104, 110, 125]
    deltas = DracoStreamEncoder.delta_encode(vals)
    assert deltas == [100, 5, -1, 6, 15]
    assert DracoStreamEncoder.delta_decode(deltas) == vals

def test_draco_compressor_mesh():
    compressor = DracoGeometryCompressor(position_bits=14, normal_bits=10)
    vertices = [[-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]]
    faces = [[0, 1, 2], [0, 2, 3], [4, 5, 6], [4, 6, 7], [0, 4, 7], [0, 7, 3], [1, 5, 6], [1, 6, 2], [3, 2, 6], [3, 6, 7], [0, 1, 5], [0, 5, 4]]
    res = compressor.compress(vertices, faces)
    assert res["vertex_count"] == 8
    assert res["compression_ratio"] < 1.0
