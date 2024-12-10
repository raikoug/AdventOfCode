from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
from queue import PriorityQueue

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)


def possible_next_steps(row:int,col:int,grid:List[List[int]]) -> List[List[int]]:
    
    positions = [
        [row+1,col],
        [row,col+1],
        [row-1,col],
        [row,col-1]
    ]
    #print(f"        possible_next_steps - positions: {positions}")
    
    max_row = len(grid)-1
    max_col = len(grid[0])-1
    

    #print(f"        possible_next_steps - init with row: {row}, col: {col}, max_row: {max_row}, max_col: {max_col}")
    good_pos: List[int] = list()
    
    for pos in positions:
        new_row,new_col = pos
        #print(f"        possible_next_steps - evaluating {new_row},{new_col}")
        if all([
            new_row >= 0,
            new_col >= 0,
            new_row <= max_row,
            new_col <= max_col
        ]):
            if grid[new_row][new_col] == (grid[row][col] + 1):
                good_pos.append(pos)
            
    
    return good_pos



def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    hashing = lambda x,y : (x*10000) + y
    visited : List = list()
    grid = [[int(el) for el in line] for line in inputs_1.splitlines()]
    max_row = len(grid)-1
    max_col = len(grid[0])-1
    q = PriorityQueue()
    # queue values will have: [steps,row,col]
    start_points : List = list()
    total : int = 0
    for i,row in enumerate(grid):
        for j,col in enumerate(row):
            if col == 0:
                start_points.append([i,j])

    for start_point in start_points:
        new_row,new_col = start_point
        #print(f"Evaluating starting point {new_row},{new_col}")
        visited: set = set()
        q.put([0,new_row,new_col])
        while not q.empty():
            steps,row,col = q.get()
            h = hashing(row,col)
            if h in visited:
                continue
            elif grid[row][col] == 9:
                #print("    Peak found!")
                visited.add(h)
                total += 1
                continue
            #print(f"  Evaluating {row},{col}")
            
            visited.add(h)
            next_steps = possible_next_steps(row,col,grid)
            #print(f"    from {row},{col} -> {next_steps}")
            for next_step in next_steps:
                new_row,new_col = next_step
                q.put([steps+1,new_row,new_col])
        #print(f"new_total: {total}")
    return total
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    hashing = lambda x,y : (x*10000) + y
    visited : List = list()
    grid = [[int(el) for el in line] for line in inputs_1.splitlines()]
    max_row = len(grid)-1
    max_col = len(grid[0])-1
    q = PriorityQueue()
    # queue values will have: [steps,row,col]
    start_points : List = list()
    total : int = 0
    for i,row in enumerate(grid):
        for j,col in enumerate(row):
            if col == 0:
                start_points.append([i,j])

    for start_point in start_points:
        new_row,new_col = start_point
        #print(f"Evaluating starting point {new_row},{new_col}")
        q.put([0,new_row,new_col])
        while not q.empty():
            steps,row,col = q.get()

            if grid[row][col] == 9:
                #print("    Peak found!")
                total += 1
                continue
            #print(f"  Evaluating {row},{col}")
            
            next_steps = possible_next_steps(row,col,grid)
            #print(f"    from {row},{col} -> {next_steps}")
            for next_step in next_steps:
                new_row,new_col = next_step
                q.put([steps+1,new_row,new_col])
        #print(f"new_total: {total}")
        
        
    
    return total


if __name__ == "__main__":
    test = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
    test_2 = """012345
123456
234567
345678
416789
567891
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")