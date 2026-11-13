import sys
from pathlib import Path

# Add backend directory to sys.path
sys.path.insert(0, str(Path(__file__).parent))

from app.pipeline.geometry import GeometryEngine
from app.pipeline.optimizer import MeshOptimizer
from app.pipeline.exporter import AssetExporter
from app.core.config import settings

def test_full_pipeline():
    print("=== PolyGen Pipeline Verification ===")
    geo = GeometryEngine()
    opt = MeshOptimizer(target_polycount=10000)
    exp = AssetExporter(output_root=settings.OUTPUTS_DIR)

    # 1. Geometry
    print("\n[Step 1] Synthesizing 3D Geometry from prompt...")
    mesh = geo.generate_mesh("A rusted medieval broadsword with glowing sapphire")
    print(f"-> Raw 3D mesh: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")

    # 2. Decimation
    print("\n[Step 2] Applying QEM Decimation & Topology Cleaning...")
    cleaned = opt.clean_and_repair(mesh)
    decimated, stats = opt.decimate(cleaned, target_faces=8000)
    print(f"-> Optimized mesh: {len(decimated.vertices)} vertices, {len(decimated.faces)} faces (Reduction: {stats['reduction_percentage']})")

    # 3. UV Unwrapping
    print("\n[Step 3] Computing Conformal UV Coordinates...")
    uv_mesh = opt.compute_uv_unwrapping(decimated)
    has_uv = hasattr(uv_mesh.visual, "uv") and uv_mesh.visual.uv is not None
    print(f"-> UV Coordinates mapped: {has_uv} ({len(uv_mesh.visual.uv)} UV points)")

    # 4. Packaging
    print("\n[Step 4] Packaging to Binary GLB & Wavefront OBJ...")
    info = exp.export_asset(uv_mesh, "test_broadsword")
    print(f"-> Exported GLB: {info['glb_path']} ({info['glb_size_bytes']} bytes)")
    print(f"-> Exported OBJ: {info['obj_path']} ({info['obj_size_bytes']} bytes)")
    print("\n[SUCCESS] PolyGen pipeline verification completed successfully!")

if __name__ == "__main__":
    test_full_pipeline()
