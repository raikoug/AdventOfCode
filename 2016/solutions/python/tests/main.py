from __future__ import annotations
from typing import List, Tuple, Set, Dict
from collections import deque
import re

# Node data class to hold the node's properties
class Node:
    def __init__(self, x: int, y: int, size: int, used: int, avail: int):
        self.x: int = x
        self.y: int = y
        self.size: int = size
        self.used: int = used
        self.avail: int = avail

# Function to parse the input and create the grid of nodes
def parse_input(input_lines: List[str]) -> Tuple[Dict[Tuple[int, int], Node], int, int]:
    nodes: Dict[Tuple[int, int], Node] = {}
    max_x: int = 0
    max_y: int = 0
    pattern = re.compile(r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T")
    for line in input_lines:
        match = pattern.match(line)
        if match:
            x, y, size, used, avail = map(int, match.groups())
            nodes[(x, y)] = Node(x, y, size, used, avail)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
    return nodes, max_x, max_y

# Function to find the shortest path from the empty node to the goal data
def bfs(grid: Dict[Tuple[int, int], Node], start: Tuple[int, int], targets: Set[Tuple[int, int]], walls: Set[Tuple[int, int]], max_x: int, max_y: int) -> int:
    queue: deque[Tuple[Tuple[int, int], int]] = deque()
    queue.append((start, 0))
    visited: Set[Tuple[int, int]] = set()
    visited.add(start)

    while queue:
        (x, y), steps = queue.popleft()
        if (x, y) in targets:
            return steps
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx: int = x + dx
            ny: int = y + dy
            if 0 <= nx <= max_x and 0 <= ny <= max_y and (nx, ny) not in walls and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), steps + 1))
    return -1  # No path found

# Main function to solve the problem
def solve_part_two(input_lines: List[str]) -> int:
    nodes, max_x, max_y = parse_input(input_lines)

    # Identify the walls (nodes that are too big to traverse)
    walls: Set[Tuple[int, int]] = set()
    for (x, y), node in nodes.items():
        if node.used > 100:  # Threshold can be adjusted based on the data
            walls.add((x, y))

    # Find the empty node
    for (x, y), node in nodes.items():
        if node.used == 0:
            empty_node_pos: Tuple[int, int] = (x, y)
            break

    # Goal data position
    goal_data_pos: Tuple[int, int] = (max_x, 0)

    # Positions adjacent to the goal data
    targets: Set[Tuple[int, int]] = set()
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx: int = goal_data_pos[0] + dx
        ny: int = goal_data_pos[1] + dy
        if 0 <= nx <= max_x and 0 <= ny <= max_y and (nx, ny) not in walls:
            targets.add((nx, ny))

    # Compute the initial steps to get the empty node adjacent to the goal data
    initial_steps: int = bfs(nodes, empty_node_pos, targets, walls, max_x, max_y)

    if initial_steps == -1:
        raise ValueError("No path found from empty node to goal data.")

    # Total steps calculation:
    # initial_steps: Steps to get empty node next to goal data
    # (goal_data_pos[0] - 1): Number of times we need to move the goal data left
    # Each move requires 5 steps except the last one, which requires only 1 step
    total_steps: int = initial_steps + (goal_data_pos[0] - 1) * 5 + 1

    return total_steps

# Example usage:
if __name__ == "__main__":
    # Read the input data
    with open("/home/raikoug/SyncThing/SharedCodeTest/adventOfCode/2016/inputs/day_22/input_1.txt") as f:
        input_lines = f.readlines()

    result = solve_part_two(input_lines)
    print(f"The fewest number of steps required to move the goal data to node-x0-y0 is: {result}")
