from starter import AOC, CURRENT_YEAR
from pathlib import Path
from re import findall
import sys

sys.setrecursionlimit(20000000)

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def gen_code(i):
    if i == 1:
        return 20151125
    return (gen_code(i-1)*252533) % 33554393

def gen_start(i):
    if i == 1:
        return 1
    return gen_start(i-1) + (i - 1)

def grid_print(row,col):
    rows = list()
    for i in range(1,row+1):
        rows.append(list())
        index = i -1
        next_n = i + 1
        start = gen_start(i)
        
        rows[index].append(start)
        j = 1
        while j < col:
            rows[index].append(rows[index][-1] + next_n)
            next_n += 1 
            j+=1
            p = len(str(rows[index][-1]))
    
    max_first_col = len(str(row))
    first_row = "".join([f"{i+1: ^{(p+2)}}" for i in range(col)])
    print(f"{' ' * (max_first_col+2)}|{first_row}")
    print("-"*(max_first_col+2),"+", "+".join(["-"*(p+1)]*(col)), "+",sep="")
    
    for i,row in enumerate(rows):
        print(f"{i+1: ^{(max_first_col+2)}}","|","".join([f'{str(el): ^{p+2}}' for el in row]), sep="")
        
def get_row_col_val(row: int, col: int) -> int:
    start = gen_start(row)
    j = 1
    next_n = row + 1
    while j < col:
        start = start + next_n
        next_n += 1
        j += 1
    
    return start

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    regex = r'row (\d*), column (\d*)\.'
    matches = findall(regex, inputs_1)
    row = int(matches[0][0])
    col = int(matches[0][1])
    print(row, col)
    grid_print(10,10)
    val = get_row_col_val(row, col)
    print(val)
    result = gen_code(val)
    return result
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
        
    return 1


if __name__ == "__main__":
    test_1 = 'row 3, column 4.'
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
    
