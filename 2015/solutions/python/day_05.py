from starter import AOC, CURRENT_YEAR
from pathlib import Path

import re

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    res = 0
    for line in inputs_1.splitlines():
        good = sum([line.count(l) for l in ["a","e","i","o","u"]]) >= 3
        if not good: continue
        good = sum([l in line for l in ["ab","cd","pq","xy"]]) == 0
        if not good: continue
        good = sum([line[i:i+2][0]==line[i:i+2][1] for i in range(0,len(line)-1)]) >= 1
        if not good: continue
        if good: res+=1
        
    return res
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    res = 0
    for line in inputs_1.splitlines():
        pattern=r'(\w).\1'
        #print(f"{line}")
        good = re.search(pattern,line) != None
        #print(f"   {good}")
        if not good: continue
        pattern=r'(\w\w).*\1'
        good = re.search(pattern,line) != None
        #print(f"   {good}")
        if not good: continue
        if good: res +=1
    return res


if __name__ == "__main__":
    print(solve_2())