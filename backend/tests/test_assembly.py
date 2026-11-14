"""
Unit tests for PolyGen 3D Assembly Engine & Kinematics Decomposer
"""
import pytest
from app.pipeline.assembly import AssemblyEngine, AssemblyModel, AssemblyPart

def test_drone_assembly_structure():
    drone = AssemblyEngine.create_drone_assembly("drone-test")
    assert drone.id == "drone-test"
    assert len(drone.parts) >= 12
    assert len(drone.relationships) >= 5
    assert len(drone.details) >= 2
    assert drone.primary_axis == "y"

    part_ids = [p.id for p in drone.parts]
    assert "main_chassis" in part_ids
    assert "flight_controller_pcb" in part_ids
    assert "lipo_battery" in part_ids
    assert "rotor_front_left" in part_ids

def test_broadsword_assembly_structure():
    sword = AssemblyEngine.create_broadsword_assembly("sword-test")
    assert sword.id == "sword-test"
    assert len(sword.parts) >= 5
    assert any(p.material == "metal" for p in sword.parts)
    assert any(p.material == "glass" for p in sword.parts)

def test_shield_assembly_structure():
    shield = AssemblyEngine.create_shield_assembly("shield-test")
    assert shield.id == "shield-test"
    assert len(shield.parts) >= 5
    assert shield.primary_axis == "z"

def test_chair_assembly_structure():
    chair = AssemblyEngine.create_chair_assembly("chair-test")
    assert chair.id == "chair-test"
    assert len(chair.parts) >= 8

def test_robotic_arm_structure():
    arm = AssemblyEngine.create_robotic_arm_assembly("arm-test")
    assert arm.id == "arm-test"
    assert len(arm.parts) >= 6
