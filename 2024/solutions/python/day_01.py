from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    left_values = list()
    right_values= list()
    for line in inputs_1.splitlines():
        left, right = line.split("   ")
        left_values.append(int(left))
        right_values.append(int(right))
    left_values.sort()
    right_values.sort()
    summ = 0
    for i in range(len(left_values)):
        summ += abs(left_values[i] - right_values[i])
    
    return summ
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    left_values = list()
    right_values= list()
    for line in inputs_1.splitlines():
        left, right = line.split("   ")
        left_values.append(int(left))
        right_values.append(int(right))
    
    summ = 0
    for i in range(len(left_values)):
        summ += left_values[i] * right_values.count(left_values[i])
    
    return summ


if __name__ == "__main__":
    test = """3   4
4   3
2   5
1   3
3   9
3   3
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")