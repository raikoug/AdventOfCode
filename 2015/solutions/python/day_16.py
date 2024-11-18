from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

TP = {
    "children" : 3,
    "cats" : 7,
    "samoyeds" : 2,
    "pomeranians" : 3,
    "akitas" : 0,
    "vizslas" : 0,
    "goldfish" : 5,
    "trees" : 3,
    "cars" : 2,
    "perfumes" : 1
}

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # i know I have a problem with this........
    get_i = lambda s, i : s.replace(":","").replace(",","").replace("Sue ","").split(" ")[i]
    sues = {
        int(get_i(line,0)) : {
            get_i(line, 1) : int(get_i(line, 2)),
            get_i(line, 3) : int(get_i(line, 4)),
            get_i(line, 5) : int(get_i(line, 6)),
            } 
        for line in inputs_1.splitlines()}
    
    for i in range(1,501):
        ok = True
        sue = sues[i]
        suekeys = sue.keys()
        for k,v in TP.items():
            if k in suekeys:
                if v != sue[k]:
                    ok = False
                    break
        if not ok: continue
        result = i
    
    return result

    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # i know I have a problem with this........
    get_i = lambda s, i : s.replace(":","").replace(",","").replace("Sue ","").split(" ")[i]
    sues = {
        int(get_i(line,0)) : {
            get_i(line, 1) : int(get_i(line, 2)),
            get_i(line, 3) : int(get_i(line, 4)),
            get_i(line, 5) : int(get_i(line, 6)),
            } 
        for line in inputs_1.splitlines()}
    
    for i in range(1,501):
        ok = True
        sue = sues[i]
        suekeys = sue.keys()
        for k,v in TP.items():
            if k in suekeys:
                if k in ["cats", "trees"]:
                    if sue[k] <= v:
                        ok = False
                        break
                elif k in ["pomeranians", "goldfish"]:
                    if sue[k] >=v:
                        ok = False
                        break
                elif v != sue[k]:
                    ok = False
                    break
                
        if not ok: continue
        result = i
    
    return result


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")