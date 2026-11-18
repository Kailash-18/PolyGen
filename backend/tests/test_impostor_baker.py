import pytest
from app.pipeline.impostor_baker import ImpostorBaker, ImpostorConfig, OctahedralProjection

def test_octahedral_projection_roundtrip():
    test_dirs = [(0.0, 1.0, 0.0), (1.0, 0.0, 0.0), (0.0, 0.0, 1.0)]
    for d in test_dirs:
        u, v = OctahedralProjection.direction_to_uv(d)
        rec_d = OctahedralProjection.uv_to_direction(u, v)
        dot = d[0] * rec_d[0] + d[1] * rec_d[1] + d[2] * rec_d[2]
        assert dot > 0.95

def test_impostor_baker_generation():
    baker = ImpostorBaker(ImpostorConfig(atlas_resolution=512, subdivisions=4))
    vertices = [[-1, -1, -1], [1, 1, 1]]
    faces = [[0, 1, 0]]
    desc = baker.bake_impostor_descriptor("test_asset", vertices, faces)
    assert desc["model_id"] == "test_asset"
    assert desc["lod_level"] == "LOD4_Impostor"
    assert desc["tile_count"] == 16
