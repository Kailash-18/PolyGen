"""Unit tests for MidProjectGeometryAuditor and RenderingValidator."""
import pytest
from app.pipeline.geometry_audit import MidProjectGeometryAuditor
from app.pipeline.rendering_validator import RenderingValidator

def test_geometry_audit_pass():
    auditor = MidProjectGeometryAuditor()
    # 12 faces cube vertices
    verts = [
        [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],
        [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]
    ]
    faces = [
        [0, 1, 2], [0, 2, 3], [4, 5, 6], [4, 6, 7],
        [0, 1, 5], [0, 5, 4], [2, 3, 7], [2, 7, 6],
        [1, 2, 6], [1, 6, 5], [0, 3, 7], [0, 7, 4]
    ]
    res = auditor.audit_geometry(verts, faces)
    assert res["status"] == "PASS"
    assert res["non_blob_fidelity"] is True

def test_rendering_validator():
    validator = RenderingValidator()
    res = validator.validate_rendering_pipeline(
        mesh_id="test_model",
        uvs_count=24,
        texture_manifest={"albedo": True, "normal": True, "roughness": True}
    )
    assert res["status"] == "PASS"
    assert res["webgl_ready"] is True
