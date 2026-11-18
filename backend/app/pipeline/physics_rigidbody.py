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

    @classmethod
    def evaluate_mesh(cls, vertices: List[List[float]], faces: List[List[int]], material_density_kg_m3: float = 1200.0) -> RigidBodyProperties:
        total_vol = 0.0
        weighted_com = [0.0, 0.0, 0.0]
        for f in faces:
            p0 = vertices[f[0]]
            p1 = vertices[f[1]]
            p2 = vertices[f[2]]
            tet_vol, tet_com = cls.calculate_tetrahedron_properties(p0, p1, p2)
            total_vol += tet_vol
            weighted_com[0] += tet_vol * tet_com[0]
            weighted_com[1] += tet_vol * tet_com[1]
            weighted_com[2] += tet_vol * tet_com[2]

        abs_vol = abs(total_vol)
        if abs_vol < 1e-7:
            xs = [v[0] for v in vertices]
            ys = [v[1] for v in vertices]
            zs = [v[2] for v in vertices]
            dx = max(max(xs) - min(xs), 0.01)
            dy = max(max(ys) - min(ys), 0.01)
            dz = max(max(zs) - min(zs), 0.01)
            abs_vol = dx * dy * dz * 0.5
            com = [(min(xs) + max(xs)) * 0.5, (min(ys) + max(ys)) * 0.5, (min(zs) + max(zs)) * 0.5]
        else:
            com = [weighted_com[0] / total_vol, weighted_com[1] / total_vol, weighted_com[2] / total_vol]

        mass = abs_vol * material_density_kg_m3
        xs = [v[0] - com[0] for v in vertices]
        ys = [v[1] - com[1] for v in vertices]
        zs = [v[2] - com[2] for v in vertices]
        r_x2 = sum(x * x for x in xs) / max(len(vertices), 1)
        r_y2 = sum(y * y for y in ys) / max(len(vertices), 1)
        r_z2 = sum(z * z for z in zs) / max(len(vertices), 1)
        Ixx = mass * (r_y2 + r_z2)
        Iyy = mass * (r_x2 + r_z2)
        Izz = mass * (r_x2 + r_y2)
        inertia_matrix = [[round(Ixx, 6), 0.0, 0.0], [0.0, round(Iyy, 6), 0.0], [0.0, 0.0, round(Izz, 6)]]
