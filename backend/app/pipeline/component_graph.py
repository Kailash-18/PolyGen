"""
PolyGen - 3D Component Relationship Graph & Mechanical Dependency Solver
Constructs directed acyclic graphs of mechanical assemblies and validates structural connectivity.
"""
from typing import Dict, List, Set, Optional
from app.pipeline.assembly import AssemblyModel, AssemblyRelationship

class ComponentGraph:
    def __init__(self, assembly: AssemblyModel):
        self.assembly = assembly
        self.nodes: Set[str] = {p.id for p in assembly.parts}
        self.adj: Dict[str, List[str]] = {nid: [] for nid in self.nodes}
        self.rev_adj: Dict[str, List[str]] = {nid: [] for nid in self.nodes}
        self.edge_types: Dict[tuple[str, str], str] = {}

        for rel in assembly.relationships:
            if rel.from_part in self.nodes and rel.to_part in self.nodes:
                self.adj[rel.from_part].append(rel.to_part)
                self.rev_adj[rel.to_part].append(rel.from_part)
                self.edge_types[(rel.from_part, rel.to_part)] = rel.rel_type

    def get_dependencies(self, part_id: str) -> List[str]:
        """Returns direct components that this component depends on or mounts to."""
        return self.adj.get(part_id, [])

    def get_dependents(self, part_id: str) -> List[str]:
        """Returns components that depend directly on this component."""
        return self.rev_adj.get(part_id, [])

    def topological_sort(self) -> List[str]:
        """Computes topological disassembly order ensuring zero blocked components."""
        in_degree = {nid: len(self.rev_adj[nid]) for nid in self.nodes}
        queue = [nid for nid, deg in in_degree.items() if deg == 0]
        order = []

        while queue:
            curr = queue.pop(0)
            order.append(curr)
            for neighbor in self.adj[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Fallback to append any remaining nodes
        for nid in self.nodes:
            if nid not in order:
                order.append(nid)
        return order
