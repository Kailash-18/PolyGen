"""
Stage 1: Geometry Generation Engine (TripoSR / Shap-E / Mesh Synthesis)
"""

import math
import numpy as np
import trimesh
from app.core.device import detect_compute_device

class GeometryEngine:
    def __init__(self, device: str = "auto"):
        self.device_info = detect_compute_device(device)
        self.device = self.device_info["device"]
        self.model = None
        print(f"[GeometryEngine] Initialized on device: {self.device}")
