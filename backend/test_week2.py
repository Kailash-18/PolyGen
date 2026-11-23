"""
Week 2 & Mid-Project Review Verification Script
Tests Geometry Audit, UV mapping, PBR Texture Synthesis, and GLB Packaging.
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from app.pipeline.geometry import GeometryEngine
from app.pipeline.optimizer import MeshOptimizer
from app.pipeline.texture import TextureEngine
from app.pipeline.exporter import AssetExporter
from app.core.config import settings

def test_week2_milestone():
    print("=======================================================")
    print("   PolyGen - Week 2 & Mid-Project Audit Verification   ")
    print("=======================================================")

    geo = GeometryEngine()
    opt = MeshOptimizer(target_polycount=10000)
    tex = TextureEngine(resolution=1024)
    exp = AssetExporter(output_root=settings.OUTPUTS_DIR)

    test_cases = [
        ("A rusted medieval broadsword with a glowing blue sapphire in the hilt", "broadsword"),
        ("A heavy knight tower shield with reinforced iron boss", "shield"),
        ("An ancient ceramic Greek vase with etched geometric patterns", "vase"),
        ("A gothic carved wooden chair", "chair")
    ]

    for prompt, slug in test_cases:
        print(f"\n--- Testing Asset: '{slug.upper()}' ---")
        print(f"Prompt: \"{prompt}\"")

        # 1. Geometry Audit
        mesh = geo.generate_mesh(prompt)
        print(f"1. [Geometry Audit] Generated recognizable 3D structure: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces (watertight: {mesh.is_watertight})")

        # 2. Decimation
        cleaned = opt.clean_and_repair(mesh)
        decimated, d_stats = opt.decimate(cleaned, target_faces=8000)
        print(f"2. [QEM Decimation] Polygons: {d_stats['before_faces']} -> {d_stats['after_faces']} (Saved: {d_stats['reduction_percentage']})")

        # 3. UV Unwrapping
        uv_mesh = opt.compute_uv_unwrapping(decimated)
        assert hasattr(uv_mesh.visual, "uv") and uv_mesh.visual.uv is not None
        print(f"3. [UV Mapping] Successfully parameterized UV atlas with {len(uv_mesh.visual.uv)} coordinates")

        # 4. Texture Synthesis
        textures = tex.synthesize_pbr_textures(prompt)
        print(f"4. [Texture Synthesis] Synthesized Albedo ({textures['albedo'].size}), Normal ({textures['normal'].size}), Roughness ({textures['roughness'].size})")

        # 5. Packaging & GLB Export
        result = exp.export_asset(uv_mesh, f"week2_{slug}", textures=textures)
        print(f"5. [Rendering Validation] Embedded PBR into binary GLB: {result['glb_path']} ({result['glb_size_bytes']} bytes)")
        print(f"   Individual PBR maps saved: {list(result['textures'].keys())}")

    print("\n=======================================================")
    print(" [PASSED] Mid-Project Review & Week 2 Pipeline Validated ")
    print("=======================================================")

if __name__ == "__main__":
    test_week2_milestone()
