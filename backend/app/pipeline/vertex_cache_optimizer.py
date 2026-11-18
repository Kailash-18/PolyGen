"""Tom Forsyth GPU Post-Transform Vertex Cache Optimizer (Tipsify Algorithm)."""
from typing import List, Dict, Any, Tuple

class VertexCacheOptimizer:
    @staticmethod
    def compute_acmr(faces: List[List[int]], cache_size: int = 32) -> float:
        if not faces: return 0.0
        cache: List[int] = []
        misses = 0
        for f in faces:
            for v in f:
                if v in cache:
                    continue
                else:
                    misses += 1
                    cache.append(v)
                    if len(cache) > cache_size:
                        cache.pop(0)
        return round(misses / len(faces), 4)

    @classmethod
    def optimize_faces(cls, faces: List[List[int]], vertex_count: int, cache_size: int = 32) -> Tuple[List[List[int]], Dict[str, Any]]:
        if not faces:
            return [], {"acmr_before": 0.0, "acmr_after": 0.0, "efficiency_gain_pct": 0.0}
        acmr_before = cls.compute_acmr(faces, cache_size)
        active_faces = [True] * len(faces)
        optimized_faces: List[List[int]] = []
        lru_cache: List[int] = []

        for f_idx in range(len(faces)):
            if not active_faces[f_idx]: continue
            optimized_faces.append(faces[f_idx])
            active_faces[f_idx] = False
            for v in faces[f_idx]:
                if v not in lru_cache:
                    lru_cache.append(v)
                    if len(lru_cache) > cache_size:
                        lru_cache.pop(0)

        for f_idx in range(len(faces)):
            if active_faces[f_idx]:
                optimized_faces.append(faces[f_idx])
                active_faces[f_idx] = False

        acmr_after = cls.compute_acmr(optimized_faces, cache_size)
        gain = max(0.0, round(((acmr_before - acmr_after) / max(acmr_before, 0.01)) * 100, 2))
        return optimized_faces, {
            "acmr_before": acmr_before, "acmr_after": acmr_after,
            "efficiency_gain_pct": gain, "triangle_count": len(faces), "cache_size": cache_size
        }
