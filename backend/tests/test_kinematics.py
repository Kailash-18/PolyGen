"""
Unit tests for PolyGen Advanced Kinematics & Disassembly Motion Solver
"""
from app.pipeline.motion import (
    HelicalTrajectory,
    calculate_helical_pose,
    ease_in_out_cubic,
    spring_damper_oscillation,
    smoothstep,
    calculate_progressive_layer_explosion
)

def test_helical_trajectory_calculation():
    helix = HelicalTrajectory(
        part_id="screw_m4",
        rotation_axis=(0.0, 1.0, 0.0),
        pitch_mm=2.0,
        thread_turns=3.0,
        axial_travel_mm=15.0
    )
    pose_mid = calculate_helical_pose(0.5, helix)
    assert pose_mid["turns_completed"] == 1.5
    assert pose_mid["linear_travel_mm"] == 7.5
    assert pose_mid["position"][1] == 7.5

def test_ease_in_out_cubic():
    assert ease_in_out_cubic(0.0) == 0.0
    assert ease_in_out_cubic(0.5) == 0.5
    assert ease_in_out_cubic(1.0) == 1.0
    assert ease_in_out_cubic(0.2) < 0.2

def test_spring_damper_oscillation():
    assert spring_damper_oscillation(0.0) == 0.0
    val_1 = spring_damper_oscillation(1.0)
    assert val_1 == 1.0

def test_smoothstep_interpolation():
    assert smoothstep(0.0, 1.0, 0.0) == 0.0
    assert smoothstep(0.0, 1.0, 1.0) == 1.0
    assert smoothstep(0.0, 1.0, 0.5) == 0.5

def test_progressive_layer_explosion_ordering():
    components = [
        {"id": "p_fastener", "type": "fastener", "explosion_direction": [0, 1, 0], "explosion_distance": 20.0},
        {"id": "p_shell", "type": "cover", "explosion_direction": [1, 0, 0], "explosion_distance": 30.0},
        {"id": "p_core", "type": "chassis", "explosion_direction": [0, 0, 1], "explosion_distance": 10.0}
    ]
    poses_early = calculate_progressive_layer_explosion(components, 0.25)
    f_early = next(p for p in poses_early if p["id"] == "p_fastener")
    c_early = next(p for p in poses_early if p["id"] == "p_core")
    assert f_early["local_progress"] > c_early["local_progress"]
