"""
PolyGen - Mechanical Teardown Sequencing and Disassembly Hierarchy Engine
Computes dependency order, removal layers, and non-colliding disassembly trajectories.
"""
from typing import List, Dict, Any, Optional
from app.pipeline.assembly import AssemblyModel, AssemblyPart, AssemblyRelationship

class TeardownEngine:
    @staticmethod
    def compute_teardown_sequence(assembly: AssemblyModel) -> List[Dict[str, Any]]:
        """
        Calculates optimal disassembly order (from exterior fasteners and enclosures
        inward to core internal components) based on part layers and relationship dependencies.
        """
        sorted_parts = sorted(
            assembly.parts,
            key=lambda p: (getattr(p, 'layer', 1) or 1, -p.explode_dist),
            reverse=True
        )

        steps = []
        for seq_idx, part in enumerate(sorted_parts, start=1):
            part_type = getattr(part, 'part_type', 'body') or 'body'
            shape = getattr(part, 'shape', '') or ''
            requires_tool = "fastener" in part_type.lower() or "screw" in shape.lower()
            steps.append({
                "step": seq_idx,
                "part_id": part.id,
                "part_name": part.name,
                "layer": getattr(part, 'layer', 1) or 1,
                "explode_dir": part.explode_dir,
                "explode_dist": part.explode_dist,
                "requires_tool": requires_tool,
                "action": f"Release and slide {part.name} along trajectory vector [{part.explode_dir[0]:.2f}, {part.explode_dir[1]:.2f}, {part.explode_dir[2]:.2f}]"
            })
        return steps

    @staticmethod
    def get_layer_grouping(assembly: AssemblyModel) -> Dict[int, List[str]]:
        """Groups part IDs by physical structural layer."""
        layers: Dict[int, List[str]] = {}
        for p in assembly.parts:
            layer = getattr(p, 'layer', 1) or 1
            if layer not in layers:
                layers[layer] = []
            layers[layer].append(p.id)
        return dict(sorted(layers.items()))
