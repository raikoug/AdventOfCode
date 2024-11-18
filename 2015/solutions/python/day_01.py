from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    up      = inputs_1.count('(')
    down    = inputs_1.count(')')
    result = up - down
    return result
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    list_1 = [1 if el == "(" else -1 for el in list(inputs_1)]
    sum = 0
    i = 0
    while list_1:
        sum += list_1.pop(0)
        i += 1
        if sum == -1:
            return i
    return i


if __name__ == "__main__":
    print(solve_2())