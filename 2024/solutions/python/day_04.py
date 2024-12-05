from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    all_strings: List[str] = list()
    rows: List[str] = inputs_1.splitlines()
    all_strings += rows
    columns: List[str] = ["".join([rows[j][i] for j in range(len(rows))]) for i in range(len(rows[0])) ]
    all_strings += columns
    diagonali: List[str] = list()
    total = 0
    for offset in range(len(rows)):
        tmp_column_diag: str = ""
        tmp_row_diag: str = ""
        tmp_column_diag_dx: str = ""
        tmp_row_diag_dx: str = ""
        for row,col in zip(range(len(rows)),range(len(rows))):
            try:
                tmp_column_diag += rows[row+offset][col]
            except:
                pass
            try:
                tmp_row_diag += rows[row][col+offset]
            except:
                pass
            try:
                tmp_column_diag_dx += rows[row][-1-col-offset]
            except:
                pass
            try:
                tmp_row_diag_dx += rows[row+offset][-1-col]
            except:
                pass
            
            
        if len(tmp_column_diag) >=3: diagonali.append(tmp_column_diag)
        if len(tmp_row_diag) >= 3 and (offset != 0): diagonali.append(tmp_row_diag)
        if len(tmp_column_diag_dx) >=3: diagonali.append(tmp_column_diag_dx)
        if len(tmp_row_diag_dx) >= 3 and (offset != 0): diagonali.append(tmp_row_diag_dx)
    
    all_strings += diagonali
    for string in all_strings:
        total += string.count("XMAS")
        total += string.count("SAMX")
    return total
        
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # Create the grid from the given string input.
    # Define the dimensions of the grid
    grid = inputs_1.splitlines()
    rows = len(grid)
    cols = len(grid[0])
    
    count = 0
    
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "A":
                #print(f"found an A - {row}-{col}")
                # check the 4 pattern with try to avoid index out of range, but have to still check index < 0
                #
                # 1.2
                # .3.
                # 4.5
                #
                try:
                    if row-1 < 0:
                        raise
                    if col-1 < 0:
                        raise
                    one = grid[row-1][col-1]
                    two = grid[row-1][col+1]
                    # three always correct
                    four = grid[row+1][col-1]
                    five = grid[row+1][col+1]
                except:
                    #out of grid, not a pattern
                    #print(f"   Out of indexes!")
                    continue
                
                if any ([one not in "MS", two not in "MS", four not in "MS", five not in "MS"]): 
                    #print(f"   Not a X-MAS")
                    #print(f"      {one}-{two}-{four}-{five}")
                    continue
                #the possible combinations have this pattern:
                # M.M
                # .A.
                # S.S
                elif all([one == "M", two == "M", four == "S", five == "S"]) : 
                    #print(f"   It is a X-MAS!")
                    count += 1

                # S.M
                # .A.
                # S.M
                elif all([one == "S", two == "M", four == "S", five == "M"]) : 
                    #print(f"   It is a X-MAS!")
                    count += 1
                
                # S.S
                # .A.
                # M.M
                elif all([one == "S", two == "S", four == "M", five == "M"]) : 
                    #print(f"   It is a X-MAS!")
                    count += 1
                
                # M.S
                # .A.
                # M.S
                elif all([one == "M", two == "S", four == "M", five == "S"]) : 
                    #print(f"   It is a X-MAS!")
                    count += 1
                else:
                    #print(f"   Not a X-MAS")
                    #print(f"      {one}-{two}-{four}-{five}")
                    pass
                    

    return count


if __name__ == "__main__":
    test = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")