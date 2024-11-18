from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

class Grid(list):
    def __init__(self):
        for i in range(1000):
            self.append([False]*1000)
    
    def turn(self, corner1, corner2, on, off, toggle):
        new = True if on else False
        x1,y1 = corner1
        x2,y2 = corner2
        for i in range(x1,x2+1):
            for j in range(y1,y2+1):
                if toggle: self[i][j] = not self[i][j]
                else: self[i][j] = new
    
    def bright(self, corner1, corner2, on, off, toggle):
        new = 1 if on else -1
        x1,y1 = corner1
        x2,y2 = corner2
        for i in range(x1,x2+1):
            for j in range(y1,y2+1):
                if toggle: self[i][j] += 2
                else: self[i][j] = max(0, self[i][j] + new)
    
    def count(self) -> int:
        res = 0
        for i in range(1000):
            for j in range(1000):
                res += self[i][j]
        return res
    
    def print(self) -> None:
        for i in range(1000):
            for j in range(1000):
                print(1 if self[i][j] else 0, end = "")
            print()
        print()
    
    def save(self) -> None:
        path = aoc.get_day_folder_path(CURRENT_DAY)
        outfile = path / "out.text"
        with open(outfile, "w") as f:
            for i in range(1000):
                for j in range(1000):
                    f.write(f"{1 if self[i][j] else 0}")
                f.write("\n")
            f.write("\n")

def map_string_to_command(line:str) -> list:
    #toggle 461,550 through 564,900
    #turn off 370,39 through 425,839
    #turn on 599,989 through 806,993
    on, off, toggle = False, False, False
    corner1 = [0,0]
    corner2 = [0,0]

    if line.startswith("turn on"): 
        on = True
        new_line = line.replace("turn on ", "").replace(" through ", " ")
    elif line.startswith("turn off"): 
        off = True
        new_line = line.replace("turn off ", "").replace(" through ", " ")
    elif line.startswith("toggle"): 
        toggle = True
        new_line = line.replace("toggle ", "").replace(" through ", " ")
        
    c1,c2 = new_line.split(" ")
    corner1 = [int(i) for i in c1.split(",")]
    corner2 = [int(i) for i in c2.split(",")]
    
    return corner1, corner2, on, off, toggle

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    g = Grid()
    lines = inputs_1.splitlines()
    for line in lines:
        g.turn(*map_string_to_command(line))
    g.save()
    return g.count()
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    g = Grid()
    lines = inputs_1.splitlines()
    for line in lines:
        g.bright(*map_string_to_command(line))
    g.save()
    return g.count()


if __name__ == "__main__":
    print(solve_2())