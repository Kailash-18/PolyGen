"""
Stage 1: Geometry Generation Engine (High-Fidelity Procedural & Parametric 3D Mesh Synthesis)
Produces watertight, multi-component, game-ready 3D geometry across diverse asset classes.
Aligned with standard WebGL / Three.js Y-up coordinates.
"""

import math
import re
import hashlib
import numpy as np
import trimesh
from app.core.device import detect_compute_device

def _set_colors(mesh: trimesh.Trimesh, rgba: list[int]):
    """Applies uniform RGBA vertex colors to a mesh component."""
    mesh.visual.vertex_colors = np.tile(np.array(rgba, dtype=np.uint8), (len(mesh.vertices), 1))
    return mesh

def _match_words(prompt: str, words: list[str]) -> bool:
    """Matches words using exact word boundaries to avoid substring false positives (e.g. 'rod' in 'aerodynamic')."""
    pattern = r'\b(' + '|'.join(re.escape(w) for w in words) + r')\b'
    return bool(re.search(pattern, prompt, re.IGNORECASE))

def _cylinder_y(radius: float, height: float, sections: int = 32) -> trimesh.Trimesh:
    """Creates a cylinder with height aligned along the Y-axis (upright in WebGL/Three.js)."""
    c = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    c.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
    return c

def _cone_y(radius: float, height: float, sections: int = 24) -> trimesh.Trimesh:
    """Creates an upright cone pointing along +Y with base at origin Y=0."""
    c = trimesh.creation.cone(radius=radius, height=height, sections=sections)
    c.apply_transform(trimesh.transformations.rotation_matrix(-math.pi / 2, [1, 0, 0]))
    return c

def _torus_y(major_radius: float, minor_radius: float, major_sections: int = 32, minor_sections: int = 16) -> trimesh.Trimesh:
    """Creates a horizontal ring in the XZ plane with its normal along the Y-axis."""
    t = trimesh.creation.torus(major_radius=major_radius, minor_radius=minor_radius,
                               major_sections=major_sections, minor_sections=minor_sections)
    t.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
    return t

def _cylinder_z(radius: float, height: float, sections: int = 24) -> trimesh.Trimesh:
    """Creates a cylinder aligned with Z axis (e.g. for fuselage or gun barrels)."""
    return trimesh.creation.cylinder(radius=radius, height=height, sections=sections)

def _cylinder_x(radius: float, height: float, sections: int = 24) -> trimesh.Trimesh:
    """Creates a cylinder aligned with X axis."""
    c = trimesh.creation.cylinder(radius=radius, height=height, sections=sections)
    c.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 1, 0]))
    return c

class GeometryEngine:
    def __init__(self, device: str = "auto", enable_neural: bool = False):
        self.device_info = detect_compute_device(device)
        self.device = self.device_info["device"]
        self.enable_neural = enable_neural

    # -------------------------------------------------------------------------
    # VEHICLES & MACHINES (Y-up: X=width, Y=height, Z=length)
    # -------------------------------------------------------------------------
    def _create_sports_car(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        p = prompt.lower()
        body_col = [220, 30, 45, 255]  # Racing Red
        if "black" in p or "dark" in p or "stealth" in p:
            body_col = [28, 30, 36, 255]
        elif "blue" in p or "cyan" in p or "neon" in p:
            body_col = [20, 120, 240, 255]
        elif "gold" in p or "yellow" in p:
            body_col = [235, 185, 25, 255]
        elif "white" in p or "silver" in p:
            body_col = [240, 242, 248, 255]
        elif "green" in p:
            body_col = [30, 180, 80, 255]

        # Wheel rim glow color (for neon rims)
        rim_glow_col = [0, 230, 255, 255] if ("neon" in p or "cyber" in p or "glow" in p) else [218, 175, 55, 255]

        # 1. Lower Chassis (Sleek wedge profile)
        chassis = trimesh.creation.box(extents=[1.3, 0.28, 2.7])
        chassis.apply_translation([0, 0.32, 0])
        _set_colors(chassis, body_col)
        parts.append(chassis)

        # 2. Front Hood (Slanted forward)
        hood = trimesh.creation.box(extents=[1.2, 0.16, 0.95])
        hood.apply_translation([0, 0.38, 0.85])
        _set_colors(hood, body_col)
        parts.append(hood)

        # 3. Cockpit Greenhouse Cabin (Curved roof with tinted glass)
        cabin = trimesh.creation.box(extents=[1.05, 0.38, 1.25])
        cabin.apply_translation([0, 0.62, -0.15])
        _set_colors(cabin, [20, 25, 35, 255])
        parts.append(cabin)

        # Windshield bevel wedge
        windshield = trimesh.creation.box(extents=[1.02, 0.28, 0.45])
        windshield.apply_transform(trimesh.transformations.rotation_matrix(0.55, [1, 0, 0]))
        windshield.apply_translation([0, 0.58, 0.48])
        _set_colors(windshield, [25, 35, 50, 255])
        parts.append(windshield)

        # 4. Front Splitter / Air Dam
        splitter = trimesh.creation.box(extents=[1.34, 0.06, 0.35])
        splitter.apply_translation([0, 0.18, 1.35])
        _set_colors(splitter, [20, 22, 26, 255])
        parts.append(splitter)

        # 5. Rear Diffuser
        diffuser = trimesh.creation.box(extents=[1.25, 0.12, 0.28])
        diffuser.apply_translation([0, 0.22, -1.35])
        _set_colors(diffuser, [20, 22, 26, 255])
        parts.append(diffuser)

        # 6. Rear Wing / Aerodynamic Spoiler
        spoiler_blade = trimesh.creation.box(extents=[1.42, 0.05, 0.32])
        spoiler_blade.apply_translation([0, 0.82, -1.25])
        _set_colors(spoiler_blade, [20, 22, 26, 255])
        parts.append(spoiler_blade)

        for sx in [-0.5, 0.5]:
            strut = trimesh.creation.box(extents=[0.05, 0.32, 0.1])
            strut.apply_translation([sx, 0.66, -1.25])
            _set_colors(strut, [20, 22, 26, 255])
            parts.append(strut)

        # 7. Dual Chrome Exhaust Pipes
        for ex in [-0.22, 0.22]:
            pipe = trimesh.creation.cylinder(radius=0.055, height=0.25, sections=16)
            pipe.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
            pipe.apply_translation([ex, 0.24, -1.45])
            _set_colors(pipe, [210, 215, 225, 255])
            parts.append(pipe)

        # 8. LED Headlights & Taillights
        for hx in [-0.48, 0.48]:
            headlight = trimesh.creation.box(extents=[0.24, 0.07, 0.08])
            headlight.apply_translation([hx, 0.38, 1.32])
            _set_colors(headlight, [220, 245, 255, 255])
            parts.append(headlight)

            taillight = trimesh.creation.box(extents=[0.28, 0.06, 0.08])
            taillight.apply_translation([hx, 0.42, -1.36])
            _set_colors(taillight, [240, 25, 35, 255])
            parts.append(taillight)

        # 9. 4 Detailed Wheels (Tires + Rims + Glowing Neon Rings)
        wheel_positions = [
            [-0.72, 0.28, 0.82],
            [0.72, 0.28, 0.82],
            [-0.72, 0.28, -0.82],
            [0.72, 0.28, -0.82]
        ]
        for wx, wy, wz in wheel_positions:
            # Tire
            tire = trimesh.creation.cylinder(radius=0.28, height=0.24, sections=24)
            tire.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 0, 1]))
            tire.apply_translation([wx, wy, wz])
            _set_colors(tire, [30, 32, 38, 255])
            parts.append(tire)

            # Rim
            rim = trimesh.creation.cylinder(radius=0.19, height=0.25, sections=16)
            rim.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 0, 1]))
            rim.apply_translation([wx, wy, wz])
            _set_colors(rim, [195, 200, 210, 255])
            parts.append(rim)

            # Glowing Rim Ring
            neon_ring = trimesh.creation.torus(major_radius=0.19, minor_radius=0.02, major_sections=24, minor_sections=12)
            neon_ring.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 1, 0]))
            neon_ring.apply_translation([wx + (0.13 if wx > 0 else -0.13), wy, wz])
            _set_colors(neon_ring, rim_glow_col)
            parts.append(neon_ring)

        return trimesh.util.concatenate(parts)

    def _create_spaceship(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        p = prompt.lower()
        hull_col = [225, 230, 240, 255]
        accent_col = [230, 45, 30, 255] if "red" in p else [0, 180, 255, 255]

        # Central fuselage
        fuselage = trimesh.creation.box(extents=[0.65, 0.42, 2.8])
        fuselage.apply_translation([0, 0.45, 0])
        _set_colors(fuselage, hull_col)
        parts.append(fuselage)

        # Cockpit canopy
        canopy = trimesh.creation.icosphere(subdivisions=2, radius=0.28)
        canopy.apply_scale([0.8, 0.65, 1.8])
        canopy.apply_translation([0, 0.72, 0.35])
        _set_colors(canopy, [35, 45, 65, 255])
        parts.append(canopy)

        # Nose cone
        nose = trimesh.creation.cone(radius=0.32, height=0.9, sections=20)
        nose.apply_transform(trimesh.transformations.rotation_matrix(-math.pi / 2, [1, 0, 0]))
        nose.apply_translation([0, 0.45, 1.85])
        _set_colors(nose, accent_col)
        parts.append(nose)

        # Swept delta wings
        for sx in [-1, 1]:
            wing = trimesh.creation.box(extents=[1.35, 0.06, 1.5])
            wing.apply_transform(trimesh.transformations.rotation_matrix(sx * 0.18, [0, 1, 0]))
            wing.apply_translation([sx * 1.05, 0.42, -0.35])
            _set_colors(wing, hull_col)
            parts.append(wing)

            # Wingtip stabilizer fin
            fin = trimesh.creation.box(extents=[0.05, 0.45, 0.65])
            fin.apply_translation([sx * 1.7, 0.62, -0.4])
            _set_colors(fin, accent_col)
            parts.append(fin)

            # Laser cannon
            cannon = trimesh.creation.cylinder(radius=0.045, height=0.9, sections=16)
            cannon.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
            cannon.apply_translation([sx * 1.35, 0.35, 0.15])
            _set_colors(cannon, [55, 60, 70, 255])
            parts.append(cannon)

        # Twin Plasma Thrusters
        for ex in [-0.28, 0.28]:
            engine = trimesh.creation.cylinder(radius=0.18, height=1.2, sections=24)
            engine.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
            engine.apply_translation([ex, 0.45, -1.45])
            _set_colors(engine, [45, 50, 60, 255])
            parts.append(engine)

            plasma = trimesh.creation.cylinder(radius=0.15, height=0.2, sections=24)
            plasma.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
            plasma.apply_translation([ex, 0.45, -2.1])
            _set_colors(plasma, [0, 240, 255, 255])
            parts.append(plasma)

        return trimesh.util.concatenate(parts)

    def _create_drone(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        body = trimesh.creation.icosphere(subdivisions=2, radius=0.45)
        body.apply_scale([1.0, 0.45, 1.2])
        body.apply_translation([0, 0.55, 0])
        _set_colors(body, [32, 35, 42, 255])
        parts.append(body)

        cam = trimesh.creation.icosphere(subdivisions=2, radius=0.18)
        cam.apply_translation([0, 0.35, 0.42])
        _set_colors(cam, [0, 210, 255, 255])
        parts.append(cam)

        arm_angles = [math.pi / 4, 3 * math.pi / 4, 5 * math.pi / 4, 7 * math.pi / 4]
        for angle in arm_angles:
            dist = 1.15
            ax = dist * math.cos(angle)
            az = dist * math.sin(angle)

            arm = trimesh.creation.cylinder(radius=0.04, height=dist, sections=16)
            arm.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 0, 1]))
            arm.apply_transform(trimesh.transformations.rotation_matrix(angle, [0, 1, 0]))
            arm.apply_translation([ax / 2, 0.55, az / 2])
            _set_colors(arm, [45, 48, 55, 255])
            parts.append(arm)

            motor = _cylinder_y(radius=0.12, height=0.18, sections=20)
            motor.apply_translation([ax, 0.64, az])
            _set_colors(motor, [212, 175, 55, 255])
            parts.append(motor)

            blade = _cylinder_y(radius=0.55, height=0.015, sections=32)
            blade.apply_translation([ax, 0.75, az])
            _set_colors(blade, [180, 195, 210, 200])
            parts.append(blade)

        for lx in [-0.42, 0.42]:
            skid = trimesh.creation.cylinder(radius=0.03, height=1.35, sections=16)
            skid.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
            skid.apply_translation([lx, 0.12, 0])
            _set_colors(skid, [25, 28, 35, 255])
            parts.append(skid)

        return trimesh.util.concatenate(parts)

    def _create_mech(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        armor_col = [45, 50, 62, 255]
        glow_col = [0, 230, 255, 255]

        torso = trimesh.creation.box(extents=[1.15, 0.95, 0.85])
        torso.apply_translation([0, 1.45, 0])
        _set_colors(torso, armor_col)
        parts.append(torso)

        visor = trimesh.creation.box(extents=[0.58, 0.2, 0.15])
        visor.apply_translation([0, 1.62, 0.44])
        _set_colors(visor, glow_col)
        parts.append(visor)

        for sx in [-0.78, 0.78]:
            pod = trimesh.creation.box(extents=[0.38, 0.45, 0.65])
            pod.apply_translation([sx, 1.82, 0])
            _set_colors(pod, [65, 72, 85, 255])
            parts.append(pod)

            arm = _cylinder_y(radius=0.1, height=0.75, sections=16)
            arm.apply_translation([sx, 1.15, 0.15])
            _set_colors(arm, [35, 38, 48, 255])
            parts.append(arm)

            gun = trimesh.creation.cylinder(radius=0.08, height=0.95, sections=16)
            gun.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
            gun.apply_translation([sx, 0.85, 0.65])
            _set_colors(gun, [145, 150, 160, 255])
            parts.append(gun)

        pelvis = trimesh.creation.box(extents=[0.8, 0.35, 0.55])
        pelvis.apply_translation([0, 0.9, 0])
        _set_colors(pelvis, [30, 32, 40, 255])
        parts.append(pelvis)

        for lx in [-0.42, 0.42]:
            leg = _cylinder_y(radius=0.11, height=0.75, sections=16)
            leg.apply_translation([lx, 0.45, 0])
            _set_colors(leg, armor_col)
            parts.append(leg)

            foot = trimesh.creation.box(extents=[0.35, 0.15, 0.6])
            foot.apply_translation([lx, 0.08, 0.1])
            _set_colors(foot, armor_col)
            parts.append(foot)

        return trimesh.util.concatenate(parts)

    # -------------------------------------------------------------------------
    # WEAPONS & PROPS (Upright Y-axis)
    # -------------------------------------------------------------------------
    def _create_sword(self, prompt: str = "") -> trimesh.Trimesh:
        is_katana = _match_words(prompt, ["katana", "samurai"])
        parts = []

        if is_katana:
            n_segments = 14
            for i in range(n_segments):
                t = i / n_segments
                seg = trimesh.creation.box(extents=[0.08, 0.22, 0.025])
                curve = 0.08 * math.sin(t * math.pi * 0.7)
                seg.apply_translation([curve, 0.45 + i * 0.20, 0])
                _set_colors(seg, [230, 235, 245, 255])
                parts.append(seg)

            habaki = trimesh.creation.box(extents=[0.11, 0.08, 0.04])
            habaki.apply_translation([0, 0.42, 0])
            _set_colors(habaki, [218, 165, 32, 255])
            parts.append(habaki)

            tsuba = _cylinder_y(radius=0.28, height=0.04, sections=32)
            tsuba.apply_translation([0, 0.38, 0])
            _set_colors(tsuba, [35, 38, 45, 255])
            parts.append(tsuba)

            handle = _cylinder_y(radius=0.045, height=0.75, sections=24)
            handle.apply_translation([0, -0.02, 0])
            _set_colors(handle, [180, 40, 35, 255])
            parts.append(handle)

            pommel = _cylinder_y(radius=0.05, height=0.06, sections=24)
            pommel.apply_translation([0, -0.42, 0])
            _set_colors(pommel, [218, 165, 32, 255])
            parts.append(pommel)
        else:
            blade = trimesh.creation.box(extents=[0.18, 2.5, 0.04])
            blade.apply_translation([0, 1.45, 0])
            _set_colors(blade, [222, 228, 238, 255])
            parts.append(blade)

            tip = _cone_y(radius=0.09, height=0.55, sections=20)
            tip.apply_translation([0, 2.7, 0])
            _set_colors(tip, [232, 238, 248, 255])
            parts.append(tip)

            guard = trimesh.creation.box(extents=[0.85, 0.1, 0.12])
            guard.apply_translation([0, 0.2, 0])
            _set_colors(guard, [212, 175, 55, 255])
            parts.append(guard)

            for fx in [-0.42, 0.42]:
                f = trimesh.creation.icosphere(subdivisions=2, radius=0.075)
                f.apply_translation([fx, 0.2, 0])
                _set_colors(f, [212, 175, 55, 255])
                parts.append(f)

            handle = _cylinder_y(radius=0.046, height=0.75, sections=24)
            handle.apply_translation([0, -0.22, 0])
            _set_colors(handle, [75, 45, 30, 255])
            parts.append(handle)

            for ry in [-0.05, -0.22, -0.38]:
                ring = _torus_y(major_radius=0.052, minor_radius=0.012, major_sections=24, minor_sections=12)
                ring.apply_translation([0, ry, 0])
                _set_colors(ring, [212, 175, 55, 255])
                parts.append(ring)

            pommel = trimesh.creation.icosphere(subdivisions=2, radius=0.11)
            pommel.apply_translation([0, -0.65, 0])
            _set_colors(pommel, [212, 175, 55, 255])
            parts.append(pommel)

            gem_col = [0, 160, 255, 255] if _match_words(prompt, ["sapphire", "blue"]) else [230, 30, 60, 255]
            gem = trimesh.creation.icosphere(subdivisions=2, radius=0.065)
            gem.apply_translation([0, 0.2, 0.06])
            _set_colors(gem, gem_col)
            parts.append(gem)

        return trimesh.util.concatenate(parts)

    def _create_axe(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        haft = _cylinder_y(radius=0.055, height=2.4, sections=24)
        haft.apply_translation([0, 1.2, 0])
        _set_colors(haft, [110, 70, 45, 255])
        parts.append(haft)

        head_core = trimesh.creation.box(extents=[0.35, 0.3, 0.16])
        head_core.apply_translation([0, 2.05, 0])
        _set_colors(head_core, [160, 165, 175, 255])
        parts.append(head_core)

        blade = trimesh.creation.cylinder(radius=0.75, height=0.04, sections=36)
        blade.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 0, 1]))
        blade.apply_scale([1.2, 1.0, 0.45])
        blade.apply_translation([0.45, 2.05, 0])
        _set_colors(blade, [220, 225, 235, 255])
        parts.append(blade)

        top_spike = _cone_y(radius=0.065, height=0.4, sections=16)
        top_spike.apply_translation([0, 2.4, 0])
        _set_colors(top_spike, [210, 215, 225, 255])
        parts.append(top_spike)

        pommel = _torus_y(major_radius=0.09, minor_radius=0.03, major_sections=24, minor_sections=12)
        pommel.apply_translation([0, 0.05, 0])
        _set_colors(pommel, [212, 175, 55, 255])
        parts.append(pommel)

        return trimesh.util.concatenate(parts)

    def _create_hammer(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        haft = _cylinder_y(radius=0.055, height=2.2, sections=24)
        haft.apply_translation([0, 1.1, 0])
        _set_colors(haft, [85, 55, 35, 255])
        parts.append(haft)

        head = trimesh.creation.box(extents=[0.7, 0.38, 0.38])
        head.apply_translation([0, 2.0, 0])
        _set_colors(head, [170, 175, 185, 255])
        parts.append(head)

        for sx in [-0.38, 0.38]:
            f1 = trimesh.creation.cylinder(radius=0.18, height=0.1, sections=24)
            f1.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 0, 1]))
            f1.apply_translation([sx, 2.0, 0])
            _set_colors(f1, [215, 220, 230, 255])
            parts.append(f1)

        cspike = _cone_y(radius=0.07, height=0.35, sections=16)
        cspike.apply_translation([0, 2.2, 0])
        _set_colors(cspike, [212, 175, 55, 255])
        parts.append(cspike)

        return trimesh.util.concatenate(parts)

    def _create_shield(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        body = trimesh.creation.cylinder(radius=1.1, height=0.08, sections=40)
        body.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
        body.apply_translation([0, 1.1, 0])
        _set_colors(body, [50, 75, 110, 255])
        parts.append(body)

        rim = trimesh.creation.torus(major_radius=1.12, minor_radius=0.06, major_sections=40, minor_sections=16)
        rim.apply_translation([0, 1.1, 0])
        _set_colors(rim, [212, 175, 55, 255])
        parts.append(rim)

        boss = trimesh.creation.icosphere(subdivisions=3, radius=0.32)
        boss.apply_translation([0, 1.1, 0.07])
        _set_colors(boss, [200, 205, 215, 255])
        parts.append(boss)

        return trimesh.util.concatenate(parts)

    def _create_gun_blaster(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        receiver = trimesh.creation.box(extents=[0.16, 0.32, 1.4])
        receiver.apply_translation([0, 0.7, 0.1])
        _set_colors(receiver, [32, 35, 42, 255])
        parts.append(receiver)

        barrel = trimesh.creation.cylinder(radius=0.065, height=1.1, sections=24)
        barrel.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
        barrel.apply_translation([0, 0.75, 1.1])
        _set_colors(barrel, [80, 85, 95, 255])
        parts.append(barrel)

        grip = trimesh.creation.box(extents=[0.14, 0.65, 0.28])
        grip.apply_transform(trimesh.transformations.rotation_matrix(0.35, [1, 0, 0]))
        grip.apply_translation([0, 0.32, -0.4])
        _set_colors(grip, [25, 26, 30, 255])
        parts.append(grip)

        scope = trimesh.creation.cylinder(radius=0.075, height=0.75, sections=24)
        scope.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [1, 0, 0]))
        scope.apply_translation([0, 1.02, 0])
        _set_colors(scope, [20, 22, 26, 255])
        parts.append(scope)

        return trimesh.util.concatenate(parts)

    def _create_staff(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        shaft = _cylinder_y(radius=0.05, height=2.8, sections=24)
        shaft.apply_translation([0, 1.4, 0])
        _set_colors(shaft, [95, 60, 40, 255])
        parts.append(shaft)

        crystal = trimesh.creation.icosphere(subdivisions=2, radius=0.2)
        crystal.apply_scale([0.8, 1.4, 0.8])
        crystal.apply_translation([0, 3.0, 0])
        _set_colors(crystal, [0, 230, 255, 255])
        parts.append(crystal)

        ring = _torus_y(major_radius=0.28, minor_radius=0.025, major_sections=32, minor_sections=12)
        ring.apply_translation([0, 3.0, 0])
        _set_colors(ring, [212, 175, 55, 255])
        parts.append(ring)

        return trimesh.util.concatenate(parts)

    def _create_chest(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        box = trimesh.creation.box(extents=[1.5, 0.75, 0.95])
        box.apply_translation([0, 0.38, 0])
        _set_colors(box, [115, 75, 45, 255])
        parts.append(box)

        lid = trimesh.creation.cylinder(radius=0.48, height=1.5, sections=32)
        lid.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 0, 1]))
        lid.apply_translation([0, 0.75, 0])
        _set_colors(lid, [115, 75, 45, 255])
        parts.append(lid)

        for bx in [-0.55, 0.0, 0.55]:
            band = trimesh.creation.box(extents=[0.1, 0.78, 0.98])
            band.apply_translation([bx, 0.38, 0])
            _set_colors(band, [212, 175, 55, 255])
            parts.append(band)

        lock = trimesh.creation.box(extents=[0.22, 0.25, 0.06])
        lock.apply_translation([0, 0.65, 0.5])
        _set_colors(lock, [212, 175, 55, 255])
        parts.append(lock)

        return trimesh.util.concatenate(parts)

    def _create_potion(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        bulb = trimesh.creation.icosphere(subdivisions=3, radius=0.75)
        bulb.apply_translation([0, 0.75, 0])
        _set_colors(bulb, [210, 235, 255, 120])
        parts.append(bulb)

        liquid = trimesh.creation.icosphere(subdivisions=3, radius=0.62)
        liquid.apply_translation([0, 0.68, 0])
        _set_colors(liquid, [230, 30, 80, 255])
        parts.append(liquid)

        neck = _cylinder_y(radius=0.22, height=0.7, sections=32)
        neck.apply_translation([0, 1.65, 0])
        _set_colors(neck, [210, 235, 255, 140])
        parts.append(neck)

        cork = _cylinder_y(radius=0.2, height=0.32, sections=24)
        cork.apply_translation([0, 2.12, 0])
        _set_colors(cork, [140, 95, 60, 255])
        parts.append(cork)

        rim = _torus_y(major_radius=0.25, minor_radius=0.04, major_sections=24, minor_sections=12)
        rim.apply_translation([0, 2.0, 0])
        _set_colors(rim, [210, 235, 255, 160])
        parts.append(rim)

        return trimesh.util.concatenate(parts)

    def _create_vase(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        terracotta_col = [205, 110, 65, 255]
        gold_accent = [218, 175, 55, 255]
        black_accent = [30, 28, 32, 255]

        # 1. Base pedestal
        base = _cylinder_y(radius=0.48, height=0.18, sections=36)
        base.apply_translation([0, 0.09, 0])
        _set_colors(base, terracotta_col)
        parts.append(base)

        base_rim = _torus_y(major_radius=0.48, minor_radius=0.05, major_sections=36, minor_sections=16)
        base_rim.apply_translation([0, 0.18, 0])
        _set_colors(base_rim, gold_accent)
        parts.append(base_rim)

        # 2. Lower tapered foot
        foot = _cylinder_y(radius=0.35, height=0.35, sections=36)
        foot.apply_translation([0, 0.35, 0])
        _set_colors(foot, terracotta_col)
        parts.append(foot)

        # 3. Amphora main belly body (curved egg shape)
        body = trimesh.creation.icosphere(subdivisions=3, radius=0.92)
        body.apply_scale([1.0, 1.25, 1.0])
        body.apply_translation([0, 1.35, 0])
        _set_colors(body, terracotta_col)
        parts.append(body)

        # Decorative Greek key / meander middle frieze band
        frieze = _cylinder_y(radius=0.93, height=0.28, sections=40)
        frieze.apply_translation([0, 1.35, 0])
        _set_colors(frieze, black_accent)
        parts.append(frieze)

        # 4. Fluted Neck
        neck = _cylinder_y(radius=0.40, height=0.75, sections=36)
        neck.apply_translation([0, 2.35, 0])
        _set_colors(neck, terracotta_col)
        parts.append(neck)

        # 5. Flared lip / lip rim
        rim = _torus_y(major_radius=0.50, minor_radius=0.08, major_sections=36, minor_sections=16)
        rim.apply_translation([0, 2.72, 0])
        _set_colors(rim, gold_accent)
        parts.append(rim)

        # 6. Symmetrical curved amphora handles
        for hx in [-0.78, 0.78]:
            handle = trimesh.creation.torus(major_radius=0.48, minor_radius=0.065, major_sections=32, minor_sections=16)
            handle.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, [0, 0, 1]))
            handle.apply_scale([0.5, 1.2, 0.5])
            handle.apply_translation([hx, 2.0, 0])
            _set_colors(handle, terracotta_col)
            parts.append(handle)

        return trimesh.util.concatenate(parts)

    def _create_crystal(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        rock = trimesh.creation.icosphere(subdivisions=2, radius=0.9)
        rock.apply_scale([1.3, 0.35, 1.3])
        rock.apply_translation([0, 0.15, 0])
        _set_colors(rock, [65, 68, 75, 255])
        parts.append(rock)

        offsets = [
            (0.0, 0.0, 1.7, 0.28),
            (0.38, 0.25, 1.3, 0.20),
            (-0.35, 0.28, 1.2, 0.18),
            (0.28, -0.32, 1.1, 0.16),
            (-0.38, -0.22, 1.25, 0.19)
        ]
        for ox, oz, h, rad in offsets:
            c = _cylinder_y(radius=rad, height=h, sections=6)
            tip = _cone_y(radius=rad, height=rad * 1.8, sections=6)
            tip.apply_translation([0, h / 2, 0])
            one_c = trimesh.util.concatenate([c, tip])
            one_c.apply_translation([ox, h / 2 + 0.15, oz])
            _set_colors(one_c, [0, 210, 255, 255])
            parts.append(one_c)

        return trimesh.util.concatenate(parts)

    def _create_chair(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        seat = trimesh.creation.box(extents=[0.95, 0.12, 0.95])
        seat.apply_translation([0, 0.85, 0])
        _set_colors(seat, [35, 38, 48, 255])
        parts.append(seat)

        back = trimesh.creation.box(extents=[0.85, 0.95, 0.08])
        back.apply_translation([0, 1.35, -0.42])
        _set_colors(back, [40, 45, 55, 255])
        parts.append(back)

        piston = _cylinder_y(radius=0.05, height=0.85, sections=20)
        piston.apply_translation([0, 0.42, 0])
        _set_colors(piston, [200, 205, 215, 255])
        parts.append(piston)

        for i in range(5):
            angle = i * (2 * math.pi / 5)
            star_leg = trimesh.creation.box(extents=[0.06, 0.06, 0.55])
            star_leg.apply_transform(trimesh.transformations.rotation_matrix(angle, [0, 1, 0]))
            rad = 0.28
            star_leg.apply_translation([rad * math.sin(angle), 0.05, rad * math.cos(angle)])
            _set_colors(star_leg, [30, 32, 38, 255])
            parts.append(star_leg)

        return trimesh.util.concatenate(parts)

    # -------------------------------------------------------------------------
    # FURNITURE, CONTAINERS, ARCHITECTURE & SCI-FI EXPANDED ARTIFACTS
    # -------------------------------------------------------------------------
    def _create_table(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        p = prompt.lower()
        wood_col = [135, 85, 45, 255]
        if "dark" in p or "black" in p or "ebony" in p:
            wood_col = [42, 35, 30, 255]
        elif "white" in p or "marble" in p:
            wood_col = [235, 235, 240, 255]
        elif "gold" in p or "golden" in p:
            wood_col = [218, 175, 45, 255]

        is_round = any(w in p for w in ["round", "circular", "circle", "oval"])
        if is_round:
            top = _cylinder_y(radius=0.92, height=0.08, sections=36)
            top.apply_translation([0, 0.96, 0])
            _set_colors(top, wood_col)
            parts.append(top)

            for i in range(4):
                ang = i * (math.pi / 2) + (math.pi / 4)
                leg = _cylinder_y(radius=0.045, height=0.92, sections=16)
                leg.apply_translation([0.62 * math.cos(ang), 0.46, 0.62 * math.sin(ang)])
                _set_colors(leg, [int(c * 0.85) for c in wood_col[:3]] + [255])
                parts.append(leg)

            brace = _torus_y(major_radius=0.58, minor_radius=0.025, major_sections=32)
            brace.apply_translation([0, 0.42, 0])
            _set_colors(brace, [int(c * 0.7) for c in wood_col[:3]] + [255])
            parts.append(brace)
        else:
            top = trimesh.creation.box(extents=[1.7, 0.08, 1.05])
            top.apply_translation([0, 0.96, 0])
            _set_colors(top, wood_col)
            parts.append(top)

            for dx in [-0.74, 0.74]:
                for dz in [-0.42, 0.42]:
                    leg = trimesh.creation.box(extents=[0.08, 0.92, 0.08])
                    leg.apply_translation([dx, 0.46, dz])
                    _set_colors(leg, [int(c * 0.85) for c in wood_col[:3]] + [255])
                    parts.append(leg)

            apron_x1 = trimesh.creation.box(extents=[1.42, 0.08, 0.03])
            apron_x1.apply_translation([0, 0.88, 0.42])
            _set_colors(apron_x1, wood_col)
            parts.append(apron_x1)

            apron_x2 = trimesh.creation.box(extents=[1.42, 0.08, 0.03])
            apron_x2.apply_translation([0, 0.88, -0.42])
            _set_colors(apron_x2, wood_col)
            parts.append(apron_x2)

            apron_z1 = trimesh.creation.box(extents=[0.03, 0.08, 0.80])
            apron_z1.apply_translation([0.74, 0.88, 0])
            _set_colors(apron_z1, wood_col)
            parts.append(apron_z1)

            apron_z2 = trimesh.creation.box(extents=[0.03, 0.08, 0.80])
            apron_z2.apply_translation([-0.74, 0.88, 0])
            _set_colors(apron_z2, wood_col)
            parts.append(apron_z2)

        return trimesh.util.concatenate(parts)

    def _create_barrel(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        p = prompt.lower()
        wood_col = [125, 78, 38, 255]
        band_col = [45, 48, 55, 255]
        if "gold" in p or "brass" in p:
            band_col = [218, 175, 45, 255]

        radii = [0.52, 0.62, 0.68, 0.62, 0.52]
        heights = [0.26, 0.28, 0.30, 0.28, 0.26]
        cur_y = 0.0
        for r, h in zip(radii, heights):
            seg = _cylinder_y(radius=r, height=h, sections=24)
            seg.apply_translation([0, cur_y + h / 2.0, 0])
            _set_colors(seg, wood_col)
            parts.append(seg)
            cur_y += h

        hoop_ys = [0.22, 0.52, 0.86, 1.16]
        hoop_radii = [0.55, 0.66, 0.66, 0.55]
        for y_pos, r in zip(hoop_ys, hoop_radii):
            hoop = _torus_y(major_radius=r, minor_radius=0.024, major_sections=28)
            hoop.apply_translation([0, y_pos, 0])
            _set_colors(hoop, band_col)
            parts.append(hoop)

        top_lid = _cylinder_y(radius=0.48, height=0.04, sections=24)
        top_lid.apply_translation([0, cur_y + 0.01, 0])
        _set_colors(top_lid, [100, 60, 30, 255])
        parts.append(top_lid)

        bung = _cylinder_x(radius=0.045, height=0.18, sections=12)
        bung.apply_translation([0.68, 0.70, 0])
        _set_colors(bung, [90, 50, 25, 255])
        parts.append(bung)

        return trimesh.util.concatenate(parts)

    def _create_mug_cup(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        p = prompt.lower()
        mug_col = [240, 240, 245, 255]
        if "black" in p or "dark" in p:
            mug_col = [30, 32, 38, 255]
        elif "gold" in p or "golden" in p:
            mug_col = [218, 175, 45, 255]
        elif "blue" in p or "cyan" in p:
            mug_col = [35, 120, 220, 255]

        body = _cylinder_y(radius=0.46, height=0.92, sections=32)
        body.apply_translation([0, 0.46, 0])
        _set_colors(body, mug_col)
        parts.append(body)

        base_rim = _cylinder_y(radius=0.48, height=0.05, sections=32)
        base_rim.apply_translation([0, 0.025, 0])
        _set_colors(base_rim, mug_col)
        parts.append(base_rim)

        lip = _torus_y(major_radius=0.46, minor_radius=0.02, major_sections=32)
        lip.apply_translation([0, 0.92, 0])
        _set_colors(lip, mug_col)
        parts.append(lip)

        liq_col = [55, 32, 18, 255] if "tea" not in p else [160, 85, 35, 255]
        liquid = _cylinder_y(radius=0.42, height=0.02, sections=32)
        liquid.apply_translation([0, 0.85, 0])
        _set_colors(liquid, liq_col)
        parts.append(liquid)

        h_top = trimesh.creation.box(extents=[0.24, 0.06, 0.07])
        h_top.apply_translation([0.56, 0.72, 0])
        _set_colors(h_top, mug_col)
        parts.append(h_top)

        h_side = trimesh.creation.box(extents=[0.06, 0.44, 0.07])
        h_side.apply_translation([0.67, 0.50, 0])
        _set_colors(h_side, mug_col)
        parts.append(h_side)

        h_bot = trimesh.creation.box(extents=[0.24, 0.06, 0.07])
        h_bot.apply_translation([0.56, 0.28, 0])
        _set_colors(h_bot, mug_col)
        parts.append(h_bot)

        return trimesh.util.concatenate(parts)

    def _create_helmet(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        p = prompt.lower()
        steel_col = [180, 190, 202, 255]
        visor_col = [0, 215, 255, 255] if ("cyber" in p or "scifi" in p or "neon" in p) else [25, 28, 35, 255]

        dome = trimesh.creation.icosphere(subdivisions=3, radius=0.68)
        dome.vertices[:, 1] *= 1.15
        dome.vertices[:, 2] *= 1.08
        dome.apply_translation([0, 1.0, 0])
        _set_colors(dome, steel_col)
        parts.append(dome)

        jaw = trimesh.creation.box(extents=[0.92, 0.48, 0.72])
        jaw.apply_translation([0, 0.65, 0.15])
        _set_colors(jaw, steel_col)
        parts.append(jaw)

        visor = trimesh.creation.box(extents=[0.76, 0.12, 0.22])
        visor.apply_translation([0, 0.82, 0.50])
        _set_colors(visor, visor_col)
        parts.append(visor)

        collar = _cylinder_y(radius=0.58, height=0.20, sections=28)
        collar.apply_translation([0, 0.35, 0.05])
        _set_colors(collar, [int(c * 0.8) for c in steel_col[:3]] + [255])
        parts.append(collar)

        ridge = trimesh.creation.box(extents=[0.08, 0.22, 1.05])
        ridge.apply_translation([0, 1.62, -0.05])
        _set_colors(ridge, [218, 175, 45, 255])
        parts.append(ridge)

        return trimesh.util.concatenate(parts)

    def _create_tower_castle(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        stone_col = [115, 118, 125, 255]
        dark_stone = [75, 78, 85, 255]

        base = _cylinder_y(radius=1.12, height=0.32, sections=24)
        base.apply_translation([0, 0.16, 0])
        _set_colors(base, dark_stone)
        parts.append(base)

        shaft = _cylinder_y(radius=0.86, height=2.1, sections=24)
        shaft.apply_translation([0, 1.25, 0])
        _set_colors(shaft, stone_col)
        parts.append(shaft)

        corbel = _cylinder_y(radius=1.04, height=0.22, sections=24)
        corbel.apply_translation([0, 2.35, 0])
        _set_colors(corbel, dark_stone)
        parts.append(corbel)

        parapet = _cylinder_y(radius=1.02, height=0.28, sections=24)
        parapet.apply_translation([0, 2.58, 0])
        _set_colors(parapet, stone_col)
        parts.append(parapet)

        for i in range(6):
            ang = i * (2 * math.pi / 6)
            merlon = trimesh.creation.box(extents=[0.24, 0.26, 0.24])
            merlon.apply_translation([0.92 * math.cos(ang), 2.84, 0.92 * math.sin(ang)])
            _set_colors(merlon, stone_col)
            parts.append(merlon)

        door = trimesh.creation.box(extents=[0.36, 0.64, 0.14])
        door.apply_translation([0, 0.46, 0.84])
        _set_colors(door, [85, 52, 28, 255])
        parts.append(door)

        for dy in [1.1, 1.7]:
            slit = trimesh.creation.box(extents=[0.08, 0.32, 0.12])
            slit.apply_translation([0, dy, 0.84])
            _set_colors(slit, [30, 30, 35, 255])
            parts.append(slit)

        return trimesh.util.concatenate(parts)

    def _create_robot_arm(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        chassis_col = [235, 145, 20, 255]
        dark_col = [35, 38, 45, 255]
        chrome_col = [205, 210, 220, 255]

        base = _cylinder_y(radius=0.72, height=0.20, sections=32)
        base.apply_translation([0, 0.10, 0])
        _set_colors(base, dark_col)
        parts.append(base)

        shoulder = trimesh.creation.box(extents=[0.52, 0.42, 0.52])
        shoulder.apply_translation([0, 0.38, 0])
        _set_colors(shoulder, chassis_col)
        parts.append(shoulder)

        pivot1 = _cylinder_x(radius=0.18, height=0.58, sections=16)
        pivot1.apply_translation([0, 0.48, 0])
        _set_colors(pivot1, dark_col)
        parts.append(pivot1)

        lower_arm = trimesh.creation.box(extents=[0.24, 0.95, 0.28])
        lower_arm.apply_transform(trimesh.transformations.rotation_matrix(0.35, [1, 0, 0]))
        lower_arm.apply_translation([0, 0.92, -0.15])
        _set_colors(lower_arm, chassis_col)
        parts.append(lower_arm)

        piston = _cylinder_y(radius=0.045, height=0.75, sections=12)
        piston.apply_transform(trimesh.transformations.rotation_matrix(0.28, [1, 0, 0]))
        piston.apply_translation([0.16, 0.82, -0.05])
        _set_colors(piston, chrome_col)
        parts.append(piston)

        forearm = trimesh.creation.box(extents=[0.20, 0.85, 0.24])
        forearm.apply_transform(trimesh.transformations.rotation_matrix(-0.55, [1, 0, 0]))
        forearm.apply_translation([0, 1.48, 0.25])
        _set_colors(forearm, dark_col)
        parts.append(forearm)

        wrist = _cylinder_z(radius=0.14, height=0.22, sections=16)
        wrist.apply_translation([0, 1.72, 0.62])
        _set_colors(wrist, chassis_col)
        parts.append(wrist)

        for dx in [-0.12, 0.12]:
            claw = trimesh.creation.box(extents=[0.06, 0.28, 0.12])
            claw.apply_translation([dx, 1.72, 0.82])
            _set_colors(claw, chrome_col)
            parts.append(claw)

        return trimesh.util.concatenate(parts)

    def _create_airplane(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        body_col = [230, 235, 245, 255]
        p = prompt.lower()
        if "dark" in p or "stealth" in p:
            body_col = [32, 35, 42, 255]

        fuselage = _cylinder_z(radius=0.34, height=2.6, sections=24)
        fuselage.apply_translation([0, 0.85, 0])
        _set_colors(fuselage, body_col)
        parts.append(fuselage)

        cone = trimesh.creation.cone(radius=0.34, height=0.75, sections=24)
        cone.apply_translation([0, 0, 1.3])
        cone.apply_translation([0, 0.85, 0.35])
        _set_colors(cone, [int(c * 0.9) for c in body_col[:3]] + [255])
        parts.append(cone)

        canopy = trimesh.creation.box(extents=[0.38, 0.24, 0.65])
        canopy.apply_translation([0, 1.12, 0.45])
        _set_colors(canopy, [20, 25, 40, 255])
        parts.append(canopy)

        wings = trimesh.creation.box(extents=[2.8, 0.05, 0.82])
        wings.apply_translation([0, 0.80, -0.15])
        _set_colors(wings, body_col)
        parts.append(wings)

        for dx in [-0.75, 0.75]:
            engine = _cylinder_z(radius=0.15, height=0.72, sections=16)
            engine.apply_translation([dx, 0.68, -0.22])
            _set_colors(engine, [50, 55, 65, 255])
            parts.append(engine)

        fin = trimesh.creation.box(extents=[0.05, 0.68, 0.52])
        fin.apply_translation([0, 1.30, -1.05])
        _set_colors(fin, body_col)
        parts.append(fin)

        h_tail = trimesh.creation.box(extents=[1.05, 0.04, 0.35])
        h_tail.apply_translation([0, 0.95, -1.15])
        _set_colors(h_tail, body_col)
        parts.append(h_tail)

        return trimesh.util.concatenate(parts)

    def _create_boat_ship(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        hull_col = [40, 48, 65, 255]
        deck_col = [145, 95, 52, 255]

        hull = trimesh.creation.box(extents=[1.05, 0.55, 2.3])
        hull.apply_translation([0, 0.42, 0])
        _set_colors(hull, hull_col)
        parts.append(hull)

        bow = trimesh.creation.box(extents=[0.75, 0.55, 0.85])
        bow.apply_translation([0, 0.42, 1.35])
        _set_colors(bow, hull_col)
        parts.append(bow)

        deck = trimesh.creation.box(extents=[0.98, 0.04, 2.8])
        deck.apply_translation([0, 0.71, 0.25])
        _set_colors(deck, deck_col)
        parts.append(deck)

        cabin = trimesh.creation.box(extents=[0.72, 0.48, 0.82])
        cabin.apply_translation([0, 0.95, -0.32])
        _set_colors(cabin, [230, 235, 240, 255])
        parts.append(cabin)

        mast = _cylinder_y(radius=0.055, height=1.75, sections=16)
        mast.apply_translation([0, 1.55, 0.42])
        _set_colors(mast, [110, 70, 35, 255])
        parts.append(mast)

        yard = _cylinder_x(radius=0.038, height=1.05, sections=12)
        yard.apply_translation([0, 2.05, 0.42])
        _set_colors(yard, [110, 70, 35, 255])
        parts.append(yard)

        return trimesh.util.concatenate(parts)

    def _create_tree_mushroom(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        p = prompt.lower()
        is_mushroom = any(w in p for w in ["mushroom", "fungus", "shroom", "toadstool"])

        if is_mushroom:
            stem = _cylinder_y(radius=0.22, height=1.1, sections=20)
            stem.apply_translation([0, 0.55, 0])
            _set_colors(stem, [235, 230, 215, 255])
            parts.append(stem)

            gills = _cylinder_y(radius=0.45, height=0.08, sections=24)
            gills.apply_translation([0, 1.08, 0])
            _set_colors(gills, [205, 195, 175, 255])
            parts.append(gills)

            cap = trimesh.creation.icosphere(subdivisions=3, radius=0.82)
            cap.vertices[:, 1] *= 0.5
            cap.apply_translation([0, 1.25, 0])
            _set_colors(cap, [215, 38, 42, 255])
            parts.append(cap)
        else:
            trunk = _cylinder_y(radius=0.26, height=1.4, sections=16)
            trunk.apply_translation([0, 0.70, 0])
            _set_colors(trunk, [105, 68, 35, 255])
            parts.append(trunk)

            t1 = _cone_y(radius=1.1, height=1.05, sections=16)
            t1.apply_translation([0, 1.25, 0])
            _set_colors(t1, [28, 105, 42, 255])
            parts.append(t1)

            t2 = _cone_y(radius=0.84, height=0.92, sections=16)
            t2.apply_translation([0, 1.82, 0])
            _set_colors(t2, [36, 138, 52, 255])
            parts.append(t2)

            t3 = _cone_y(radius=0.55, height=0.78, sections=16)
            t3.apply_translation([0, 2.35, 0])
            _set_colors(t3, [48, 168, 64, 255])
            parts.append(t3)

        return trimesh.util.concatenate(parts)

    def _create_ring_crown(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        p = prompt.lower()
        gold_col = [225, 185, 35, 255]
        is_crown = any(w in p for w in ["crown", "tiara", "coronet", "circlet"])

        if is_crown:
            base = _torus_y(major_radius=0.75, minor_radius=0.065, major_sections=36)
            base.apply_translation([0, 0.25, 0])
            _set_colors(base, gold_col)
            parts.append(base)

            for i in range(6):
                ang = i * (2 * math.pi / 6)
                peak = _cone_y(radius=0.12, height=0.58, sections=12)
                peak.apply_translation([0.75 * math.cos(ang), 0.32, 0.75 * math.sin(ang)])
                _set_colors(peak, gold_col)
                parts.append(peak)

                gem = trimesh.creation.icosphere(subdivisions=2, radius=0.065)
                gem.apply_translation([0.75 * math.cos(ang), 0.62, 0.75 * math.sin(ang)])
                _set_colors(gem, [220, 28, 45, 255])
                parts.append(gem)
        else:
            ring = _torus_y(major_radius=0.62, minor_radius=0.085, major_sections=36)
            ring.apply_translation([0, 0.62, 0])
            _set_colors(ring, gold_col)
            parts.append(ring)

            bezel = trimesh.creation.box(extents=[0.32, 0.18, 0.32])
            bezel.apply_translation([0, 0.75, 0.62])
            _set_colors(bezel, gold_col)
            parts.append(bezel)

            gem = trimesh.creation.icosphere(subdivisions=2, radius=0.22)
            gem.apply_translation([0, 0.90, 0.62])
            _set_colors(gem, [175, 235, 255, 255])
            parts.append(gem)

        return trimesh.util.concatenate(parts)

    def _create_turret_cannon(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        metal_col = [55, 60, 72, 255]
        dark_col = [30, 32, 38, 255]

        base = _cylinder_y(radius=0.85, height=0.22, sections=32)
        base.apply_translation([0, 0.11, 0])
        _set_colors(base, dark_col)
        parts.append(base)

        for dx in [-0.42, 0.42]:
            bracket = trimesh.creation.box(extents=[0.14, 0.62, 0.45])
            bracket.apply_translation([dx, 0.45, 0])
            _set_colors(bracket, metal_col)
            parts.append(bracket)

        housing = trimesh.creation.box(extents=[0.72, 0.52, 0.95])
        housing.apply_translation([0, 0.68, 0])
        _set_colors(housing, metal_col)
        parts.append(housing)

        for dx in [-0.22, 0.22]:
            barrel = _cylinder_z(radius=0.075, height=1.65, sections=16)
            barrel.apply_translation([dx, 0.68, 0.95])
            _set_colors(barrel, dark_col)
            parts.append(barrel)

            muzzle = _cylinder_z(radius=0.10, height=0.18, sections=16)
            muzzle.apply_translation([dx, 0.68, 1.80])
            _set_colors(muzzle, [200, 160, 40, 255])
            parts.append(muzzle)

        optic = _cylinder_z(radius=0.12, height=0.45, sections=16)
        optic.apply_translation([0, 1.05, 0.15])
        _set_colors(optic, [0, 220, 255, 255])
        parts.append(optic)

        return trimesh.util.concatenate(parts)

    def _create_tech_gadget(self, prompt: str = "") -> trimesh.Trimesh:
        parts = []
        chassis_col = [42, 46, 56, 255]
        glow_col = [0, 220, 255, 255]

        chassis = trimesh.creation.box(extents=[1.3, 0.92, 0.88])
        chassis.apply_translation([0, 0.56, 0])
        _set_colors(chassis, chassis_col)
        parts.append(chassis)

        for dx in [-0.58, 0.58]:
            for dz in [-0.38, 0.38]:
                foot = _cylinder_y(radius=0.08, height=0.10, sections=16)
                foot.apply_translation([dx, 0.05, dz])
                _set_colors(foot, [25, 26, 30, 255])
                parts.append(foot)

        screen = trimesh.creation.box(extents=[1.1, 0.72, 0.04])
        screen.apply_translation([0, 0.58, 0.45])
        _set_colors(screen, glow_col)
        parts.append(screen)

        antenna = _cylinder_y(radius=0.025, height=0.65, sections=12)
        antenna.apply_translation([0.45, 1.32, -0.25])
        _set_colors(antenna, [180, 190, 200, 255])
        parts.append(antenna)

        return trimesh.util.concatenate(parts)

    # -------------------------------------------------------------------------
    # UNIVERSAL DEEP SEMANTIC PROCEDURAL SYNTHESIZER (OUT-OF-SAMPLE FALLBACK)
    # -------------------------------------------------------------------------
    def _create_procedural_artifact(self, prompt: str) -> trimesh.Trimesh:
        parts = []
        p = prompt.lower()

        # 1. Color / Material extraction
        body_col = [120, 130, 145, 255] # Default sleek slate
        accent_col = [218, 175, 45, 255] # Default gold
        glow_col = [0, 220, 255, 255] # Cyan glow

        if any(w in p for w in ["wood", "wooden", "oak", "timber", "rustic", "brown"]):
            body_col = [135, 85, 45, 255]
        elif any(w in p for w in ["gold", "golden", "brass", "bronze", "yellow"]):
            body_col = [220, 180, 40, 255]
        elif any(w in p for w in ["dark", "black", "stealth", "shadow", "ebony", "obsidian"]):
            body_col = [28, 30, 36, 255]
        elif any(w in p for w in ["white", "silver", "marble", "chrome", "platinum"]):
            body_col = [235, 238, 245, 255]
        elif any(w in p for w in ["red", "crimson", "ruby", "scarlet", "blood"]):
            body_col = [215, 35, 45, 255]
        elif any(w in p for w in ["green", "emerald", "nature", "jade"]):
            body_col = [35, 160, 65, 255]
        elif any(w in p for w in ["purple", "violet", "arcane", "void", "amethyst"]):
            body_col = [150, 55, 215, 255]
        elif any(w in p for w in ["blue", "azure", "cyan", "sapphire"]):
            body_col = [25, 120, 230, 255]

        if "neon" in p or "plasma" in p or "magenta" in p or "pink" in p:
            glow_col = [235, 30, 160, 255]
        elif "green" in p or "toxic" in p or "acid" in p:
            glow_col = [30, 235, 100, 255]
        elif "red" in p or "lava" in p or "fire" in p:
            glow_col = [255, 60, 30, 255]

        # 2. Structural & feature detection
        has_legs = any(w in p for w in ["leg", "legs", "foot", "feet", "tripod", "quad", "walker", "stand", "stool", "table"])
        has_wheels = any(w in p for w in ["wheel", "wheels", "tread", "tire", "roller"])
        has_wings = any(w in p for w in ["wing", "wings", "fin", "fins", "glider", "flying"])
        has_handle = any(w in p for w in ["handle", "grip", "holder"])
        has_glow = any(w in p for w in ["glow", "glowing", "neon", "energy", "plasma", "crystal", "core", "magic", "light"])

        # 3. Primary shape
        is_box = any(w in p for w in ["box", "cube", "block", "brick", "crate", "case", "storage", "safe", "monolith", "chest", "toaster", "terminal", "console"])
        is_cylinder = any(w in p for w in ["cylinder", "tube", "pipe", "can", "silo", "pillar", "column", "spire", "chimney", "stack"])
        is_sphere = any(w in p for w in ["sphere", "orb", "globe", "ball", "eye", "bubble", "planet", "round", "oval"])
        is_ring = any(w in p for w in ["ring", "torus", "donut", "loop", "portal", "gateway", "halo", "belt"])
        is_cone = any(w in p for w in ["cone", "pyramid", "spike", "peak", "shard", "obelisk"])

        base_y = 0.0
        if has_legs:
            leg_h = 0.55
            for dx in [-0.45, 0.45]:
                for dz in [-0.45, 0.45]:
                    leg = _cylinder_y(radius=0.045, height=leg_h, sections=16)
                    leg.apply_translation([dx, leg_h / 2.0, dz])
                    _set_colors(leg, [int(c * 0.8) for c in body_col[:3]] + [255])
                    parts.append(leg)
            base_y = leg_h
        elif has_wheels:
            wh_r = 0.22
            for dx in [-0.55, 0.55]:
                for dz in [-0.45, 0.45]:
                    wheel = _cylinder_x(radius=wh_r, height=0.12, sections=16)
                    wheel.apply_translation([dx, wh_r, dz])
                    _set_colors(wheel, [28, 30, 36, 255])
                    parts.append(wheel)
            base_y = wh_r * 2
        else:
            plinth = trimesh.creation.box(extents=[1.2, 0.12, 1.2])
            plinth.apply_translation([0, 0.06, 0])
            _set_colors(plinth, [int(c * 0.75) for c in body_col[:3]] + [255])
            parts.append(plinth)
            base_y = 0.12

        # 4. Primary Body Assembly
        if is_box:
            body = trimesh.creation.box(extents=[1.0, 0.9, 0.85])
            body.apply_translation([0, base_y + 0.45, 0])
            _set_colors(body, body_col)
            parts.append(body)

            plate = trimesh.creation.box(extents=[0.82, 0.72, 0.04])
            plate.apply_translation([0, base_y + 0.45, 0.44])
            _set_colors(plate, [int(c * 0.85) for c in body_col[:3]] + [255])
            parts.append(plate)
        elif is_cylinder:
            body = _cylinder_y(radius=0.52, height=1.3, sections=28)
            body.apply_translation([0, base_y + 0.65, 0])
            _set_colors(body, body_col)
            parts.append(body)

            collar = _torus_y(major_radius=0.54, minor_radius=0.03, major_sections=28)
            collar.apply_translation([0, base_y + 1.2, 0])
            _set_colors(collar, accent_col)
            parts.append(collar)
        elif is_sphere:
            body = trimesh.creation.icosphere(subdivisions=3, radius=0.62)
            body.apply_translation([0, base_y + 0.62, 0])
            _set_colors(body, body_col)
            parts.append(body)

            ring = _torus_y(major_radius=0.78, minor_radius=0.03, major_sections=32)
            ring.apply_translation([0, base_y + 0.62, 0])
            _set_colors(ring, accent_col)
            parts.append(ring)
        elif is_ring:
            body = _torus_y(major_radius=0.75, minor_radius=0.12, major_sections=36)
            body.apply_translation([0, base_y + 0.75, 0])
            _set_colors(body, body_col)
            parts.append(body)

            vortex = _cylinder_y(radius=0.62, height=0.04, sections=32)
            vortex.apply_translation([0, base_y + 0.75, 0])
            _set_colors(vortex, glow_col)
            parts.append(vortex)
        elif is_cone:
            body = _cone_y(radius=0.58, height=1.45, sections=20)
            body.apply_translation([0, base_y + 0.725, 0])
            _set_colors(body, body_col)
            parts.append(body)

            tip_gem = trimesh.creation.icosphere(subdivisions=2, radius=0.12)
            tip_gem.apply_translation([0, base_y + 1.5, 0])
            _set_colors(tip_gem, glow_col)
            parts.append(tip_gem)
        else:
            pylon = _cylinder_y(radius=0.42, height=0.95, sections=24)
            pylon.apply_translation([0, base_y + 0.475, 0])
            _set_colors(pylon, body_col)
            parts.append(pylon)

            cap = trimesh.creation.box(extents=[0.75, 0.12, 0.75])
            cap.apply_translation([0, base_y + 0.98, 0])
            _set_colors(cap, accent_col)
            parts.append(cap)

        # 5. Modifiers
        if has_wings:
            wing = trimesh.creation.box(extents=[2.4, 0.04, 0.65])
            wing.apply_translation([0, base_y + 0.55, 0])
            _set_colors(wing, accent_col)
            parts.append(wing)

        if has_handle:
            handle = trimesh.creation.box(extents=[0.06, 0.45, 0.22])
            handle.apply_translation([0.62, base_y + 0.5, 0])
            _set_colors(handle, accent_col)
            parts.append(handle)

        if has_glow:
            glow_core = trimesh.creation.icosphere(subdivisions=2, radius=0.22)
            glow_core.apply_translation([0, base_y + 0.55, 0.35])
            _set_colors(glow_core, glow_col)
            parts.append(glow_core)

        return trimesh.util.concatenate(parts)

    # -------------------------------------------------------------------------
    # MAIN INGESTION DISPATCHER
    # -------------------------------------------------------------------------
    def generate_mesh(self, prompt: str, detail_level: str = "high") -> trimesh.Trimesh:
        # 1. Vehicles & Aircraft
        if _match_words(prompt, ["car", "vehicle", "automobile", "coupe", "sedan", "truck", "sports car"]):
            mesh = self._create_sports_car(prompt)
        elif _match_words(prompt, ["spaceship", "starfighter", "rocket", "shuttle", "interceptor"]):
            mesh = self._create_spaceship(prompt)
        elif _match_words(prompt, ["airplane", "plane", "jet", "aircraft", "aeroplane", "fighter jet", "glider"]):
            mesh = self._create_airplane(prompt)
        elif _match_words(prompt, ["boat", "ship", "vessel", "yacht", "pirate ship", "sailboat", "canoe", "frigate"]):
            mesh = self._create_boat_ship(prompt)
        elif _match_words(prompt, ["drone", "quadcopter", "uav", "hovercraft", "hover"]):
            mesh = self._create_drone(prompt)

        # 2. Robotics & Sci-Fi Tech
        elif _match_words(prompt, ["robot arm", "robotic arm", "gripper", "claw", "manipulator", "actuator"]):
            mesh = self._create_robot_arm(prompt)
        elif _match_words(prompt, ["mech", "robot", "android", "cyborg", "bipedal", "gundam", "exoskeleton"]):
            mesh = self._create_mech(prompt)
        elif _match_words(prompt, ["turret", "cannon", "artillery", "sentry gun", "mortar"]):
            mesh = self._create_turret_cannon(prompt)
        elif _match_words(prompt, ["computer", "console", "terminal", "generator", "battery", "gadget", "device", "server"]):
            mesh = self._create_tech_gadget(prompt)

        # 3. Weapons & Combat
        elif _match_words(prompt, ["sword", "blade", "broadsword", "katana", "rapier", "saber", "cutlass"]):
            mesh = self._create_sword(prompt)
        elif _match_words(prompt, ["axe", "hatchet", "tomahawk", "halberd"]):
            mesh = self._create_axe(prompt)
        elif _match_words(prompt, ["hammer", "mace", "morningstar", "warhammer", "mjolnir"]):
            mesh = self._create_hammer(prompt)
        elif _match_words(prompt, ["shield", "buckler", "aegis", "targe"]):
            mesh = self._create_shield(prompt)
        elif _match_words(prompt, ["gun", "blaster", "pistol", "rifle", "plasma gun", "laser gun"]):
            mesh = self._create_gun_blaster(prompt)
        elif _match_words(prompt, ["staff", "scepter", "wand", "rod"]):
            mesh = self._create_staff(prompt)

        # 4. Containers, Vessels & Tableware
        elif _match_words(prompt, ["table", "desk", "coffee table", "dining table", "counter", "workbench"]):
            mesh = self._create_table(prompt)
        elif _match_words(prompt, ["barrel", "keg", "cask", "vat"]):
            mesh = self._create_barrel(prompt)
        elif _match_words(prompt, ["mug", "cup", "coffee mug", "teacup", "tankard", "chalice", "goblet", "stein"]):
            mesh = self._create_mug_cup(prompt)
        elif _match_words(prompt, ["chest", "coffer", "box", "crate"]):
            mesh = self._create_chest(prompt)
        elif _match_words(prompt, ["potion", "bottle", "flask", "elixir", "vial"]):
            mesh = self._create_potion(prompt)
        elif _match_words(prompt, ["vase", "pot", "urn", "amphora"]):
            mesh = self._create_vase(prompt)

        # 5. Wearables & Jewelry
        elif _match_words(prompt, ["helmet", "mask", "visor", "bascinet", "headgear", "kabuto"]):
            mesh = self._create_helmet(prompt)
        elif _match_words(prompt, ["ring", "crown", "tiara", "circlet", "amulet", "gemstone ring"]):
            mesh = self._create_ring_crown(prompt)

        # 6. Architecture & Nature
        elif _match_words(prompt, ["tower", "castle", "fortress", "keep", "watchtower", "bastion"]):
            mesh = self._create_tower_castle(prompt)
        elif _match_words(prompt, ["tree", "pine", "palm", "mushroom", "fungus", "shroom"]):
            mesh = self._create_tree_mushroom(prompt)
        elif _match_words(prompt, ["crystal", "gem", "mineral", "geode", "quartz"]):
            mesh = self._create_crystal(prompt)
        elif _match_words(prompt, ["chair", "seat", "stool", "throne", "bench"]):
            mesh = self._create_chair(prompt)

        # 7. Intelligent Semantic Procedural Synthesis (Universal Open-Ended Fallback)
        else:
            mesh = self._create_procedural_artifact(prompt)

        # Re-center and normalize to standard 3D studio scale (height ~ 1.8 units)
        mesh.rezero()
        max_extent = max(mesh.extents)
        if max_extent > 0:
            scale_factor = 2.0 / max_extent
            mesh.apply_scale(scale_factor)

        # Sit neatly on ground at Y = 0, centered in X and Z
        bounds = mesh.bounds
        center_x = (bounds[0][0] + bounds[1][0]) / 2.0
        min_y = bounds[0][1]
        center_z = (bounds[0][2] + bounds[1][2]) / 2.0
        mesh.apply_translation([-center_x, -min_y, -center_z])

        return mesh
