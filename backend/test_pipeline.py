import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.pipeline.geometry import GeometryEngine
from app.pipeline.optimizer import MeshOptimizer
from app.pipeline.texture import TextureEngine
from app.pipeline.exporter import AssetExporter
from app.pipeline.assembly import AssemblyEngine
from app.pipeline.teardown import TeardownEngine
from app.pipeline.component_graph import ComponentGraph
from app.core.config import settings

def test_full_pipeline():
    print("=== PolyGen Pipeline Verification ===")
    geo = GeometryEngine()
    opt = MeshOptimizer(target_polycount=10000)
    tex = TextureEngine(resolution=256)
    exp = AssetExporter(output_root=settings.OUTPUTS_DIR)

    print("\n[Step 1] Synthesizing 3D Geometry from prompt...")
    mesh = geo.generate_mesh("A rusted medieval broadsword with glowing sapphire")
    print(f"-> Raw 3D mesh: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")

    print("\n[Step 2] Applying QEM Decimation & Topology Cleaning...")
    cleaned = opt.clean_and_repair(mesh)
    decimated, stats = opt.decimate(cleaned, target_faces=8000)
    print(f"-> Optimized mesh: {len(decimated.vertices)} vertices, {len(decimated.faces)} faces (Reduction: {stats['reduction_percentage']})")

    print("\n[Step 3] Computing Conformal UV Coordinates & PBR Textures...")
    uv_mesh = opt.compute_uv_unwrapping(decimated)
    pbr_maps = tex.synthesize_pbr_maps("broadsword", uv_mesh)
    textured_mesh = tex.apply_textures_to_mesh(uv_mesh, pbr_maps)
    print(f"-> PBR Textures synthesized: Albedo, Normal, Roughness, Metalness")

    print("\n[Step 4] Packaging to Binary GLB & Wavefront OBJ...")
    info = exp.export_asset(textured_mesh, "test_broadsword", pbr_maps=pbr_maps)
    print(f"-> Exported GLB: {info['glb_path']} ({info['glb_size_bytes']} bytes)")
    print(f"-> Exported OBJ: {info['obj_path']} ({info['obj_size_bytes']} bytes)")

    print("\n[Step 5] Kinematic 3D Assembly Decomposition & Exploded View Poses...")
    assembly = AssemblyEngine.create_broadsword_assembly("broadsword-assembly-01")
    poses = AssemblyEngine.calculate_explosion_pose(assembly, progress=0.75)
    print(f"-> Assembly Model: '{assembly.name}' ({len(assembly.parts)} parts, {len(assembly.relationships)} links)")
    print(f"-> Trajectory Poses calculated at 75% explosion for {len(poses)} components")

    print("\n[Step 6] Teardown Sequencing & Structural Dependency Graph...")
    teardown_steps = TeardownEngine.compute_teardown_sequence(assembly)
    graph = ComponentGraph(assembly)
    topo_order = graph.topological_sort()
    print(f"-> Generated {len(teardown_steps)} sequential teardown steps")
    print(f"-> Resolved mechanical dependency DAG order: {topo_order[:4]}...")

    print("\n[SUCCESS] PolyGen pipeline verification completed successfully!")

if __name__ == "__main__":
    test_full_pipeline()
