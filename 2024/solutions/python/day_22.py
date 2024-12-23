from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
from functools import cache

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

@cache
def mix(n1: int, n2: int, v2: bool = False) -> int:
    return n1 ^ n2

@cache
def prune(n: int, v2:bool = False, mod:int = 16777216) -> int:
    return n % mod

@cache
def phase_1(secret: int, v2: bool = False, base: int = 64) -> int:
    number = secret * base
    return prune(mix(number,secret))

@cache
def phase_2(secret: int, v2: bool = False, den:int = 32) -> int:
    number = secret // den
    return prune(mix(number, secret))

@cache
def phase_3(secret: int, v2: bool = False, prod:int = 2048) -> int:
    number = secret * prod
    return prune(mix(number, secret))

@cache
def phases(secret, times: int, v2: bool = False) -> int:
    for _ in range(times):
        p1 = phase_1(secret)
        p2 = phase_2(p1)
        secret = phase_3(p2)
    return secret

def phase_iterator(secret, times: int, actual: int = 0):
    if actual < times:
        

        p1 = phase_1(secret)
        p2 = phase_2(p1)
        secret = phase_3(p2)
        yield secret
        
        yield from phase_iterator(secret, times, actual +1)
    
class Sequence(list):
    @cache
    def __hash__(self):
        return int("".join([str(ord(a)) for a in "".join([str(el) for el in self])]))
                

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    initials = [int(el) for el in inputs_1.splitlines()]
    total: int = 0
    for initial in initials:
        total += phases(initial, 2000)
    
    
    return total
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    sequences = dict()
    
    return 1


if __name__ == "__main__":
    test = """1
10
100
2024
"""
    #print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")