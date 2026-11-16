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


def ease_in_out_cubic(t: float) -> float:
    """
    Cubic easing in/out curve for natural physical acceleration and deceleration.
    """
    clamped = max(0.0, min(1.0, t))
    if clamped < 0.5:
        return 4.0 * clamped * clamped * clamped
    p = 2.0 * clamped - 2.0
    return 0.5 * (p * p * p + 2.0)

def spring_damper_oscillation(
    t: float,
    damping_ratio: float = 0.65,
    natural_freq: float = 14.0
) -> float:
    """
    Simulates second-order underdamped harmonic settling motion at mechanical stop.
    """
    clamped = max(0.0, min(1.0, t))
    if clamped <= 0.0:
        return 0.0
    if clamped >= 1.0:
        return 1.0
    damped_freq = natural_freq * math.sqrt(max(0.01, 1.0 - damping_ratio * damping_ratio))
    decay = math.exp(-damping_ratio * natural_freq * clamped)
    osc = math.cos(damped_freq * clamped) + (damping_ratio / math.sqrt(1.0 - damping_ratio * damping_ratio)) * math.sin(damped_freq * clamped)
    return round(1.0 - decay * osc, 4)

def smoothstep(edge0: float, edge1: float, x: float) -> float:
    """
    Standard Hermite smoothstep interpolation between edge0 and edge1.
    """
    if edge1 <= edge0:
        return 1.0 if x >= edge1 else 0.0
    t = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return round(t * t * (3.0 - 2.0 * t), 4)

def damped_harmonic_wobble(t: float, amplitude: float = 0.08, decay: float = 6.0) -> float:
    """
    Transient vibrational wobble simulating elastic snap when parts detach.
    """
    clamped = max(0.0, min(1.0, t))
    return round(amplitude * math.exp(-decay * clamped) * math.sin(2.0 * math.pi * 3.5 * clamped), 4)


def calculate_progressive_layer_explosion(
    components: List[Dict[str, Any]],
    global_progress: float
) -> List[Dict[str, Any]]:
    """
    Calculates ordered, multi-stage explosion poses.
    Fasteners detach first, then shells, then mechanisms, then structural chassis.
    """
    p = max(0.0, min(1.0, global_progress))
    results = []

    layer_schedule = {
        "fastener": (0.00, 0.30),
        "cover": (0.15, 0.55),
        "mechanism": (0.35, 0.80),
        "sensor": (0.40, 0.85),
        "controller": (0.50, 0.90),
        "power_source": (0.55, 0.95),
        "structure": (0.65, 1.00),
        "chassis": (0.70, 1.00)
    }

    for comp in components:
        cid = comp.get("id", "part")
        ptype = comp.get("type", "structure")
        t_start, t_end = layer_schedule.get(ptype, (0.25, 0.85))

        local_t = 0.0
        if p > t_start:
            local_t = min(1.0, (p - t_start) / max(0.001, t_end - t_start))

        eased_t = ease_in_out_cubic(local_t)
        base_dir = comp.get("explosion_direction", [0.0, 1.0, 0.0])
        dist = comp.get("explosion_distance", 15.0)

        mag = math.sqrt(sum(x*x for x in base_dir)) or 1.0
        norm_dir = [x / mag for x in base_dir]

        pos = [
            round(norm_dir[0] * dist * eased_t, 3),
            round(norm_dir[1] * dist * eased_t, 3),
            round(norm_dir[2] * dist * eased_t, 3)
        ]

        results.append({
            "id": cid,
            "type": ptype,
            "local_progress": round(local_t, 3),
            "eased_factor": round(eased_t, 3),
            "offset": pos,
            "is_moving": 0.0 < local_t < 1.0,
            "is_settled": local_t >= 1.0
        })

    return results
