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


