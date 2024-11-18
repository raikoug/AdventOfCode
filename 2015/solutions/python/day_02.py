from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    lines = inputs_1.splitlines()
    line_numbers = [line.split("x") for line in lines if line]
    sqf = 0
    for numbers in line_numbers:
        real = [int(n) for n in numbers]
        l,w,h = real
        real.sort()
        sqf += 2 * (l*w + w*h + h*l)
        sqf += real[0] * real[1]
    return sqf
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    lines = inputs_1.splitlines()
    line_numbers = [line.split("x") for line in lines if line]
    ribbonfeet = 0
    for numbers in line_numbers:
        real = [int(n) for n in numbers]
        l,w,h = real
        real.sort()
        ribbonfeet += l*w*h
        ribbonfeet += 2 * (real[0]+real[1])
    return ribbonfeet


if __name__ == "__main__":
    print(solve_2())