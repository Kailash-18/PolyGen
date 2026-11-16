"""
PolyGen - Bill of Materials (BOM) & Material Physical Analysis Engine
Provides material registries, density lookup, volumetric mass calculation,
manufacturing process estimation, and assembly-level BOM synthesis.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class MaterialSpec(BaseModel):
    id: str
    name: str
    category: str = Field(..., description="metal, polymer, composite, ceramic, elastomer")
    density_g_cm3: float = Field(..., description="Density in grams per cubic centimeter")
    yield_strength_mpa: float = Field(..., description="Yield strength in MPa")
    thermal_conductivity_w_mk: float = Field(..., description="Thermal conductivity in W/(m*K)")
    cost_usd_per_kg: float = Field(..., description="Base raw material cost in USD per kilogram")

class PartBOMItem(BaseModel):
    part_id: str
    label: str
    material_id: str
    material_name: str
    volume_cm3: float
    mass_grams: float
    manufacturing_process: str
    unit_cost_usd: float
    source: str = "PolyGen Generative CAD Synthesis"

class AssemblyBOM(BaseModel):
    model_id: str
    title: str
    total_parts: int
    total_mass_grams: float
    total_cost_usd: float
    items: List[PartBOMItem]

MATERIAL_REGISTRY: Dict[str, MaterialSpec] = {
    "titanium_gr5": MaterialSpec(
        id="titanium_gr5",
        name="Titanium Ti-6Al-4V (Grade 5)",
        category="metal",
        density_g_cm3=4.43,
        yield_strength_mpa=880.0,
        thermal_conductivity_w_mk=6.7,
        cost_usd_per_kg=48.50
    ),
    "aluminum_7075": MaterialSpec(
        id="aluminum_7075",
        name="Aerospace Aluminum 7075-T6",
        category="metal",
        density_g_cm3=2.81,
        yield_strength_mpa=503.0,
        thermal_conductivity_w_mk=130.0,
        cost_usd_per_kg=12.80
    ),
    "aluminum_6061": MaterialSpec(
        id="aluminum_6061",
        name="Structural Aluminum 6061-T6",
        category="metal",
        density_g_cm3=2.70,
        yield_strength_mpa=276.0,
        thermal_conductivity_w_mk=167.0,
        cost_usd_per_kg=8.50
    ),
    "stainless_steel_316": MaterialSpec(
        id="stainless_steel_316",
        name="Marine-Grade Stainless Steel 316L",
        category="metal",
        density_g_cm3=8.00,
        yield_strength_mpa=290.0,
        thermal_conductivity_w_mk=16.3,
        cost_usd_per_kg=7.90
    ),
    "high_carbon_steel_1095": MaterialSpec(
        id="high_carbon_steel_1095",
        name="Hardened High-Carbon Steel 1095",
        category="metal",
        density_g_cm3=7.85,
        yield_strength_mpa=680.0,
        thermal_conductivity_w_mk=45.0,
        cost_usd_per_kg=6.40
    ),
    "brass_c360": MaterialSpec(
        id="brass_c360",
        name="Free-Cutting Brass C360",
        category="metal",
        density_g_cm3=8.50,
        yield_strength_mpa=310.0,
        thermal_conductivity_w_mk=115.0,
        cost_usd_per_kg=11.20
    ),
    "copper_c110": MaterialSpec(
        id="copper_c110",
        name="Electrolytic Tough Pitch Copper C110",
        category="metal",
        density_g_cm3=8.94,
        yield_strength_mpa=220.0,
        thermal_conductivity_w_mk=390.0,
        cost_usd_per_kg=14.50
    ),
    "carbon_fiber_twill_3k": MaterialSpec(
        id="carbon_fiber_twill_3k",
        name="3K Twill Carbon Fiber Composite / Epoxy",
        category="composite",
        density_g_cm3=1.55,
        yield_strength_mpa=600.0,
        thermal_conductivity_w_mk=5.0,
        cost_usd_per_kg=65.00
    ),
    "abs_plastic": MaterialSpec(
        id="abs_plastic",
        name="High-Impact Acrylonitrile Butadiene Styrene (ABS)",
        category="polymer",
        density_g_cm3=1.05,
        yield_strength_mpa=40.0,
        thermal_conductivity_w_mk=0.17,
        cost_usd_per_kg=3.40
    ),
    "polycarbonate": MaterialSpec(
        id="polycarbonate",
        name="Optical-Grade Polycarbonate (PC)",
        category="polymer",
        density_g_cm3=1.20,
        yield_strength_mpa=65.0,
        thermal_conductivity_w_mk=0.20,
        cost_usd_per_kg=4.80
    ),
    "delrin_acetal_pom": MaterialSpec(
        id="delrin_acetal_pom",
        name="Delrin POM-H Acetal Homopolymer",
        category="polymer",
        density_g_cm3=1.41,
        yield_strength_mpa=69.0,
        thermal_conductivity_w_mk=0.23,
        cost_usd_per_kg=5.90
    ),
    "silicone_rubber": MaterialSpec(
        id="silicone_rubber",
        name="High-Tear-Strength Silicone Elastomer",
        category="elastomer",
        density_g_cm3=1.15,
        yield_strength_mpa=8.5,
        thermal_conductivity_w_mk=0.20,
        cost_usd_per_kg=7.20
    ),
    "neodymium_n52": MaterialSpec(
        id="neodymium_n52",
        name="Sintered Neodymium Magnet NdFeB N52",
        category="metal",
        density_g_cm3=7.50,
        yield_strength_mpa=80.0,
        thermal_conductivity_w_mk=9.0,
        cost_usd_per_kg=82.00
    ),
    "fr4_pcb": MaterialSpec(
        id="fr4_pcb",
        name="Multi-Layer FR-4 Glass Epoxy Copper-Clad Laminate",
        category="composite",
        density_g_cm3=1.85,
        yield_strength_mpa=340.0,
        thermal_conductivity_w_mk=0.30,
        cost_usd_per_kg=24.00
    ),
    "lithium_polymer": MaterialSpec(
        id="lithium_polymer",
        name="LiPo High-Discharge Battery Cell Substrate",
        category="composite",
        density_g_cm3=2.10,
        yield_strength_mpa=15.0,
        thermal_conductivity_w_mk=1.2,
        cost_usd_per_kg=38.00
    )
}


def estimate_component_volume(
    dx_cm: float,
    dy_cm: float,
    dz_cm: float,
    geometry_type: str = "box",
    fill_factor: float = 0.65
) -> float:
    """
    Computes volumetric displacement in cm^3 from bounding box and shape type.
    """
    bounding_vol = max(0.001, dx_cm * dy_cm * dz_cm)
    factors = {
        "box": 0.85,
        "cylinder": 0.785,
        "sphere": 0.524,
        "cone": 0.333,
        "hollow_shell": 0.22,
        "sheet_metal": 0.12,
        "lattice_frame": 0.18,
        "pcb_board": 0.95,
        "wire_conduit": 0.40
    }
    effective_factor = factors.get(geometry_type.lower(), fill_factor)
    return round(bounding_vol * effective_factor, 2)

def calculate_part_mass(volume_cm3: float, material_id: str) -> float:
    """
    Calculates mass in grams = volume (cm^3) * density (g/cm^3).
    """
    mat = MATERIAL_REGISTRY.get(material_id, MATERIAL_REGISTRY["aluminum_6061"])
    mass = volume_cm3 * mat.density_g_cm3
    return round(mass, 2)

def estimate_part_specs(
    part_id: str,
    label: str,
    dimensions_cm: tuple[float, float, float],
    geometry_type: str = "box",
    preferred_material: Optional[str] = None
) -> Dict[str, Any]:
    """
    Infers material from part label semantics if not explicitly provided.
    """
    lbl = label.lower()
    mat_id = preferred_material
    if not mat_id:
        if any(k in lbl for k in ["blade", "tang", "steel", "cutter", "piston"]):
            mat_id = "high_carbon_steel_1095"
        elif any(k in lbl for k in ["pommel", "guard", "brass", "bushing"]):
            mat_id = "brass_c360"
        elif any(k in lbl for k in ["shield", "frame", "boom", "arm", "chassis"]):
            mat_id = "titanium_gr5" if "shield" in lbl or "boom" in lbl else "aluminum_7075"
        elif any(k in lbl for k in ["carbon", "rotor", "drone", "wing"]):
            mat_id = "carbon_fiber_twill_3k"
        elif any(k in lbl for k in ["pcb", "controller", "esc", "board"]):
            mat_id = "fr4_pcb"
        elif any(k in lbl for k in ["motor", "magnet", "stator"]):
            mat_id = "copper_c110"
        elif any(k in lbl for k in ["canopy", "lens", "visor", "window"]):
            mat_id = "polycarbonate"
        elif any(k in lbl for k in ["cover", "casing", "shell", "handle"]):
            mat_id = "abs_plastic"
        elif any(k in lbl for k in ["gear", "cam", "roller", "wheel"]):
            mat_id = "delrin_acetal_pom"
        elif any(k in lbl for k in ["grip", "cushion", "pad", "gasket", "seal"]):
            mat_id = "silicone_rubber"
        elif any(k in lbl for k in ["battery", "cell", "power"]):
            mat_id = "lithium_polymer"
        else:
            mat_id = "aluminum_6061"

    vol = estimate_component_volume(dimensions_cm[0], dimensions_cm[1], dimensions_cm[2], geometry_type)
    mass = calculate_part_mass(vol, mat_id)
    return {
        "material_id": mat_id,
        "material_name": MATERIAL_REGISTRY[mat_id].name,
        "volume_cm3": vol,
        "mass_grams": mass
    }


MANUFACTURING_PROCESSES: Dict[str, Dict[str, Any]] = {
    "cnc_milling_5axis": {
        "name": "5-Axis High-Precision CNC Milling",
        "machine_hourly_rate_usd": 68.0,
        "setup_cost_usd": 55.0,
        "finishing_per_part_usd": 4.50,
        "tolerance_mm": 0.015,
        "applicable_categories": ["metal", "polymer"]
    },
    "injection_molding": {
        "name": "High-Volume Precision Injection Molding",
        "machine_hourly_rate_usd": 22.0,
        "tooling_die_amortized_usd": 8.50,
        "finishing_per_part_usd": 0.80,
        "tolerance_mm": 0.05,
        "applicable_categories": ["polymer", "elastomer"]
    },
    "sls_3d_printing": {
        "name": "Direct Metal / Polymer Selective Laser Sintering (SLS)",
        "machine_hourly_rate_usd": 42.0,
        "setup_cost_usd": 15.0,
        "finishing_per_part_usd": 6.00,
        "tolerance_mm": 0.08,
        "applicable_categories": ["metal", "polymer", "composite"]
    },
    "sheet_metal_laser_stamping": {
        "name": "Fiber Laser Cutting & Progressive Stamping",
        "machine_hourly_rate_usd": 32.0,
        "setup_cost_usd": 25.0,
        "finishing_per_part_usd": 1.50,
        "tolerance_mm": 0.04,
        "applicable_categories": ["metal"]
    },
    "die_casting": {
        "name": "High-Pressure Die Casting (HPDC)",
        "machine_hourly_rate_usd": 28.0,
        "tooling_die_amortized_usd": 12.00,
        "finishing_per_part_usd": 2.20,
        "tolerance_mm": 0.05,
        "applicable_categories": ["metal"]
    },
    "pcb_smt_assembly": {
        "name": "Automated SMT Pick-and-Place & Reflow Soldering",
        "machine_hourly_rate_usd": 45.0,
        "setup_cost_usd": 20.0,
        "finishing_per_part_usd": 3.00,
        "tolerance_mm": 0.02,
        "applicable_categories": ["composite"]
    }
}

def estimate_manufacturing_cost(
    material_id: str,
    mass_grams: float,
    process: str,
    batch_size: int = 250
) -> Dict[str, float]:
    """
    Computes unit part cost factoring raw materials, machine runtime, tooling, and surface treatment.
    """
    mat = MATERIAL_REGISTRY.get(material_id, MATERIAL_REGISTRY["aluminum_6061"])
    proc = MANUFACTURING_PROCESSES.get(process, MANUFACTURING_PROCESSES["cnc_milling_5axis"])

    raw_material_cost = (mass_grams / 1000.0) * mat.cost_usd_per_kg * 1.15
    setup_amortized = proc.get("setup_cost_usd", 20.0) / max(1, batch_size)
    tooling_amortized = proc.get("tooling_die_amortized_usd", 0.0)
    cycle_time_hours = max(0.04, (mass_grams / 500.0) * 0.15)
    machine_cost = cycle_time_hours * proc["machine_hourly_rate_usd"]
    finishing_cost = proc.get("finishing_per_part_usd", 2.0)

    total_unit_cost = raw_material_cost + setup_amortized + tooling_amortized + machine_cost + finishing_cost

    return {
        "raw_material_cost_usd": round(raw_material_cost, 2),
        "setup_amortized_usd": round(setup_amortized, 2),
        "tooling_amortized_usd": round(tooling_amortized, 2),
        "machine_labor_cost_usd": round(machine_cost, 2),
        "finishing_cost_usd": round(finishing_cost, 2),
        "total_cost_usd": round(total_unit_cost, 2)
    }
