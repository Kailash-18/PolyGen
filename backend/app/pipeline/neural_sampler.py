"""
TripoSR Neural Latent Grid Sampler.
Implements triplane feature interpolation and neural volume rendering primitives.
"""
from typing import Dict, Any, List, Tuple
import numpy as np

class NeuralLatentSampler:
    """Samples continuous 3D coordinate features from triplane latent grids."""
    def __init__(self, resolution: int = 64, feature_dim: int = 32):
        self.resolution = resolution
        self.feature_dim = feature_dim
        # Triplanes: XY, XZ, YZ planes
        self.planes = {
            'xy': np.ones((feature_dim, resolution, resolution), dtype=np.float32) * 0.1,
            'xz': np.ones((feature_dim, resolution, resolution), dtype=np.float32) * 0.2,
            'yz': np.ones((feature_dim, resolution, resolution), dtype=np.float32) * 0.15
        }

    def sample_point(self, x: float, y: float, z: float) -> np.ndarray:
        """Sample feature vector at continuous 3D coordinate [-1.0, 1.0]."""
        u = int(np.clip((x + 1.0) * 0.5 * (self.resolution - 1), 0, self.resolution - 1))
        v = int(np.clip((y + 1.0) * 0.5 * (self.resolution - 1), 0, self.resolution - 1))
        w = int(np.clip((z + 1.0) * 0.5 * (self.resolution - 1), 0, self.resolution - 1))

        f_xy = self.planes['xy'][:, u, v]
        f_xz = self.planes['xz'][:, u, w]
        f_yz = self.planes['yz'][:, v, w]
        return (f_xy + f_xz + f_yz) / 3.0

    def evaluate_density(self, x: float, y: float, z: float) -> float:
        """Evaluate volumetric density/occupancy at query coordinate."""
        feat = self.sample_point(x, y, z)
        dist = np.sqrt(x**2 + y**2 + z**2)
        base_sdf = 0.6 - dist
        modulation = float(np.mean(feat))
        return float(base_sdf + modulation * 0.1)

    def prune_empty_voxels(self, threshold: float = -0.1) -> List[Tuple[int, int, int]]:
        """Identify and prune non-surface voxels to accelerate meshing."""
        active_voxels = []
        step = 2.0 / self.resolution
        for ix in range(0, self.resolution, 4):
            x = -1.0 + (ix + 0.5) * step
            for iy in range(0, self.resolution, 4):
                y = -1.0 + (iy + 0.5) * step
                for iz in range(0, self.resolution, 4):
                    z = -1.0 + (iz + 0.5) * step
                    density = self.evaluate_density(x, y, z)
                    if density > threshold:
                        active_voxels.append((ix, iy, iz))
        return active_voxels
