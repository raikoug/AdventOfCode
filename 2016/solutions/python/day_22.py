from starter import AOC, CURRENT_YEAR
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Set, Tuple, Optional
from collections import deque

CURRENT_DAY = int(Path(__file__).stem.replace('day_', ''))
aoc = AOC(CURRENT_YEAR)

# Filesystem              Size  Used  Avail  Use%
# /dev/grid/node-x0-y0     90T   69T    21T   76%
@dataclass
class Node:
    path: Path
    x: int
    y: int
    size: int
    used: int
    avail: int
    use: int
    adjacent_nodes: List['Node']

    @staticmethod
    def from_txt_line(line: str) -> 'Node':
        parts = line.split()
        p = Path(parts[0])
        x = int(p.name.split("-")[1][1:])
        y = int(p.name.split("-")[2][1:])
        size = int(parts[1][:-1])
        used = int(parts[2][:-1])
        avail = int(parts[3][:-1])
        use = int(parts[4][:-1])

        return Node(p, x, y, size, used, avail, use, [])

    def add_adjacent_node(self, node: 'Node') -> None:
        self.adjacent_nodes.append(node)

    def is_me(self, other: 'Node') -> bool:
        return self.path == other.path

    def is_adjacent_node(self, other: 'Node') -> bool:
        # Nodes are adjacent if they are directly up, down, left, or right
        return (
            ((abs(self.x - other.x) == 1 and self.y == other.y) or
             (abs(self.y - other.y) == 1 and self.x == other.x))
            and not self.is_me(other)
        )

    def can_fit(self, other: 'Node') -> bool:
        # Node A (self) is not empty (its Used is not zero).
        # Nodes A and B (other) are not the same node.
        # The data on node A (its Used) would fit on node B (its Avail).
        return (self.used != 0) and (not self.is_me(other)) and (self.used <= other.avail)

    def __str__(self):
        return f"""Path: {self.path}
    x: {self.x}
    y: {self.y}
    size: {self.size}
    used: {self.used}
    avail: {self.avail}
    use: {self.use}
    adjacent_nodes: {[other.path for other in self.adjacent_nodes]}"""

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self):
        return hash(self.path)

    def __format__(self, format_spec: str) -> str:
        return str(self)


def solve_1(test_string: Optional[str] = None) -> int:
    inputs_1: str = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    nodes: List[Node] = []
    viable_pairs: List[Tuple[Node, Node]] = []

    # Parse the input lines and create Node instances
    for line in [line for line in inputs_1.splitlines() if "/dev/" in line]:
        nodes.append(Node.from_txt_line(line))

    # Build adjacency lists for nodes
    for node in nodes:
        for other in nodes:
            if node.is_adjacent_node(other):
                node.add_adjacent_node(other)

    # Find all viable pairs
    for node in nodes:
        for other in nodes:
            if node.can_fit(other):
                viable_pairs.append((node, other))

    return len(viable_pairs)


def solve_2(test_string: Optional[str] = None) -> int:
    inputs_1: str = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    nodes: List[Node] = []

    # Parse the input lines and create Node instances
    for line in [line for line in inputs_1.splitlines() if "/dev/" in line]:
        nodes.append(Node.from_txt_line(line))

    # Build a grid of nodes for easy access
    grid: Dict[Tuple[int, int], Node] = {}
    max_x: int = max(node.x for node in nodes)
    max_y: int = max(node.y for node in nodes)

    for node in nodes:
        grid[(node.x, node.y)] = node

    # Update adjacency lists using the corrected is_adjacent_node method
    for node in nodes:
        node.adjacent_nodes = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx: int = node.x + dx
            ny: int = node.y + dy
            if (nx, ny) in grid:
                neighbor: Node = grid[(nx, ny)]
                node.add_adjacent_node(neighbor)

    # Identify walls (nodes that are too big to move through)
    wall_threshold: int = 100  # Adjust threshold as necessary
    walls: Set[Tuple[int, int]] = {
        (node.x, node.y) for node in nodes if node.used > wall_threshold
    }

    # Find the empty node
    empty_node: Optional[Node] = next((node for node in nodes if node.used == 0), None)
    if empty_node is None:
        raise ValueError("Empty node not found")

    # Define the goal data position (top-right corner)
    goal_data_pos: Tuple[int, int] = (max_x, 0)

    # Find positions adjacent to the goal data
    targets: Set[Tuple[int, int]] = set()
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx: int = goal_data_pos[0] + dx
        ny: int = goal_data_pos[1] + dy
        if 0 <= nx <= max_x and 0 <= ny <= max_y and (nx, ny) not in walls:
            targets.add((nx, ny))

    # Use BFS to find the shortest path from the empty node to a target position
    visited: Set[Tuple[int, int]] = set()
    queue: deque[Tuple[int, int, int]] = deque()
    queue.append((empty_node.x, empty_node.y, 0))
    visited.add((empty_node.x, empty_node.y))

    initial_steps: Optional[int] = None
    while queue:
        x, y, steps = queue.popleft()
        if (x, y) in targets:
            initial_steps = steps
            break
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx: int = x + dx
            ny: int = y + dy
            if (0 <= nx <= max_x and 0 <= ny <= max_y and
                (nx, ny) not in walls and (nx, ny) not in visited):
                visited.add((nx, ny))
                queue.append((nx, ny, steps + 1))

    if initial_steps is None:
        raise ValueError("No path found from empty node to goal data.")

    # Calculate total steps required
    total_steps: int = initial_steps + (goal_data_pos[0] - 1) * 5 + 1

    return total_steps


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
