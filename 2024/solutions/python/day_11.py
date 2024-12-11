from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
from functools import cache

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

stone_have_even_digits: bool = lambda x: (len(str(x))%2) == 0

def split_string_by_half(stone: int) -> List[int]:
    l = len(str(stone))
    h = l // 2
    s = str(stone)
    return [int(s[:h]),int(s[h:])]

@cache
def parse_stone(stone: int) -> List[int]:
    if stone == 0: return [1]
    if stone_have_even_digits(stone) : return split_string_by_half(stone)
    return [stone*2024]

PART_1_BLINKS = 25
PART_2_BLINKS = 75

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    stones = [int(el) for el in inputs_1.split(" ")]
    blinks = 0
    while True:
        new_stones = list()
        for stone in stones:
            new_stones += parse_stone(stone)
        blinks += 1
        
        stones = list(new_stones)
        if blinks == PART_1_BLINKS:
            break
    
    return len(new_stones)
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    stones = [int(el) for el in inputs_1.split(" ")]
    blinks = 0
    while True:
        new_stones = list()
        for stone in stones:
            new_stones += parse_stone(stone)
        blinks += 1
        
        stones = list(new_stones)
        print(f"Blinks: {blinks: >3}", end="\r")
        
        if blinks == PART_2_BLINKS:
            print()
            break
        
    
    return len(stones)


if __name__ == "__main__":
    test = """0 1 10 99 999"""
    test_2 = """125 17"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2("125")}")