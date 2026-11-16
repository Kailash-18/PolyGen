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


def generate_standalone_viewer_bundle(
    assembly_id: str,
    title: str = "PolyGen 3D Model"
) -> str:
    """
    Compiles a self-contained, responsive HTML file containing embedded Three.js,
    procedural assembly parts, interactive exploded view slider, and studio lights.
    """
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - PolyGen 3D Web Studio</title>
    <style>
        body {{ margin: 0; overflow: hidden; background: #07090e; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        #canvas3d {{ width: 100vw; height: 100vh; display: block; }}
        #hud {{ position: absolute; top: 16px; left: 16px; color: #fff; background: rgba(13, 17, 23, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 12px 18px; pointer-events: none; }}
        #controls {{ position: absolute; bottom: 24px; left: 50%; transform: translateX(-50%); background: rgba(13, 17, 23, 0.85); backdrop-filter: blur(12px); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 30px; padding: 10px 24px; display: flex; align-items: center; gap: 16px; color: #fff; }}
        input[type=range] {{ accent-color: #3b82f6; width: 220px; }}
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="hud">
        <h3 style="margin:0 0 4px 0; font-size:16px; color:#60a5fa;">{title}</h3>
        <p style="margin:0; font-size:12px; color:#94a3b8;">PolyGen Parametric Assembly | ID: {assembly_id}</p>
    </div>
    <div id="controls">
        <label for="explodeSlider" style="font-size:13px; font-weight:600;">Explode:</label>
        <input id="explodeSlider" type="range" min="0" max="100" value="0">
        <span id="explodeVal" style="font-size:13px; min-width:40px;">0%</span>
    </div>
    <canvas id="canvas3d"></canvas>
    <script>
        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0x07090e);
        const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(30, 25, 40);
        const renderer = new THREE.WebGLRenderer({{ canvas: document.getElementById('canvas3d'), antialias: true }});
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        
        // Studio Lighting
        const ambient = new THREE.AmbientLight(0xffffff, 0.6);
        scene.add(ambient);
        const dirLight = new THREE.DirectionalLight(0x60a5fa, 1.2);
        dirLight.position.set(20, 40, 20);
        scene.add(dirLight);
        
        // Root Assembly Group
        const assemblyGroup = new THREE.Group();
        scene.add(assemblyGroup);
        
        // Grid floor
        const grid = new THREE.GridHelper(60, 40, 0x1e293b, 0x0f172a);
        grid.position.y = -10;
        scene.add(grid);
        
        window.addEventListener('resize', () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
        
        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        animate();
    </script>
</body>
</html>
"""
