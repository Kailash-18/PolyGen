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
