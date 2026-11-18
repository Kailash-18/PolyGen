import os, tempfile, zipfile
from app.pipeline.usdz_exporter import USDZExporter

def test_usda_generation():
    usda = USDZExporter.generate_usda("TestModel", [[0,0,0],[1,0,0],[0,1,0]], [[0,1,2]])
    assert "#usda 1.0" in usda
    assert "UsdPreviewSurface" in usda

def test_usdz_package_creation():
    with tempfile.TemporaryDirectory() as tmpdir:
        p = os.path.join(tmpdir, "model.usdz")
        res = USDZExporter.create_usdz_package(p, "TestModel", [[0,0,0],[1,0,0],[0,1,0]], [[0,1,2]])
        assert os.path.exists(p)
        assert res["file_size_bytes"] > 0
