"""Rigid Body Physics Simulation and Center-of-Mass / Inertia Tensor Engine."""
import math
from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class RigidBodyProperties:
    mass_kg: float
    volume_m3: float
    center_of_mass: List[float]
    inertia_tensor: List[List[float]]
    principal_moments: List[float]
    stability_tipping_angle_deg: float
    is_stable: bool

class MeshPhysicsEvaluator:
    """Computes exact volumetric integrals for arbitrary triangular surface meshes."""
    @staticmethod
    def calculate_tetrahedron_properties(p0: List[float], p1: List[float], p2: List[float]) -> Tuple[float, List[float]]:
        v = (
            p0[0] * (p1[1] * p2[2] - p1[2] * p2[1])
            - p0[1] * (p1[0] * p2[2] - p1[2] * p2[0])
            + p0[2] * (p1[0] * p2[1] - p1[1] * p2[0])
        ) / 6.0
        centroid = [(p0[0] + p1[0] + p2[0]) * 0.25, (p0[1] + p1[1] + p2[1]) * 0.25, (p0[2] + p1[2] + p2[2]) * 0.25]
        return v, centroid
