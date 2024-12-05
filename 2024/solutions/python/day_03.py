from starter import AOC, CURRENT_YEAR
from pathlib import Path
from re import findall
import re

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    regex = r'mul\((\d{1,3}),(\d{1,3})\)'
    finds = findall(regex,inputs_1)
    total = 0
    for find in finds:
        total += int(find[0])*int(find[1])
    return total
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    
    mul_regex = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
    do_regex = re.compile(r'do\(\)')
    dont_regex = re.compile(r'don\'t\(\)')

    total_sum = 0
    mul_enabled = True  

    index = 0
    length = len(inputs_1)
    
    while index < length:
        do_match = do_regex.match(inputs_1, index)
        dont_match = dont_regex.match(inputs_1, index)
        mul_match = mul_regex.match(inputs_1, index)    
        if do_match:
            mul_enabled = True
            index += do_match.end() - do_match.start()
        elif dont_match:
            mul_enabled = False
            index += dont_match.end() - dont_match.start()
        elif mul_match and mul_enabled:
            x, y = mul_match.groups()
            total_sum += int(x) * int(y)
            index += mul_match.end() - mul_match.start()
        else:
            index += 1
    return total_sum
    


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")