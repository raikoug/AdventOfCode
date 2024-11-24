from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Self

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

class Digital():
    grid = List[List]
    off: str
    on: str
    
    def __init__(self, rows: int = 6, cols: int = 50,
                 on = "𑨠", off = " ")-> None:
        self.grid = list()
        self.on = on
        self.off = off
        for _ in range(rows):
            self.grid.append([self.off]*cols)
    
    def printa(self):
        for row in self.grid:
            print(" ".join(row))
    
    def rect(self, lenght: int, height: int)-> None:
        for row in range(height):
            self.grid[row][:lenght] = [self.on]*lenght
            
    def row_rotate(self, row: int, times: int) -> None:
        for _ in range(times):
            self.grid[row].insert(0,self.grid[row].pop(-1))
            
    def col_rotate(self, col: int, times: int) -> None:
        column = [self.grid[i][col] for i in range(len(self.grid))]
        for _ in range(times):
            column.insert(0, column.pop(-1))
        for i in range(len(self.grid)):
            self.grid[i][col] = column[i]

    def count(self):
        res = 0
        for row in self.grid:
            res += row.count(self.on)
        return res

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    d = Digital()
    for line in inputs_1.splitlines():
        if "rect" in line:
            _, vals = line.split(" ")
            lenght, height = vals.split("x")
            d.rect(int(lenght), int(height))
        elif "column" in line:
            #rotazione colonna
            # rotate column x=1 by 1
            _,_,xeq,_,times = line.split(" ")
            col = int(xeq.replace("x=", ""))
            times = int(times)
            d.col_rotate(int(col), times)

        elif "row" in line:
            #rotazione riga
            # rotate row y=0 by 4
            _,_,yeq,_,times = line.split(" ")
            row = int(yeq.replace("y=", ""))
            times = int(times)
            d.row_rotate(int(row), times)
    return d
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
        
    return 1


if __name__ == "__main__":
    test="""rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
"""
    d: Digital = solve_1()
    print(f"Part 1: {d.count}")
    print(f"Part 2: {d.printa()}")