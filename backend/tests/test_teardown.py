import pytest
from app.pipeline.assembly import AssemblyEngine
from app.pipeline.teardown import TeardownEngine
from app.pipeline.component_graph import ComponentGraph

def test_teardown_sequence_generation():
    drone = AssemblyEngine.create_drone_assembly()
    sequence = TeardownEngine.compute_teardown_sequence(drone)
    assert len(sequence) == len(drone.parts)
    assert sequence[0]["step"] == 1
    assert "explode_dir" in sequence[0]
    assert "action" in sequence[0]

def test_teardown_layer_grouping():
    drone = AssemblyEngine.create_drone_assembly()
    grouping = TeardownEngine.get_layer_grouping(drone)
    assert len(grouping) >= 3
    total_parts = sum(len(parts) for parts in grouping.values())
    assert total_parts == len(drone.parts)

def test_component_graph_dependencies():
    broadsword = AssemblyEngine.create_broadsword_assembly()
    graph = ComponentGraph(broadsword)
    assert len(graph.nodes) == len(broadsword.parts)
    order = graph.topological_sort()
    assert len(order) == len(broadsword.parts)
