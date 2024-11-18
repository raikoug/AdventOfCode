from starter import AOC, CURRENT_YEAR
from pathlib import Path
import string
import re

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def alphabetically_increment(source: str) -> str:
    l = string.ascii_lowercase
    source_map = [l.index(el) for el in source]
    source_map[-1] += 1
    destination_map = []
    wrap = False
    for el in source_map[::-1]:
        if wrap:
            el += 1
            wrap = False

        if el == len(l):
            wrap = True
            destination_map.insert(0,0)
        else:
            destination_map.insert(0,el)
            
    
    new_string = "".join([l[el] for el in destination_map])
        
    return new_string

def is_next_next(a,b,c):
    oa, ob, oc = ord(a), ord(b), ord(c)
    return (ob == oa + 1) and (ob == oc -1)

def has_ladder(s: str) -> bool:
    trees = [[s[i],s[i+1],s[i+2]] for i in range(len(s)-2)]
    for tree in trees:
        if is_next_next(*tree): return True
    
    return False

def has_double_double(s: str) -> bool:
    regex = r'(.)\1'
    findall = set(re.findall(regex, s))
    return len(findall) >= 2

    
def string_is_ok(source: str) -> bool:
    ok = True
    if not has_ladder(source): 
        #print("has no ladder")
        return False
    if not has_double_double(source): 
        #print("has no double")
        return False
    if any([c in source for c in "iol"]):
        #print("has `iol` inside")
        return False
        
    
    return ok

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    new_string = alphabetically_increment(inputs_1)
    while True:
        ok = string_is_ok(new_string)
        if ok:
            return new_string
        #print(f"new_string: {new_string} is ok: {ok}")
        new_string = alphabetically_increment(new_string)
    return new_string
    
def solve_2(test_string = None) -> int:
    return solve_1(solve_1())


if __name__ == "__main__":
    print(solve_2())