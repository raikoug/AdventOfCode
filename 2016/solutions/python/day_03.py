from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    possible = 0
    for line in inputs_1.splitlines():
        try:
            cateti = sorted([int(num.strip()) for num in line.split(" ") if num])
            if cateti[0] + cateti[1] > cateti[2]:
                possible += 1
        except Exception as e:
            print(e, line)
    
    return possible
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    possible = 0
    lines = inputs_1.splitlines()
    for i in range(0,len(lines),3):
        tr1_a, tr2_a, tr3_a = lines[i].split()
        tr1_b, tr2_b, tr3_b = lines[i+1].split()
        tr1_c, tr2_c, tr3_c = lines[i+2].split()
        tr1 = sorted([int(el) for el in [tr1_a,tr1_b,tr1_c]])
        tr2 = sorted([int(el) for el in [tr2_a,tr2_b,tr2_c]])
        tr3 = sorted([int(el) for el in [tr3_a,tr3_b,tr3_c]])
        
        if tr1[0] + tr1[1] > tr1[2]: possible += 1
        if tr2[0] + tr2[1] > tr2[2]: possible += 1
        if tr3[0] + tr3[1] > tr3[2]: possible += 1

    return possible


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")