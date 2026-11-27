"""
Stage 3: Reflection Capture Rig & Localized Radiance Probes.
Calculates localized environment probes and box-projected parallax reflections.
"""

from typing import Tuple, Dict, Any, List, Optional
import numpy as np

class ReflectionCaptureRig:
    """Manages localized reflection capture positions within bounding volumes."""

    def __init__(self, probe_position: Tuple[float, float, float] = (0.0, 1.0, 0.0)):
        self.probe_position = np.array(probe_position, dtype=np.float32)

    def compute_reflection_ray(
        self,
        surface_point: np.ndarray,
        camera_point: np.ndarray,
        surface_normal: np.ndarray
    ) -> np.ndarray:
        """Calculates specular reflection vector R = V - 2*(V.N)*N."""
        view_dir = surface_point - camera_point
        view_norm = np.linalg.norm(view_dir)
        if view_norm < 1e-12:
            return np.array([0.0, 0.0, 1.0], dtype=np.float32)
        v = view_dir / view_norm

        n_norm = np.linalg.norm(surface_normal)
        n = surface_normal / max(n_norm, 1e-12)

        r = v - 2.0 * float(np.dot(v, n)) * n
        return r / max(np.linalg.norm(r), 1e-12)

    def apply_box_projection_parallax(
        self,
        world_pos: np.ndarray,
        reflection_ray: np.ndarray,
        box_min: np.ndarray,
        box_max: np.ndarray
    ) -> np.ndarray:
        """
        Calculates corrected reflection vector accounting for localized room boundaries.
        Prevents reflections appearing infinitely distant when inside a finite vault/dungeon.
        """
        # Ray-AABB intersection: t = (bound - pos) / ray
        denom = np.where(np.abs(reflection_ray) < 1e-6, 1e-6, reflection_ray)
        t_first = (box_max - world_pos) / denom
        t_second = (box_min - world_pos) / denom
        t_max = np.maximum(t_first, t_second)
        t = np.min(t_max)

        # Intersection point on box boundary
        intersection = world_pos + t * reflection_ray
        corrected_dir = intersection - self.probe_position
        c_norm = np.linalg.norm(corrected_dir)
        return corrected_dir / max(c_norm, 1e-12)
