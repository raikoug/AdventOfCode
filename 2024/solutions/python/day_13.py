from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field

# Added imports:
import re
from z3.z3 import *

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

@dataclass(frozen=True)
class Pos:
    i: int
    j: int
    def __add__(self, other):
        return Pos(self.i + other.i, self.j + other.j)
    def scalar_mul(self, a):
        return Pos(a*self.i, a*self.j)
    def __eq__(self, other):
        return isinstance(other, Pos) and (self.i, self.j) == (other.i, other.j)
    def __hash__(self):
        return hash((self.i, self.j))

def get_min_tokens(a_vector, b_vector, prize_vector):
    l = Int('l')
    m = Int('m')
    s = Optimize()
    s.add(l >= 0)
    s.add(m >= 0)
    s.add(l * a_vector.i + m * b_vector.i == prize_vector.i)
    s.add(l * a_vector.j + m * b_vector.j == prize_vector.j)
    h = s.minimize(3*l + m)
    if s.check() == sat:
        s.lower(h)
        result = s.model()
        return 3*result[l].as_long() + result[m].as_long()
    else:
        return None

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    
    lines = inputs_1.strip().split('\n')
    min_tokens1 = 0
    for i, line in enumerate(lines):
        if i%4 == 0:
            pattern = r'Button A: X\+(\d+), Y\+(\d+)'
            ax, ay = (int(z) for z in re.match(pattern, line).groups())
        elif i%4 == 1:
            pattern = r'Button B: X\+(\d+), Y\+(\d+)'
            bx, by = (int(z) for z in re.match(pattern, line).groups())
        elif i%4 == 2:
            pattern = r'Prize: X=(\d+), Y=(\d+)'
            px, py = (int(z) for z in re.match(pattern, line).groups())
            tokens = get_min_tokens(Pos(ax, ay), Pos(bx, by), Pos(px, py))
            if tokens is not None:
                min_tokens1 += tokens
    return min_tokens1
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    
    lines = inputs_1.strip().split('\n')
    min_tokens2 = 0
    for i, line in enumerate(lines):
        if i%4 == 0:
            pattern = r'Button A: X\+(\d+), Y\+(\d+)'
            ax, ay = (int(z) for z in re.match(pattern, line).groups())
        elif i%4 == 1:
            pattern = r'Button B: X\+(\d+), Y\+(\d+)'
            bx, by = (int(z) for z in re.match(pattern, line).groups())
        elif i%4 == 2:
            pattern = r'Prize: X=(\d+), Y=(\d+)'
            px, py = (int(z) for z in re.match(pattern, line).groups())
            px2, py2 = 10000000000000 + px, 10000000000000 + py
            tokens = get_min_tokens(Pos(ax, ay), Pos(bx, by), Pos(px2, py2))
            if tokens is not None:
                min_tokens2 += tokens
    return min_tokens2

if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
