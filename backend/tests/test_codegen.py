"""
Unit tests for PolyGen Procedural Three.js Code & Shader Generator
"""
from app.pipeline.codegen import (
    generate_chamfered_cylinder_code,
    generate_tapered_blade_code,
    generate_hollow_shell_code,
    generate_pbr_material_code,
    generate_standalone_viewer_bundle
)

def test_generate_chamfered_cylinder_code():
    code = generate_chamfered_cylinder_code(2.5, 2.5, 12.0)
    assert "CylinderGeometry" in code
    assert "createChamferedCylinder" in code

def test_generate_tapered_blade_code():
    code = generate_tapered_blade_code(30.0, 4.0, 1.0)
    assert "BufferGeometry" in code
    assert "createTaperedBlade" in code
    assert "computeVertexNormals" in code

def test_generate_pbr_material_code():
    code = generate_pbr_material_code("titanium", "#8899aa", 0.15, 0.9, 0.5)
    assert "MeshPhysicalMaterial" in code
    assert "createPBRMaterial_titanium" in code

def test_generate_standalone_viewer_bundle():
    html = generate_standalone_viewer_bundle("drone_v1", "Apex Racing Drone")
    assert "<!DOCTYPE html>" in html
    assert "three.min.js" in html
    assert "OrbitControls" in html
    assert "explodeSlider" in html
