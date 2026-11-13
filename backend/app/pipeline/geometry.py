"""
Stage 1: Geometry Generation Engine (TripoSR / Shap-E / Mesh Synthesis)
"""

import math
import numpy as np
import trimesh
from app.core.device import detect_compute_device
from app.core.config import settings

class GeometryEngine:
    def __init__(self, device: str = "auto", enable_neural: bool = False):
        self.device_info = detect_compute_device(device)
        self.device = self.device_info["device"]
        self.enable_neural = enable_neural
        self.model = None
        if self.enable_neural and not settings.MOCK_3D_AI:
            self._load_lrm_weights()
        print(f"[GeometryEngine] Initialized on device: {self.device}")

    def _load_lrm_weights(self):
        try:
            import torch
            self.model = "LRM_weights_ready"
        except Exception:
            self.model = None
