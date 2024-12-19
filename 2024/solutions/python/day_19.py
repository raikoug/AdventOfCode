from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional, Tuple, Generator
from dataclasses import dataclass, field
from queue import PriorityQueue
import sys
from functools import lru_cache

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    towels = inputs_1.splitlines()[0].split(", ")
    patterns = inputs_1.splitlines()[2:]
    feasible = 0
    
    def next_towels(line:str) -> Generator[str]:
        for towel in towels:
            if line.startswith(towel):
                yield towel
    max_patterns = len(patterns)
    for i,pattern in enumerate(patterns):
        print(f"Checking pattern: {i+1: >3} of {max_patterns}", end="\r")
        current_line = pattern
        s = set()
        s.add(current_line)
        found = False

        while s:
            current_line = s.pop()
            
            for next_towel in next_towels(current_line):
                if len(next_towel) == len(current_line):
                    feasible += 1
                    found = True
                    break
                else:
                    s.add(current_line[len(next_towel):])
            
            if found: break
    print()

    return feasible

def solve_2(test_string=None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    towels = inputs_1.splitlines()[0].split(", ")
    patterns = inputs_1.splitlines()[2:]
    total = 0
    
    @lru_cache(maxsize=None)
    def count_ways(current_line: str) -> int:
        if not current_line:
            return 1
        ways = 0
        for towel in towels:
            if current_line.startswith(towel):
                new_line = current_line[len(towel):]
                ways += count_ways(new_line)
        return ways

    max_patterns = len(patterns)
    for i,pattern in enumerate(patterns):
        print(f"Checking pattern: {i+1: >3} of {max_patterns}", end="\r")
        total += count_ways(pattern)
    print()
    
    return total


if __name__ == "__main__":
    test = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb"""

    
    
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")