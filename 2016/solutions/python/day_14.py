from starter import AOC, CURRENT_YEAR
from pathlib import Path
from hashlib import md5
from re import findall
from functools import cache
CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)


@cache
def part_1_find_md5(s: str) -> str:
    return md5(s.encode()).hexdigest()

@cache
def part_2_find_md5(s: str) -> str:
    for i in range(2017):
        s = md5(s.encode()).hexdigest()
    return s

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # inside possible keys: [char, pattern, index, max_i]
    #  char that is repeated 3 times and index where it has been found.
    possible_keys = list()
    # inside keys we have [char, index1, index2]
    keys = list()
    i = 0
    regex = r'(\w)\1\1'
    found = False
    while True:
        m = part_1_find_md5(f"{inputs_1}{i}")
        # check possible keys first:
        
        r = findall(regex,m)
        if r:
            # possible key found, checking if it's also confirmed
            #print(f"Possible key found at index {i}")
            char = r[0]
            pattern = char*5
            for j in range(i+1,i+1001):
                s = part_1_find_md5(f"{inputs_1}{j}")
                if pattern in s:
                    # confirmed
                    keys.append([char,i,j])
                    #print(f"    Found a new key: {char} at index {i} confirmed at index {j}")
                    if len(keys) == 64:
                        found = True
                    break
        if found: break
        
        i += 1
    return i
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # inside possible keys: [char, pattern, index, max_i]
    #  char that is repeated 3 times and index where it has been found.
    possible_keys = list()
    # inside keys we have [char, index1, index2]
    keys = list()
    i = 0
    regex = r'(\w)\1\1'
    found = False
    while True:
        m = part_2_find_md5(f"{inputs_1}{i}")
        # check possible keys first:
        
        r = findall(regex,m)
        if r:
            # possible key found, checking if it's also confirmed
            #print(f"Possible key found at index {i}")
            char = r[0]
            pattern = char*5
            for j in range(i+1,i+1001):
                s = part_2_find_md5(f"{inputs_1}{j}")
                if pattern in s:
                    # confirmed
                    keys.append([char,i,j])
                    #print(f"    Found a new key: {char} at index {i} confirmed at index {j}")
                    if len(keys) == 64:
                        found = True
                    break
        if found: break        
        i += 1
    return i

if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")