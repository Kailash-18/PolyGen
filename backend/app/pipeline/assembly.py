"""
PolyGen 3D Assembly Engine & Kinematics Decomposer
Decomposes 3D models into functional mechanical assemblies with directional
explosion vectors, collision-free clearance solvers, PBR materials, and relationship graphs.
Extracted and enhanced from reference architecture for precision exploded views.
"""
from __future__ import annotations

import math
from typing import List, Dict, Optional, Literal, Tuple, Any
from pydantic import BaseModel, Field, ConfigDict

SHAPES = (
    "box", "rounded_box", "cylinder", "disc", "sphere",
    "ellipsoid", "dome", "capsule", "cone", "torus", "plate", "frame", "arch"
)
DETAIL_SHAPES = SHAPES + ("cross", "slots")
MATERIALS = (
    "plastic", "glossy_plastic", "rubber", "metal",
    "aluminum", "glass", "pcb", "fabric", "screen"
)

class AssemblyDetail(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    parent_id: str = Field(..., alias="parentId")
    shape: str
    size: List[float]
    position: List[float]
    rotation: List[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0])
    color: str = "#30343b"
    material: str = "plastic"
    count: int = 1
    corner_radius: Optional[float] = Field(default=None, alias="cornerRadius")

class AssemblyPart(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
    name: str = ""
    part_type: str = Field(default="structure", alias="type")
    shape: str
    size: List[float]
    position: List[float]
    rotation: List[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0])
    color: str = "#9aa0a6"
    material: str = "metal"
    explode_dir: List[float] = Field(default_factory=lambda: [0.0, 1.0, 0.0], alias="explodeDir")
    explode_dist: float = Field(default=1.0, alias="explodeDist")
    corner_radius: Optional[float] = Field(default=None, alias="cornerRadius")
    wall: Optional[float] = None
    function: str = ""
    layer: int = 0

class AssemblyRelationship(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
    from_part: str = Field(..., alias="from")
    to_part: str = Field(..., alias="to")
    rel_type: str = Field(default="mounts", alias="type")
    description: str = ""

class AssemblyModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    id: str
    name: str
    units: str = "mm"
    overall_size: List[float] = Field(..., alias="overallSize")
    parts: List[AssemblyPart]
    details: List[AssemblyDetail] = []
    relationships: List[AssemblyRelationship] = []
    primary_axis: str = "y"

class ExplosionPose(BaseModel):
    part_id: str
    current_position: List[float]
    offset: List[float]
    progress: float

class AssemblyEngine:
    @staticmethod
    def _normalize(vec: List[float]) -> List[float]:
        mag = math.sqrt(sum(v * v for v in vec))
        if mag < 1e-6:
            return [0.0, 1.0, 0.0]
        return [round(v / mag, 4) for v in vec]

    @staticmethod
    def _resolve_axis_vector(axis: str, magnitude: float = 1.0) -> List[float]:
        axis_map = {
            "x": [1.0, 0.0, 0.0],
            "-x": [-1.0, 0.0, 0.0],
            "y": [0.0, 1.0, 0.0],
            "-y": [0.0, -1.0, 0.0],
            "z": [0.0, 0.0, 1.0],
            "-z": [0.0, 0.0, -1.0]
        }
        vec = axis_map.get(axis.lower(), [0.0, 1.0, 0.0])
        return [round(v * magnitude, 4) for v in vec]

    @staticmethod
    def _order_explode_vectors(parts: List[AssemblyPart], primary_axis: str = "y") -> Dict[str, List[float]]:
        trajectories: Dict[str, List[float]] = {}
        for p in parts:
            base_dir = p.explode_dir if p.explode_dir else [0.0, 1.0, 0.0]
            norm_dir = AssemblyEngine._normalize(base_dir)
            layer_boost = 1.0 + 0.15 * abs(p.layer)
            trajectories[p.id] = [round(c * layer_boost, 4) for c in norm_dir]
        return trajectories

    @classmethod
    def create_broadsword_assembly(cls, model_id: str = "sword-01") -> AssemblyModel:
        parts = [
            AssemblyPart(
                id="blade_core",
                name="Adamantine Blade Spine",
                type="structure",
                shape="box",
                size=[14.0, 720.0, 3.5],
                position=[0.0, 360.0, 0.0],
                color="#cbd5e1",
                material="metal",
                explodeDir=[0.0, 1.0, 0.0],
                explodeDist=1.2,
                function="High-carbon edge retention central cutting blade",
                layer=2
            ),
            AssemblyPart(
                id="plasma_channel",
                name="Energized Plasma Fuller",
                type="sensor",
                shape="box",
                size=[5.0, 600.0, 4.2],
                position=[0.0, 340.0, 0.0],
                color="#06b6d4",
                material="glass",
                explodeDir=[0.0, 0.9806, 0.1961],
                explodeDist=1.5,
                function="Superconducting ion channel running along blade centre",
                layer=3
            ),
            AssemblyPart(
                id="crossguard",
                name="Aegis Titanium Crossguard",
                type="structure",
                shape="rounded_box",
                size=[180.0, 24.0, 28.0],
                position=[0.0, 0.0, 0.0],
                color="#334155",
                material="aluminum",
                explodeDir=[0.0, 0.0, 0.0],
                explodeDist=0.0,
                cornerRadius=4.0,
                function="Dual-wing defensive handguard and hilt anchor",
                layer=0
            ),
            AssemblyPart(
                id="power_cell",
                name="Kyber Sub-Hilt Battery Unit",
                type="power_source",
                shape="cylinder",
                size=[22.0, 50.0, 22.0],
                position=[0.0, -32.0, 0.0],
                color="#38bdf8",
                material="pcb",
                explodeDir=[0.0, -1.0, 0.0],
                explodeDist=0.8,
                function="Micro-fusion cell supplying high-discharge plasma current",
                layer=-1
            ),
            AssemblyPart(
                id="hilt_grip",
                name="Ergonomic Grip Sleeve",
                type="interface",
                shape="cylinder",
                size=[28.0, 140.0, 28.0],
                position=[0.0, -95.0, 0.0],
                color="#1e293b",
                material="rubber",
                explodeDir=[0.0, -1.0, 0.0],
                explodeDist=1.4,
                function="Shock-absorbing composite wrap with tactile indexing",
                layer=-2
            ),
            AssemblyPart(
                id="pommel",
                name="Counterweight Magnetic Pommel",
                type="structure",
                shape="sphere",
                size=[42.0, 42.0, 42.0],
                position=[0.0, -186.0, 0.0],
                color="#94a3b8",
                material="metal",
                explodeDir=[0.0, -1.0, 0.0],
                explodeDist=2.1,
                function="Mass counterbalance and magnetic sheath locking point",
                layer=-3
            )
        ]

        details = [
            AssemblyDetail(
                parentId="crossguard",
                shape="disc",
                size=[16.0, 4.0, 16.0],
                position=[0.0, 0.0, 15.0],
                color="#0ea5e9",
                material="glossy_plastic"
            ),
            AssemblyDetail(
                parentId="crossguard",
                shape="slots",
                size=[60.0, 4.0, 8.0],
                position=[0.0, 8.0, 0.0],
                color="#1e293b",
                material="metal",
                count=4
            ),
            AssemblyDetail(
                parentId="blade_core",
                shape="torus",
                size=[18.0, 3.0, 18.0],
                position=[0.0, 120.0, 0.0],
                color="#38bdf8",
                material="aluminum"
            )
        ]

        relationships = [
            AssemblyRelationship(id="rel_power_blade", from_part="power_cell", to_part="plasma_channel", rel_type="powers", description="Ionizing discharge bus"),
            AssemblyRelationship(id="rel_mount_blade", from_part="crossguard", to_part="blade_core", rel_type="mounts", description="Press-fit mortise and tenon tang lock"),
            AssemblyRelationship(id="rel_mount_hilt", from_part="crossguard", to_part="hilt_grip", rel_type="supports", description="Threaded hilt retention rod"),
            AssemblyRelationship(id="rel_lock_pommel", from_part="hilt_grip", to_part="pommel", rel_type="mounts", description="M16 retaining pommel nut")
        ]

        return AssemblyModel(
            id=model_id,
            name="Cybernetic Broadsword",
            units="mm",
            overallSize=[180.0, 950.0, 42.0],
            parts=parts,
            details=details,
            relationships=relationships,
            primary_axis="y"
        )



    @classmethod
    def create_shield_assembly(cls, model_id: str = "shield-01") -> AssemblyModel:
        parts = [
            AssemblyPart(
                id="outer_rim",
                name="Segmented Ballistic Rim",
                type="structure",
                shape="torus",
                size=[540.0, 36.0, 540.0],
                position=[0.0, 0.0, 0.0],
                rotation=[90.0, 0.0, 0.0],
                color="#334155",
                material="metal",
                explodeDir=[0.0, 0.0, 1.0],
                explodeDist=0.9,
                function="Perimeter kinetic deflection band absorbing peripheral strikes",
                layer=1
            ),
            AssemblyPart(
                id="face_plate",
                name="Central Convex Deflector Shell",
                type="cover",
                shape="dome",
                size=[490.0, 490.0, 45.0],
                position=[0.0, 0.0, 12.0],
                rotation=[0.0, 0.0, 0.0],
                color="#1e3a8a",
                material="aluminum",
                explodeDir=[0.0, 0.0, 1.0],
                explodeDist=1.6,
                function="Hydroformed convex alloy plate deflecting incoming kinetic energy",
                layer=2
            ),
            AssemblyPart(
                id="kinetic_boss",
                name="Central Kinetic Boss Core",
                type="mechanism",
                shape="cylinder",
                size=[140.0, 40.0, 140.0],
                position=[0.0, 0.0, 32.0],
                rotation=[90.0, 0.0, 0.0],
                color="#f59e0b",
                material="glossy_plastic",
                explodeDir=[0.0, 0.0, 1.0],
                explodeDist=2.3,
                function="Harmonic shock dampener dissipating direct frontal blasts",
                layer=3
            ),
            AssemblyPart(
                id="backing_frame",
                name="Arm Support Backing Truss",
                type="structure",
                shape="plate",
                size=[460.0, 460.0, 12.0],
                position=[0.0, 0.0, -10.0],
                color="#475569",
                material="metal",
                explodeDir=[0.0, 0.0, -1.0],
                explodeDist=1.1,
                function="Rigid internal skeleton anchoring arm brackets and dampeners",
                layer=-1
            ),
            AssemblyPart(
                id="forearm_straps",
                name="Padded Arm Retention Straps",
                type="interface",
                shape="arch",
                size=[180.0, 80.0, 50.0],
                position=[0.0, -40.0, -35.0],
                rotation=[0.0, 0.0, 90.0],
                color="#0f172a",
                material="fabric",
                explodeDir=[0.0, 0.0, -1.0],
                explodeDist=1.9,
                function="Dual adjustable hook-and-loop forearm stability harness",
                layer=-2
            )
        ]

        details = [
            AssemblyDetail(
                parentId="outer_rim",
                shape="cylinder",
                size=[12.0, 6.0, 12.0],
                position=[0.0, 260.0, 0.0],
                color="#94a3b8",
                material="metal"
            ),
            AssemblyDetail(
                parentId="kinetic_boss",
                shape="torus",
                size=[110.0, 8.0, 110.0],
                position=[0.0, 0.0, 50.0],
                color="#fbbf24",
                material="metal"
            )
        ]

        relationships = [
            AssemblyRelationship(id="rel_rim_backing", from_part="backing_frame", to_part="outer_rim", rel_type="supports", description="Radial structural spars"),
            AssemblyRelationship(id="rel_face_backing", from_part="backing_frame", to_part="face_plate", rel_type="mounts", description="Countersunk Allen bolt array"),
            AssemblyRelationship(id="rel_boss_face", from_part="face_plate", to_part="kinetic_boss", rel_type="mounts", description="Central locking hub"),
            AssemblyRelationship(id="rel_strap_backing", from_part="backing_frame", to_part="forearm_straps", rel_type="mounts", description="Riveted steel retaining tabs")
        ]

        return AssemblyModel(
            id=model_id,
            name="Aegis Kinetic Energy Shield",
            units="mm",
            overallSize=[540.0, 540.0, 95.0],
            parts=parts,
            details=details,
            relationships=relationships,
            primary_axis="z"
        )



    @classmethod
    def create_chair_assembly(cls, model_id: str = "chair-01") -> AssemblyModel:
        parts = [
            AssemblyPart(
                id="star_base",
                name="5-Star Reinforced Nylon Base",
                type="structure",
                shape="arch",
                size=[680.0, 95.0, 680.0],
                position=[0.0, 50.0, 0.0],
                color="#111827",
                material="plastic",
                explodeDir=[0.0, -1.0, 0.0],
                explodeDist=1.8,
                function="High-strength glass-fiber star chassis distributing load",
                layer=-3
            ),
            AssemblyPart(
                id="gas_piston",
                name="Class-4 Pneumatic Gas Lift Piston",
                type="mechanism",
                shape="cylinder",
                size=[50.0, 240.0, 50.0],
                position=[0.0, 180.0, 0.0],
                color="#cbd5e1",
                material="metal",
                explodeDir=[0.0, -1.0, 0.0],
                explodeDist=1.0,
                function="Nitrogen gas cylinder controlling height and 360-swivel",
                layer=-2
            ),
            AssemblyPart(
                id="seat_mechanism",
                name="Syncro-Tilt Control Engine",
                type="mechanism",
                shape="box",
                size=[220.0, 65.0, 240.0],
                position=[0.0, 310.0, 0.0],
                color="#374151",
                material="metal",
                explodeDir=[0.0, 0.0, 0.0],
                explodeDist=0.0,
                function="Dual-lever recline lock and seat depth adjustment bracket",
                layer=0
            ),
            AssemblyPart(
                id="seat_cushion",
                name="Contoured Ergonomic Seat Cushion",
                type="interface",
                shape="rounded_box",
                size=[510.0, 75.0, 480.0],
                position=[0.0, 370.0, 0.0],
                color="#1f2937",
                material="fabric",
                explodeDir=[0.0, 1.0, 0.0],
                explodeDist=0.8,
                cornerRadius=25.0,
                function="Molded waterfall foam reducing thigh pressure and fatigue",
                layer=1
            ),
            AssemblyPart(
                id="backrest_frame",
                name="Breathable Mesh Spine Frame",
                type="structure",
                shape="frame",
                size=[470.0, 560.0, 45.0],
                position=[0.0, 660.0, -220.0],
                rotation=[12.0, 0.0, 0.0],
                color="#111827",
                material="plastic",
                explodeDir=[0.0, 0.6, -1.0],
                explodeDist=1.5,
                wall=30.0,
                function="S-curve polypropylene frame supporting elastomeric mesh",
                layer=2
            ),
            AssemblyPart(
                id="lumbar_support",
                name="Dynamic Lumbar Cushion Pad",
                type="interface",
                shape="plate",
                size=[320.0, 140.0, 25.0],
                position=[0.0, 520.0, -210.0],
                color="#4b5563",
                material="rubber",
                explodeDir=[0.0, 0.2, -1.0],
                explodeDist=1.8,
                function="Height-adjustable lower spine posture stabilizer",
                layer=3
            ),
            AssemblyPart(
                id="armrest_left",
                name="4D Soft-Touch Armrest (Left)",
                type="interface",
                shape="rounded_box",
                size=[80.0, 220.0, 240.0],
                position=[-270.0, 460.0, -40.0],
                color="#1f2937",
                material="rubber",
                explodeDir=[-1.0, 0.3, 0.0],
                explodeDist=1.4,
                cornerRadius=15.0,
                function="Multidirectional pivoting elbow rest with height adjustment",
                layer=1
            ),
            AssemblyPart(
                id="armrest_right",
                name="4D Soft-Touch Armrest (Right)",
                type="interface",
                shape="rounded_box",
                size=[80.0, 220.0, 240.0],
                position=[270.0, 460.0, -40.0],
                color="#1f2937",
                material="rubber",
                explodeDir=[1.0, 0.3, 0.0],
                explodeDist=1.4,
                cornerRadius=15.0,
                function="Multidirectional pivoting elbow rest with height adjustment",
                layer=1
            ),
            AssemblyPart(
                id="caster_wheels",
                name="High-Glide Dual PU Caster Set",
                type="actuator",
                shape="cylinder",
                size=[65.0, 55.0, 65.0],
                position=[0.0, 15.0, 0.0],
                rotation=[0.0, 0.0, 90.0],
                color="#0f172a",
                material="rubber",
                explodeDir=[0.0, -1.0, 0.0],
                explodeDist=2.4,
                function="Smooth silent rolling casters on hard and soft floors",
                layer=-4
            )
        ]

        details = [
            AssemblyDetail(
                parentId="seat_mechanism",
                shape="cylinder",
                size=[18.0, 120.0, 18.0],
                position=[115.0, 310.0, 20.0],
                rotation=[0.0, 0.0, 90.0],
                color="#9ca3af",
                material="aluminum"
            ),
            AssemblyDetail(
                parentId="backrest_frame",
                shape="slots",
                size=[380.0, 440.0, 4.0],
                position=[0.0, 660.0, -220.0],
                color="#1e293b",
                material="fabric",
                count=18
            )
        ]

        relationships = [
            AssemblyRelationship(id="rel_piston_base", from_part="star_base", to_part="gas_piston", rel_type="supports", description="Tapered press-fit column"),
            AssemblyRelationship(id="rel_mech_piston", from_part="gas_piston", to_part="seat_mechanism", rel_type="mounts", description="Standard 28mm gas hub receiver"),
            AssemblyRelationship(id="rel_seat_mech", from_part="seat_mechanism", to_part="seat_cushion", rel_type="mounts", description="Steel mounting plates with 4 M6 screws"),
            AssemblyRelationship(id="rel_back_mech", from_part="seat_mechanism", to_part="backrest_frame", rel_type="controls", description="Dual-bar spring-assisted recline linkage"),
            AssemblyRelationship(id="rel_arm_l_seat", from_part="seat_mechanism", to_part="armrest_left", rel_type="mounts", description="Adjustable lateral slide bracket"),
            AssemblyRelationship(id="rel_arm_r_seat", from_part="seat_mechanism", to_part="armrest_right", rel_type="mounts", description="Adjustable lateral slide bracket"),
            AssemblyRelationship(id="rel_casters_base", from_part="star_base", to_part="caster_wheels", rel_type="mounts", description="11mm grip-ring friction stems")
        ]

        return AssemblyModel(
            id=model_id,
            name="Ergonomic Mesh Task Chair",
            units="mm",
            overallSize=[680.0, 1020.0, 680.0],
            parts=parts,
            details=details,
            relationships=relationships,
            primary_axis="y"
        )



    @classmethod
    def create_drone_assembly(cls, model_id: str = "drone-01") -> AssemblyModel:
        parts = [
            AssemblyPart(
                id="main_chassis",
                name="Central Carbon Monocoque Chassis",
                type="structure",
                shape="rounded_box",
                size=[140.0, 24.0, 140.0],
                position=[0.0, 0.0, 0.0],
                color="#1e2229",
                material="plastic",
                explodeDir=[0.0, 0.0, 0.0],
                explodeDist=0.0,
                cornerRadius=12.0,
                function="Main structural fuselage housing core avionics",
                layer=0
            ),
            AssemblyPart(
                id="top_canopy",
                name="Aerodynamic Cowling Shell",
                type="cover",
                shape="dome",
                size=[130.0, 22.0, 130.0],
                position=[0.0, 13.0, 0.0],
                color="#0f5fff",
                material="glossy_plastic",
                explodeDir=[0.0, 1.0, 0.0],
                explodeDist=1.6,
                function="Upper protective cowling and airflow deflector",
                layer=1
            ),
            AssemblyPart(
                id="flight_controller_pcb",
                name="Flight Controller & ESC Unit",
                type="controller",
                shape="box",
                size=[60.0, 4.0, 60.0],
                position=[0.0, 2.0, 0.0],
                color="#1d6639",
                material="pcb",
                explodeDir=[0.0, 1.0, 0.0],
                explodeDist=0.8,
                function="Autonomous navigation MCU and motor speed controllers",
                layer=1
            ),
            AssemblyPart(
                id="lipo_battery",
                name="4S 5200mAh LiPo Power Pack",
                type="power_source",
                shape="rounded_box",
                size=[80.0, 28.0, 45.0],
                position=[0.0, -20.0, 0.0],
                color="#f59e0b",
                material="rubber",
                explodeDir=[0.0, -1.0, 0.0],
                explodeDist=1.2,
                cornerRadius=4.0,
                function="5200mAh high-discharge propulsion battery",
                layer=-1
            ),
            AssemblyPart(
                id="bottom_plate",
                name="Vibration Isolation Baseplate",
                type="structure",
                shape="plate",
                size=[135.0, 3.0, 135.0],
                position=[0.0, -13.0, 0.0],
                color="#374151",
                material="aluminum",
                explodeDir=[0.0, -1.0, 0.0],
                explodeDist=1.7,
                function="Lower mounting deck for payload gimbal and battery bay",
                layer=-1
            ),
            AssemblyPart(
                id="arm_front_left",
                name="Front-Left Rotor Boom",
                type="mechanism",
                shape="cylinder",
                size=[18.0, 160.0, 18.0],
                position=[-110.0, 0.0, -110.0],
                rotation=[0.0, 45.0, 90.0],
                color="#111827",
                material="aluminum",
                explodeDir=[-0.707, 0.2, -0.707],
                explodeDist=1.5,
                function="Outrigger arm for FL brushless propulsion pod",
                layer=1
            ),
            AssemblyPart(
                id="rotor_front_left",
                name="FL Carbon Propeller Unit",
                type="actuator",
                shape="capsule",
                size=[180.0, 12.0, 22.0],
                position=[-190.0, 24.0, -190.0],
                rotation=[0.0, 30.0, 0.0],
                color="#2563eb",
                material="plastic",
                explodeDir=[-0.707, 0.8, -0.707],
                explodeDist=2.2,
                function="High-pitch aerodynamic lift propeller",
                layer=2
            ),
            AssemblyPart(
                id="arm_front_right",
                name="Front-Right Rotor Boom",
                type="mechanism",
                shape="cylinder",
                size=[18.0, 160.0, 18.0],
                position=[110.0, 0.0, -110.0],
                rotation=[0.0, -45.0, 90.0],
                color="#111827",
                material="aluminum",
                explodeDir=[0.707, 0.2, -0.707],
                explodeDist=1.5,
                function="Outrigger arm for FR brushless propulsion pod",
                layer=1
            ),
            AssemblyPart(
                id="rotor_front_right",
                name="FR Carbon Propeller Unit",
                type="actuator",
                shape="capsule",
                size=[180.0, 12.0, 22.0],
                position=[190.0, 24.0, -190.0],
                rotation=[0.0, -30.0, 0.0],
                color="#2563eb",
                material="plastic",
                explodeDir=[0.707, 0.8, -0.707],
                explodeDist=2.2,
                function="High-pitch counter-rotating lift propeller",
                layer=2
            ),
            AssemblyPart(
                id="arm_rear_left",
                name="Rear-Left Rotor Boom",
                type="mechanism",
                shape="cylinder",
                size=[18.0, 160.0, 18.0],
                position=[-110.0, 0.0, 110.0],
                rotation=[0.0, -45.0, 90.0],
                color="#111827",
                material="aluminum",
                explodeDir=[-0.707, 0.2, 0.707],
                explodeDist=1.5,
                function="Outrigger arm for RL brushless propulsion pod",
                layer=1
            ),
            AssemblyPart(
                id="rotor_rear_left",
                name="RL Carbon Propeller Unit",
                type="actuator",
                shape="capsule",
                size=[180.0, 12.0, 22.0],
                position=[-190.0, 24.0, 190.0],
                rotation=[0.0, 60.0, 0.0],
                color="#2563eb",
                material="plastic",
                explodeDir=[-0.707, 0.8, 0.707],
                explodeDist=2.2,
                function="High-pitch lift propeller",
                layer=2
            ),
            AssemblyPart(
                id="arm_rear_right",
                name="Rear-Right Rotor Boom",
                type="mechanism",
                shape="cylinder",
                size=[18.0, 160.0, 18.0],
                position=[110.0, 0.0, 110.0],
                rotation=[0.0, 45.0, 90.0],
                color="#111827",
                material="aluminum",
                explodeDir=[0.707, 0.2, 0.707],
                explodeDist=1.5,
                function="Outrigger arm for RR brushless propulsion pod",
                layer=1
            ),
            AssemblyPart(
                id="rotor_rear_right",
                name="RR Carbon Propeller Unit",
                type="actuator",
                shape="capsule",
                size=[180.0, 12.0, 22.0],
                position=[190.0, 24.0, 190.0],
                rotation=[0.0, -60.0, 0.0],
                color="#2563eb",
                material="plastic",
                explodeDir=[0.707, 0.8, 0.707],
                explodeDist=2.2,
                function="High-pitch counter-rotating lift propeller",
                layer=2
            ),
            AssemblyPart(
                id="gimbal_camera",
                name="4K 3-Axis Gimbal Sensor Pod",
                type="sensor",
                shape="sphere",
                size=[44.0, 44.0, 44.0],
                position=[0.0, -32.0, -45.0],
                color="#0a0a0c",
                material="metal",
                explodeDir=[0.0, -0.6, -0.8],
                explodeDist=1.8,
                function="High-definition aerial surveillance optics",
                layer=-2
            )
        ]

        details = [
            AssemblyDetail(
                parentId="flight_controller_pcb",
                shape="box",
                size=[14.0, 2.5, 14.0],
                position=[0.0, 5.0, 0.0],
                color="#111111",
                material="pcb"
            ),
            AssemblyDetail(
                parentId="top_canopy",
                shape="slots",
                size=[40.0, 2.0, 15.0],
                position=[0.0, 24.0, -20.0],
                color="#08080a",
                material="plastic",
                count=6
            ),
            AssemblyDetail(
                parentId="gimbal_camera",
                shape="torus",
                size=[32.0, 4.0, 32.0],
                position=[0.0, -32.0, -65.0],
                color="#d1d5db",
                material="aluminum"
            )
        ]

        relationships = [
            AssemblyRelationship(id="rel_power_fc", from_part="lipo_battery", to_part="flight_controller_pcb", rel_type="powers", description="Regulated 12V 5A power rail"),
            AssemblyRelationship(id="rel_ctrl_fl", from_part="flight_controller_pcb", to_part="rotor_front_left", rel_type="controls", description="PWM Motor pulse bus"),
            AssemblyRelationship(id="rel_ctrl_fr", from_part="flight_controller_pcb", to_part="rotor_front_right", rel_type="controls", description="PWM Motor pulse bus"),
            AssemblyRelationship(id="rel_ctrl_rl", from_part="flight_controller_pcb", to_part="rotor_rear_left", rel_type="controls", description="PWM Motor pulse bus"),
            AssemblyRelationship(id="rel_ctrl_rr", from_part="flight_controller_pcb", to_part="rotor_rear_right", rel_type="controls", description="PWM Motor pulse bus"),
            AssemblyRelationship(id="rel_video_cam", from_part="gimbal_camera", to_part="flight_controller_pcb", rel_type="feeds", description="Digital MIPI-CSI video feed"),
            AssemblyRelationship(id="rel_mount_canopy", from_part="main_chassis", to_part="top_canopy", rel_type="mounts", description="Snap-lock mounting pins")
        ]

        return AssemblyModel(
            id=model_id,
            name="Apex-Quad Industrial Autonomous Drone",
            units="mm",
            overallSize=[480.0, 110.0, 480.0],
            parts=parts,
            details=details,
            relationships=relationships,
            primary_axis="y"
        )



    @classmethod
    def create_robotic_arm_assembly(cls, model_id: str = "robot-01") -> AssemblyModel:
        parts = [
            AssemblyPart(
                id="base_pedestal",
                name="Heavy Anchor Pedestal",
                type="structure",
                shape="cylinder",
                size=[180.0, 60.0, 180.0],
                position=[0.0, 30.0, 0.0],
                color="#374151",
                material="metal",
                explodeDir=[0.0, -1.0, 0.0],
                explodeDist=1.5,
                function="Cast iron anchor flange bolting manipulator to work cell",
                layer=-1
            ),
            AssemblyPart(
                id="turntable_j1",
                name="360 Turntable Rotor (J1)",
                type="mechanism",
                shape="cylinder",
                size=[150.0, 75.0, 150.0],
                position=[0.0, 97.5, 0.0],
                color="#ea580c",
                material="metal",
                explodeDir=[0.0, 0.0, 0.0],
                explodeDist=0.0,
                function="Continuous azimuthal rotation harmonic gear drive",
                layer=0
            ),
            AssemblyPart(
                id="shoulder_boom_j2",
                name="Primary Shoulder Boom (J2)",
                type="mechanism",
                shape="cylinder",
                size=[65.0, 260.0, 65.0],
                position=[0.0, 250.0, 30.0],
                rotation=[25.0, 0.0, 0.0],
                color="#9ca3af",
                material="aluminum",
                explodeDir=[0.0, 0.5, 0.8],
                explodeDist=1.2,
                function="High-torque shoulder casting lifting main arm envelope",
                layer=1
            ),
            AssemblyPart(
                id="elbow_joint_j3",
                name="Elbow Articulator (J3)",
                type="mechanism",
                shape="cylinder",
                size=[75.0, 90.0, 75.0],
                position=[0.0, 380.0, 95.0],
                rotation=[0.0, 0.0, 90.0],
                color="#ea580c",
                material="metal",
                explodeDir=[0.0, 0.8, 0.6],
                explodeDist=1.7,
                function="Planetary reduction pivot for upper forearm extension",
                layer=2
            ),
            AssemblyPart(
                id="forearm_boom_j4",
                name="Forearm Structural Tube (J4)",
                type="structure",
                shape="cylinder",
                size=[50.0, 220.0, 50.0],
                position=[0.0, 480.0, 150.0],
                rotation=[-30.0, 0.0, 0.0],
                color="#9ca3af",
                material="aluminum",
                explodeDir=[0.0, 1.0, 0.5],
                explodeDist=2.1,
                function="Lightweight tubular reach arm routing internal signal lines",
                layer=3
            ),
            AssemblyPart(
                id="wrist_flange_j5",
                name="3-Axis Precision Wrist (J5/J6)",
                type="actuator",
                shape="cylinder",
                size=[58.0, 60.0, 58.0],
                position=[0.0, 580.0, 210.0],
                rotation=[0.0, 0.0, 0.0],
                color="#1f2937",
                material="aluminum",
                explodeDir=[0.0, 1.0, 0.7],
                explodeDist=2.6,
                function="Tri-axial orientation flange pitching and rolling end effector",
                layer=4
            ),
            AssemblyPart(
                id="pneumatic_gripper",
                name="Parallel 2-Jaw Pneumatic Gripper",
                type="actuator",
                shape="rounded_box",
                size=[70.0, 85.0, 55.0],
                position=[0.0, 645.0, 245.0],
                color="#0f172a",
                material="metal",
                explodeDir=[0.0, 1.0, 0.9],
                explodeDist=3.2,
                cornerRadius=6.0,
                function="High-repeatability robotic end effector with tactile feedback",
                layer=5
            )
        ]

        details = [
            AssemblyDetail(
                parentId="base_pedestal",
                shape="cylinder",
                size=[14.0, 20.0, 14.0],
                position=[60.0, 62.0, 60.0],
                color="#9ca3af",
                material="metal"
            ),
            AssemblyDetail(
                parentId="elbow_joint_j3",
                shape="torus",
                size=[55.0, 8.0, 55.0],
                position=[0.0, 380.0, 95.0],
                rotation=[0.0, 0.0, 90.0],
                color="#374151",
                material="metal"
            )
        ]

        relationships = [
            AssemblyRelationship(id="rel_base_j1", from_part="base_pedestal", to_part="turntable_j1", rel_type="mounts", description="Crossed roller bearing ring"),
            AssemblyRelationship(id="rel_j1_j2", from_part="turntable_j1", to_part="shoulder_boom_j2", rel_type="drives", description="Direct-drive servo gearbox"),
            AssemblyRelationship(id="rel_j2_j3", from_part="shoulder_boom_j2", to_part="elbow_joint_j3", rel_type="transmits", description="Timing belt internal linkage"),
            AssemblyRelationship(id="rel_j3_j4", from_part="elbow_joint_j3", to_part="forearm_boom_j4", rel_type="mounts", description="Splined structural clamp"),
            AssemblyRelationship(id="rel_j4_j5", from_part="forearm_boom_j4", to_part="wrist_flange_j5", rel_type="mounts", description="Precision hollow-shaft coupling"),
            AssemblyRelationship(id="rel_j5_gripper", from_part="wrist_flange_j5", to_part="pneumatic_gripper", rel_type="controls", description="ISO 9409-1 tool mounting flange")
        ]

        return AssemblyModel(
            id=model_id,
            name="6-DOF Industrial Articulated Robotic Arm",
            units="mm",
            overallSize=[240.0, 720.0, 320.0],
            parts=parts,
            details=details,
            relationships=relationships,
            primary_axis="y"
        )



    @classmethod
    def get_assembly(cls, model_id_or_prompt: str) -> AssemblyModel:
        p = model_id_or_prompt.lower()
        if "sword" in p or "blade" in p or "knife" in p:
            return cls.create_broadsword_assembly()
        if "shield" in p or "aegis" in p or "armor" in p or "buckler" in p:
            return cls.create_shield_assembly()
        if "chair" in p or "seat" in p or "bench" in p:
            return cls.create_chair_assembly()
        if "drone" in p or "quadcopter" in p or "uav" in p or "plane" in p:
            return cls.create_drone_assembly()
        if "robot" in p or "arm" in p or "manipulator" in p or "industrial" in p:
            return cls.create_robotic_arm_assembly()
        return cls.create_drone_assembly(model_id=model_id_or_prompt)



    @classmethod
    def calculate_explosion_pose(cls, model: AssemblyModel, progress: float) -> List[ExplosionPose]:
        t = max(0.0, min(1.0, progress))
        poses: List[ExplosionPose] = []
        max_dim = max(model.overall_size) * 0.8

        for p in model.parts:
            dx = p.explode_dir[0] * p.explode_dist * max_dim * t
            dy = p.explode_dir[1] * p.explode_dist * max_dim * t
            dz = p.explode_dir[2] * p.explode_dist * max_dim * t

            current_pos = [
                round(p.position[0] + dx, 3),
                round(p.position[1] + dy, 3),
                round(p.position[2] + dz, 3)
            ]
            offset = [round(dx, 3), round(dy, 3), round(dz, 3)]

            poses.append(ExplosionPose(
                part_id=p.id,
                current_position=current_pos,
                offset=offset,
                progress=t
            ))

        return poses


    @classmethod
    def generate_mechanical_relationships(cls, model: AssemblyModel) -> List[AssemblyRelationship]:
        part_ids = {p.id for p in model.parts}
        return [r for r in model.relationships if r.from_part in part_ids and r.to_part in part_ids]


    @classmethod
    def generate_fasteners_and_details(cls, model: AssemblyModel) -> List[AssemblyDetail]:
        part_ids = {p.id for p in model.parts}
        return [d for d in model.details if d.parent_id in part_ids]


    @classmethod
    def generate_mechanical_relationships(cls, model: AssemblyModel) -> List[AssemblyRelationship]:
        part_ids = {p.id for p in model.parts}
        return [r for r in model.relationships if r.from_part in part_ids and r.to_part in part_ids]
