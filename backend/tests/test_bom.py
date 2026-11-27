"""
Unit tests for PolyGen Bill of Materials (BOM) & Physical Properties Engine
"""
from app.pipeline.bom import (
    MATERIAL_REGISTRY,
    estimate_component_volume,
    calculate_part_mass,
    estimate_manufacturing_cost,
    generate_assembly_bom,
    list_available_boms
)

def test_material_registry_lookup():
    assert "titanium_gr5" in MATERIAL_REGISTRY
    assert "aluminum_7075" in MATERIAL_REGISTRY
    assert "carbon_fiber_twill_3k" in MATERIAL_REGISTRY
    assert MATERIAL_REGISTRY["titanium_gr5"].density_g_cm3 == 4.43
    assert MATERIAL_REGISTRY["carbon_fiber_twill_3k"].yield_strength_mpa == 600.0

def test_estimate_component_volume():
    vol_box = estimate_component_volume(10.0, 5.0, 2.0, "box")
    assert vol_box == 85.0
    vol_cyl = estimate_component_volume(4.0, 4.0, 10.0, "cylinder")
    assert vol_cyl == 125.6

def test_calculate_part_mass():
    mass = calculate_part_mass(100.0, "titanium_gr5")
    assert mass == 443.0

def test_estimate_manufacturing_cost():
    cost_data = estimate_manufacturing_cost("aluminum_7075", mass_grams=350.0, process="cnc_milling_5axis", batch_size=250)
    assert "total_cost_usd" in cost_data
    assert cost_data["total_cost_usd"] > 0.0
    assert cost_data["raw_material_cost_usd"] > 0.0

def test_generate_assembly_bom_drone():
    bom = generate_assembly_bom("apex_quad_drone")
    assert bom.model_id == "drone"
    assert bom.total_parts == 7
    assert bom.total_mass_grams > 0.0
    assert bom.total_cost_usd > 0.0
    assert len(bom.items) == 7

def test_generate_assembly_bom_broadsword():
    bom = generate_assembly_bom("cybernetic_broadsword")
    assert bom.model_id == "broadsword"
    assert bom.total_parts == 7
    assert len(bom.items) == 7

def test_list_available_boms():
    boms = list_available_boms()
    assert len(boms) >= 5
    ids = [b["model_id"] for b in boms]
    assert "broadsword" in ids
    assert "drone" in ids
