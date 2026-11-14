import pytest
import tempfile
from pathlib import Path
import trimesh
from app.pipeline.exporter import AssetExporter

def test_glb_obj_export():
    with tempfile.TemporaryDirectory() as tmp_dir:
        exporter = AssetExporter(output_root=Path(tmp_dir))
        box = trimesh.creation.box(extents=[1, 1, 1])
        info = exporter.export_asset(box, "test_box")

        assert Path(info["glb_path"]).exists()
        assert Path(info["obj_path"]).exists()
        assert info["glb_size_bytes"] > 0
        assert info["obj_size_bytes"] > 0

        meta_path = exporter.save_metadata("test_box", {"test": True})
        assert meta_path.exists()
