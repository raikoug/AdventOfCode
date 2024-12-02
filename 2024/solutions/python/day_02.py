from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def check_numbers(ns: list) -> bool:
    coppie = [[ns[i],ns[i+1]] for i in range(0,len(ns)-1)]
    good = True
    # se fosse crescente:
    if coppie[0][0] < coppie[0][1]: # crescente
        diff = [el[1]-el[0] for el in coppie]
    else:
        diff = [el[0]-el[1] for el in coppie]
        
    for d in diff:
        if (d > 3) or (d < 1):
            good = False
            break
    
    return good

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    safe = 0
    for line in inputs_1.splitlines():
        ns = [int(el) for el in line.split(" ")]
        if check_numbers(ns):
            safe += 1 
        
    return safe
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    safe = 0
    for line in inputs_1.splitlines():
        ns = [int(el) for el in line.split(" ")]
        if check_numbers(ns):
            safe += 1
            continue
        for i in range(len(ns)):
            tmp_row = ns[:i] + ns[i+1:]
            if check_numbers(tmp_row):
                safe += 1
                break
    
    return safe

if __name__ == "__main__":
    test = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")