from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Any
from itertools import permutations

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def safe_index(lst: list, element: Any) -> int:
    try:
        return lst.index(element)
    except:
        return -1

def update_is_ok(update: List[int], rules: List[int]) -> bool:
    for rule in rules:
        
        a,b = safe_index(update,rule[0]), safe_index(update,rule[1])
        if any([a<0, b<0]):
            # number missing, ignore rule
            continue
        if a > b:
            return False
    
    return True

def fix_update(update: List[int], rules: List[int]) :
    for rule in rules:
        a,b = safe_index(update,rule[0]), safe_index(update,rule[1])
        if any([a<0, b<0]):
            # number missing, ignore rule
            continue
        if a > b:
            #fixes! 
            # easy permutate wrong?
            update[a], update[b] =  update[b], update[a]
            return fix_update(update, rules)
    
    return [True, update]



def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    rules : List[int] = list()
    updates: List[int] = list()
    for line in inputs_1.splitlines():
        if "|" in line:
            a,b = line.split("|")
            rules.append([int(a), int(b)])
        elif "," in line:
            tmp_upd = list()
            for el in line.split(","):
                tmp_upd.append(int(el))
            updates.append(tmp_upd)
    total: int = 0
    for update in updates:
        if update_is_ok(update,rules):
            total += update[len(update)//2]
    return total
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    rules : List[int] = list()
    updates: List[int] = list()
    for line in inputs_1.splitlines():
        if "|" in line:
            a,b = line.split("|")
            rules.append([int(a), int(b)])
        elif "," in line:
            tmp_upd = list()
            for el in line.split(","):
                tmp_upd.append(int(el))
            updates.append(tmp_upd)
    total: int = 0
    for update in updates:
        if not update_is_ok(update,rules):
            result, fixed_update = fix_update(update,rules)
            total += fixed_update[len(fixed_update)//2]
    return total


if __name__ == "__main__":
    test = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")