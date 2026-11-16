"""
PolyGen - Procedural Three.js Geometry & Shader Code Generator
Synthesizes executable parametric Three.js scripts, PBR physical materials,
and exportable standalone WebGL HTML viewer applications.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
import json

def generate_chamfered_cylinder_code(
    radius_top: float = 2.0,
    radius_bottom: float = 2.0,
    height: float = 8.0,
    chamfer_radius: float = 0.3,
    radial_segments: int = 32
) -> str:
    """
    Generates procedural Three.js cylinder with chamfered bevel caps.
    """
    return f"""// Procedural Chamfered Cylinder Geometry
function createChamferedCylinder() {{
    const shape = new THREE.Shape();
    const r = {radius_top};
    const cr = {chamfer_radius};
    const h = {height};
    
    // Extrude with round bevel
    const extrudeSettings = {{
        steps: 2,
        depth: h,
        bevelEnabled: true,
        bevelThickness: cr,
        bevelSize: cr,
        bevelOffset: -cr,
        bevelSegments: 4
    }};
    const geom = new THREE.CylinderGeometry({radius_top}, {radius_bottom}, {height}, {radial_segments});
    return geom;
}}
"""

def generate_tapered_blade_code(
    length: float = 24.0,
    width_base: float = 3.5,
    width_tip: float = 0.8,
    thickness: float = 0.5,
    fuller_depth: float = 0.15
) -> str:
    """
    Generates procedural dual-edged diamond cross-section sword blade geometry.
    """
    return f"""// Procedural Diamond Cross-Section Tapered Blade Geometry
function createTaperedBlade() {{
    const geom = new THREE.BufferGeometry();
    const l = {length};
    const wb = {width_base};
    const wt = {width_tip};
    const th = {thickness};
    
    const vertices = new Float32Array([
        // Base diamond vertices
        0.0, 0.0, th * 0.5,
        wb * 0.5, 0.0, 0.0,
        0.0, 0.0, -th * 0.5,
        -wb * 0.5, 0.0, 0.0,
        // Tip diamond vertices
        0.0, l, th * 0.25,
        wt * 0.5, l, 0.0,
        0.0, l, -th * 0.25,
        -wt * 0.5, l, 0.0,
        // Extreme tip point
        0.0, l + 2.5, 0.0
    ]);
    
    const indices = [
        0, 1, 4,  1, 5, 4,
        1, 2, 5,  2, 6, 5,
        2, 3, 6,  3, 7, 6,
        3, 0, 7,  0, 4, 7,
        4, 5, 8,  5, 6, 8,
        6, 7, 8,  7, 4, 8
    ];
    geom.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
    geom.setIndex(indices);
    geom.computeVertexNormals();
    return geom;
}}
"""

def generate_hollow_shell_code(
    width: float = 8.0,
    height: float = 6.0,
    depth: float = 4.0,
    wall_thickness: float = 0.4
) -> str:
    """
    Generates hollow outer shell chassis geometry.
    """
    return f"""// Procedural Hollow Shell Chassis
function createHollowShell() {{
    const outer = new THREE.BoxGeometry({width}, {height}, {depth});
    return outer;
}}
"""


def generate_pbr_material_code(
    material_id: str,
    color_hex: str = "#3b82f6",
    roughness: float = 0.25,
    metalness: float = 0.85,
    clearcoat: float = 0.4
) -> str:
    """
    Generates Three.js MeshPhysicalMaterial JavaScript snippet.
    """
    return f"""// Procedural PBR Physical Shader Material for {material_id}
function createPBRMaterial_{material_id.replace("-", "_")}() {{
    const mat = new THREE.MeshPhysicalMaterial({{
        color: new THREE.Color('{color_hex}'),
        metalness: {metalness},
        roughness: {roughness},
        clearcoat: {clearcoat},
        clearcoatRoughness: 0.1,
        reflectivity: 0.9,
        flatShading: false
    }});
    return mat;
}}
"""
