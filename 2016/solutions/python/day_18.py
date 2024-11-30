from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def new_row(row: str) -> str:
    tmp_row = "."+row+"."
    res = ""
    triplettes = ["".join([tmp_row[i], tmp_row[i+1], tmp_row[i+2]]) for i in range(0,len(row))]
    for el in triplettes:
        char = "."
        #Its left and center tiles are traps, but its right tile is not: ^^.
        #Its center and right tiles are traps, but its left tile is not. .^^
        #Only its left tile is a trap.: ^..
        #Only its right tile is a trap.: ..^
        trap_generator = ["^^.", ".^^", "^..", "..^"]
        if el in trap_generator:
            char = "^"
        res += char
    return res
        

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    safe_tiles = inputs_1.count(".")
    row = inputs_1
    for i in range(39):
        row = new_row(row)
        safe_tiles += row.count(".")
    
    return safe_tiles
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    safe_tiles = inputs_1.count(".")
    row = inputs_1
    already_seen_rows = list()
    for i in range(400000-1):
        row = new_row(row)
        if row in already_seen_rows:
            print(f"We should reflect... after {i} we have the same pattern, module this out?")
        else:
            already_seen_rows.append(row)
        safe_tiles += row.count(".")
    
    return safe_tiles


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")