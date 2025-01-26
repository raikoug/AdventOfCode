from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass, field

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def eval_key(lines: List[str]) -> List[int]:
    """
    ..... 6
    ..... 5
    ..... 4
    #.... 3
    #.#.. 2
    #.#.# 1
    ##### 0
    """
    h = len(lines)
    l = len(lines[0])
    res : List[int] = [0] * l
    for row,line in enumerate(lines):
        for col,char in enumerate(line):
            if char == "#":
                res[col] = max(res[col], h-row-1)
    
    return res
                    
def eval_lock(lines: List[str]) -> List[int]:
    """
    ##### 0
    .#### 1
    .#### 2
    .#### 3
    .#.#. 4
    .#... 5
    ..... 6
    """
    h = len(lines)
    l = len(lines[0])
    res : List[int] = [0] * l
    for row,line in enumerate(lines):
        for col,char in enumerate(line):
            if char == "#":
                res[col] = max(res[col], row)
    
    return res

def sum_lock_key(lock: List[int], key: List[int]) -> List[int]:
    return [lock[i]+key[i] for i in range(len(lock))]
        
def eval_block(tmp_block: List[str]) -> Tuple[List[int], int]:
    if tmp_block[0].startswith("#####"):
        return eval_lock(tmp_block), 1
    else:
        return eval_key(tmp_block), 2
    
def is_ok(fit: List[int]):
    return all([el <= 5 for el in fit])


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    locks : List[int] = list()
    keys  : List[int] = list()
    tmp_block : List[str] = list()
    for line in inputs_1.splitlines():
        if line:
            tmp_block.append(line)
        
        else:
            pins, types = eval_block(tmp_block)
            if types == 1:
                locks.append(pins)
            else:
                keys.append(pins)
            tmp_block.clear()
    if tmp_block:
        pins, types = eval_block(tmp_block)
        if types == 1:
            locks.append(pins)
        else:
            keys.append(pins)
    
    total_keys = len(keys)
    result = 0
    for i,key in enumerate(keys):
        print(f"Testing key {i+1: >3} out of {total_keys}", end="\r")
        for lock in locks:
            if is_ok(sum_lock_key(key,lock)):
                result += 1

    print()
    return result
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
        
    return 1


if __name__ == "__main__":
    test = """#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")