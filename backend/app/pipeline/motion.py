"""
PolyGen - Advanced Kinematics & Helical Disassembly Motion Solver
Handles multi-stage rotational trajectories, fastener unscrewing,
spring-damper easing curves, and progressive mechanical layer clearances.
"""

from __future__ import annotations
import math
from typing import Any, Dict, List, Tuple
from pydantic import BaseModel, Field

class HelicalTrajectory(BaseModel):
    part_id: str
    rotation_axis: Tuple[float, float, float] = (0.0, 1.0, 0.0)
    pitch_mm: float = Field(default=2.5, description="Thread pitch: linear advance per full 360 deg turn")
    thread_turns: float = Field(default=4.0, description="Total turns required to clear engagement")
    axial_travel_mm: float = Field(default=25.0, description="Total linear travel along rotation axis")
    retract_speed_factor: float = Field(default=1.0, description="Multiplier for unscrew phase timing")

def calculate_helical_pose(
    progress: float,
    helix: HelicalTrajectory,
    initial_position: Tuple[float, float, float] = (0.0, 0.0, 0.0)
) -> Dict[str, Any]:
    """
    Computes exact 3D position and rotation for a threaded fastener or bayonet lock
    at normalized progress t in [0.0, 1.0].
    """
    t = max(0.0, min(1.0, progress))
    total_angle_rad = 2.0 * math.pi * helix.thread_turns * t
    linear_offset = helix.axial_travel_mm * t

    ux, uy, uz = helix.rotation_axis
    mag = math.sqrt(ux*ux + uy*uy + uz*uz) or 1.0
    ux, uy, uz = ux/mag, uy/mag, uz/mag

    pos = (
        round(initial_position[0] + ux * linear_offset, 3),
        round(initial_position[1] + uy * linear_offset, 3),
        round(initial_position[2] + uz * linear_offset, 3)
    )

    rot = (
        round(ux * total_angle_rad, 4),
        round(uy * total_angle_rad, 4),
        round(uz * total_angle_rad, 4)
    )

    return {
        "part_id": helix.part_id,
        "progress": t,
        "position": pos,
        "rotation_euler": rot,
        "turns_completed": round(helix.thread_turns * t, 2),
        "linear_travel_mm": round(linear_offset, 2)
    }
