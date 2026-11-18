import pytest
import trimesh
from app.pipeline.physics_rigidbody import MeshPhysicsEvaluator

def test_cube_rigidbody():
    box = trimesh.creation.box(extents=(2.0, 2.0, 2.0))
    props = MeshPhysicsEvaluator.evaluate_mesh(box.vertices.tolist(), box.faces.tolist(), material_density_kg_m3=1000.0)
    assert props.mass_kg > 0
    assert abs(props.volume_m3 - 8.0) < 0.2
    assert props.is_stable is True
