from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    rows = inputs_1.splitlines()
    columns = [list() for i in range(len(rows[0]) )]
    
    for row in rows:
        for i,el in enumerate(row):
            columns[i].append(el)
    
    result = ""
    for column in columns:
        best = 0
        for el in column:
            cnt = column.count(el)
            if cnt > column.count(best):
                best = el
        result += best
    return result
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    rows = inputs_1.splitlines()
    columns = [list() for i in range(len(rows[0]) )]
    
    for row in rows:
        for i,el in enumerate(row):
            columns[i].append(el)
    
    result = ""
    for column in columns:
        best = column[0]
        for el in column:
            cnt = column.count(el)
            if cnt < column.count(best):
                best = el
        result += best
    return result

if __name__ == "__main__":
    test = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")