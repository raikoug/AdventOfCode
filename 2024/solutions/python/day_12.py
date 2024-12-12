from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional, Self, Set
from dataclasses import dataclass, field
from queue import PriorityQueue
from collections import defaultdict

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)


@dataclass
class Point:
    row: int
    col: int
    char: str
    
    def __hash__(self):
        return self.row*1000000+self.col
    
    def __eq__(self, other: Self):
        return (self.row == other.row) and (self.col == other.col)
    
    def __lt__(self, other: Self):
        return (self.row < other.row) and (self.col < other.col)
    
    def __gt__(self, other: Self):
        return (self.row > other.row) and (self.col > other.col)
    
    def __lt__(self, other: Self):
        return (self.row <= other.row) and (self.col <= other.col)
    
    def __gt__(self, other: Self):
        return (self.row >= other.row) and (self.col >= other.col)
    

def list_neighbors(grid,point: Point):
    row = point.row
    col = point.col
    res: List[Point] = list()
    
    if row > 0:
        # UP
        res.append(Point(row-1,col,grid[row-1][col]))
    if col < (len(grid[0]) -1):
        # RIGHT
        res.append(Point(row,col+1,grid[row][col+1]))
    if row < (len(grid) -1):
        # DOWN
        res.append(Point(row+1,col,grid[row+1][col]))
    if col > 0:
        # LEFT
        res.append(Point(row,col-1,grid[row][col-1]))
    return res

def get_first_non_visited(grid: List[List[int]], visited: List[Point]):
    for row,line in enumerate(grid):
        for col,char in enumerate(line):
            point = Point(row, col, char)
            if point not in visited:
                return point

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    grid = inputs_1.splitlines()
    
    current_point = Point(0,0, grid[0][0])
    current_area: List[Point] = list()
    current_area.append(current_point)
    visited: Set[Point] = set()
    q = PriorityQueue()
    q.put([current_point,current_area])
    current_fences = 0  
    total = 0
    max_visited = len(grid)*len(grid[0])
    
    while len(visited) < max_visited:
        current_point: Point
        current_point,current_area = q.get()
        
        visited.add(current_point)
        
        neighbors = list_neighbors(grid,current_point)
        current_fences += 4 - len(neighbors)
        
        for neighbor in neighbors:
            if neighbor.char != current_point.char:
                current_fences += 1
                continue
            
            if neighbor in current_area:
                continue
            
            if neighbor.char == current_point.char:
                current_area.append(neighbor)
                q.put([neighbor,current_area])
        
        if q.empty():
            # Completed area, calculations!
            total += current_fences * len(current_area)
            current_fences = 0
            current_area.clear()
            
            # find a new starting point!
            current_point = get_first_non_visited(grid,visited)
            current_area.append(current_point)
            q.put([current_point,current_area])
        
        print(f"Percentuale di completamento: {((len(visited)/max_visited)*100):0.2f}%",end="\r")
    
    print()
    return total

def count_sides_of(area: List[Point]) -> int:
    reg = {(p.row, p.col) for p in area}

    left = set()
    right = set()
    up = set()
    down = set()
    
    for (r, c) in reg:
        if (r - 1, c) not in reg:
            up.add((r, c))
        if (r + 1, c) not in reg:
            down.add((r, c))
        if (r, c + 1) not in reg:
            right.add((r, c))
        if (r, c - 1) not in reg:
            left.add((r, c))

    corners = 0
    # upper corners
    for (r, c) in up:
        if (r, c) in left:
            corners += 1
        if (r, c) in right:
            corners += 1
        if (r - 1, c - 1) in right and (r, c) not in left:
            corners += 1
        if (r - 1, c + 1) in left and (r, c) not in right:
            corners += 1

    # lower corners
    for (r, c) in down:
        if (r, c) in left:
            corners += 1
        if (r, c) in right:
            corners += 1
        if (r + 1, c - 1) in right and (r, c) not in left:
            corners += 1
        if (r + 1, c + 1) in left and (r, c) not in right:
            corners += 1

    return corners
    
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    grid = inputs_1.splitlines()
    
    current_point = Point(0,0, grid[0][0])
    current_area: List[Point] = list()
    current_area.append(current_point)
    visited: Set[Point] = set()
    q = PriorityQueue()
    q.put([current_point,current_area])
    current_fences = 0  
    total = 0
    max_visited = len(grid)*len(grid[0])
    
    while len(visited) < max_visited:
        current_point: Point
        current_point,current_area = q.get()
        
        visited.add(current_point)
        
        neighbors = list_neighbors(grid,current_point)
        current_fences += 4 - len(neighbors)
        
        for neighbor in neighbors:
            if neighbor.char != current_point.char:
                current_fences += 1
                continue
            
            if neighbor in current_area:
                continue
            
            if neighbor.char == current_point.char:
                current_area.append(neighbor)
                q.put([neighbor,current_area])
        
        if q.empty():
            # Completed area, calculations!
            # Calculate the sides of the area
            total += count_sides_of(current_area) * len(current_area)
            
            # reset for next area
            current_fences = 0
            current_area.clear()
            
            # find a new starting point!
            current_point = get_first_non_visited(grid,visited)
            current_area.append(current_point)
            q.put([current_point,current_area])
        
        print(f"Percentuale di completamento: {((len(visited)/max_visited)*100):0.2f}%",end="\r")
    
    print()
    return total


if __name__ == "__main__":
    test_1 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""
    test_2 = """AAAA
BBCD
BBCC
EEEC"""
    test_3 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
    test_4 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")