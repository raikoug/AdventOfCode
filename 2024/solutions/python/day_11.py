from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional, Dict, Self
from dataclasses import dataclass, field
from functools import cache

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

stone_have_even_digits: bool = lambda x: (len(str(x))%2) == 0

class Stones(dict):
    def add_stones_list(self, stones: List[int], count: int = 1):
        for stone in stones:
            self.add_stones(stone,count)
    
    def add_stones(self, stone: int, count: int = 1):
        self[stone] = self.get(stone,0) + count

    def parse_stones(self):
        new_self = dict(self)
        self.clear()
        for stone,count in new_self.items():
            #print("     ", stone, count)
            parse_stone_v2(stone,count)



STONES = Stones()

def parse_stone_v2(stone: int, count: int) -> None:
    if stone == 0: 
        #print(f"       Stone 1 {count} times")
        STONES.add_stones(1,count)
    elif stone_have_even_digits(stone): 
        #print("       Stones list: ", split_string_by_half(stone))
        STONES.add_stones_list(split_string_by_half(stone), count)
    else: 
        #print(f"       Stone {stone*2024} {count} times")
        STONES.add_stones(stone*2024, count)

@cache
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
    STONES.add_stones_list([int(el) for el in inputs_1.split(" ")])
    #print(STONES)
    blinks = 0
    while True:
        #print(f"Giro {blinks}")
        STONES.parse_stones()
        #print("   ", STONES)
        blinks += 1
        print(f"Blink: {blinks: >5}", end = "\r")
        if blinks == PART_1_BLINKS:
            break
    print()
    return sum(STONES.values())

    
def solve_2(test_string = None) -> int:
    STONES.clear()
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    STONES.add_stones_list([int(el) for el in inputs_1.split(" ")])
    #print(STONES)
    blinks = 0
    while True:
        #print(f"Giro {blinks}")
        STONES.parse_stones()
        #print("   ", STONES)
        blinks += 1
        print(f"Blink: {blinks: >5}", end = "\r")
        if blinks == PART_2_BLINKS:
            break
    print()
    return sum(STONES.values())


if __name__ == "__main__":
    test = """0 1 10 99 999"""
    test_2 = """125 17"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")