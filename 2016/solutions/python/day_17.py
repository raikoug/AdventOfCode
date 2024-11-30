from starter import AOC, CURRENT_YEAR
from pathlib import Path
from queue import PriorityQueue
from typing import List
from hashlib import md5

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

D = {
        "U": [0,-1],
        "R": [1,0],
        "D": [0,1],
        "L": [-1,0]
    }

def part_1_find_md5(s: str) -> str:
    return md5(s.encode()).hexdigest()

move = lambda pos, d : [pos[0] + D[d][0], pos[1] + D[d][1]]

OD = "bcdef"

def find_open_doors(md5sum):
    res = list()
    if md5sum[0] in OD: res.append("U")
    if md5sum[1] in OD: res.append("D")
    if md5sum[2] in OD: res.append("L")
    if md5sum[3] in OD: res.append("R")
    return res

def around_me(code, x, y):
    res = list()
    open_doors = find_open_doors(part_1_find_md5(code))
    #UP
    if (y>0) and ("U" in open_doors): res.append("U")
    #RIGHT
    if (x<3) and ("R" in open_doors): res.append("R")
    #DOWN
    if (y<3) and ("D" in open_doors): res.append("D")
    #LEFT
    if (x>0) and ("L" in open_doors): res.append("L")
    
    return res

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    q = PriorityQueue()
    q.put([0, (0,0), ""])
    found = False
    max_steps = 0
    while not found:
        # around_me(inputs_1+"DUR", 1, 0)
        steps, pos, directions = q.get()
        possible_directions = around_me(f"{inputs_1}{directions}", *pos)
        for dir in possible_directions:
            new_pos = move(pos, dir)
            new_dir = directions+dir
            if new_pos == [3,3]:
                found = True
                break
            q.put([steps+1, new_pos, new_dir])
        
        if steps+1 > max_steps:
            max_steps += 1 
    return new_dir
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    q = PriorityQueue()
    q.put([0, (0,0), ""])
    found = False
    max_steps = 0
    while not found:
        # around_me(inputs_1+"DUR", 1, 0)
        steps, pos, directions = q.get()
        possible_directions = around_me(f"{inputs_1}{directions}", *pos)
        for dir in possible_directions:
            new_pos = move(pos, dir)
            new_dir = directions+dir
            if new_pos == [3,3]:
                max_steps = steps+1
            else:
                q.put([steps+1, new_pos, new_dir])
        if q.empty():
            break
    return max_steps

if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")