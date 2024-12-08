from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

M = {
    "^": (-1,0),
    ">": (0,1),
    "v": (1,0),
    "<": (0,-1)
}
D = {
    "^": ">",
    ">": "v",
    "v": "<",
    "<": "^"
}

def stampa_dir(grid,row,col,dir):
    for i,riga in enumerate(grid):
        for j,c in enumerate(riga):
            if row==i and j==col:
                print(dir,end="")
            else:
                print(c if c != "^" else ".",end="")
        print()   

def stampa(grid):
    for i,riga in enumerate(grid):
        print(riga)

def stampa_visited(grid,visited):
    for i,riga in enumerate(grid):
        for j,c in enumerate(riga):
            if [i,j] in visited:
                print("X",end="")
            else:
                print(c if c != "^" else ".",end="")
        print()  

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    grid: List[str] = inputs_1.splitlines()
    visited_tiles: List[List[int,int]] = list()
    walking_tiles: List[List[int,int,str]] = list()
    for i,row in enumerate(grid):
        guard =  row.find("^")
        if guard > 0:
            walking_tiles.append([i,guard,"^"])
            visited_tiles.append([i,guard])
            grid[i].replace("^",".")
            break
    guard : List[int,int,str]
    row: int
    col: int
    dir: str
    loop = 0
    
    while True:
        row,col,dir = walking_tiles[-1]
        #stampa(grid,row,col,dir)
        #print()
        new_row,new_col = row+M[dir][0],col+M[dir][1]
        if any([
            new_row <0,
            new_row >= len(grid),
            new_col <0,
            new_col > len(grid[0])
        ]):
            #end of labirinth!
            break
        if grid[new_row][new_col] == "#":
            new_dir = D[dir]
            walking_tiles.append([row,col,new_dir])
        else:
            new_walking = [new_row,new_col,dir]
            if new_walking in walking_tiles:
                # THIS IS A LOOP!
                loop += 1
                break
            walking_tiles.append(new_walking)
            new_tyle = [row,col]
            if new_tyle not in visited_tiles: visited_tiles.append(new_tyle)

    return len(visited_tiles) + 1


def is_loop(grid):
    visited_tiles: List[List[int,int]] = list()
    walking_tiles: List[List[int,int,str]] = list()
    for i,row in enumerate(grid):
        guard =  row.find("^")
        if guard > 0:
            walking_tiles.append([i,guard,"^"])
            visited_tiles.append([i,guard])
            grid[i].replace("^",".")
            break
    guard : List[int,int,str]
    row: int
    col: int
    dir: str
    loop = 0
    
    while True:
        row,col,dir = walking_tiles[-1]
        #stampa(grid,row,col,dir)
        #print()
        new_row,new_col = row+M[dir][0],col+M[dir][1]
        if any([
            new_row <0,
            new_row >= len(grid),
            new_col <0,
            new_col >= len(grid[0])
        ]):
            #end of labirinth!
            break
        if grid[new_row][new_col] == "#":
            new_dir = D[dir]
            walking_tiles.append([row,col,new_dir])
        else:
            new_walking = [new_row,new_col,dir]
            if new_walking in walking_tiles:
                # THIS IS A LOOP!
                loop += 1
                return True
            walking_tiles.append(new_walking)
            new_tyle = [row,col]
            if new_tyle not in visited_tiles: visited_tiles.append(new_tyle)
    return False

def make_new_grid(grid,tile):
    new_grid = list()
    for i,row in enumerate(grid):
        tmp_row = ""
        for j,c in enumerate(row):
            if c == "^":
                tmp_row += c
            elif [i,j] == tile:
                tmp_row += "#"
            else:
                tmp_row += c
        new_grid.append(tmp_row)
    return new_grid

def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    grid: List[str] = inputs_1.splitlines()
    visited_tiles: List[List[int,int]] = list()
    walking_tiles: List[List[int,int,str]] = list()
    for i,row in enumerate(grid):
        guard =  row.find("^")
        if guard > 0:
            walking_tiles.append([i,guard,"^"])
            visited_tiles.append([i,guard])
            grid[i].replace("^",".")
            break
    guard : List[int,int,str]
    row: int
    col: int
    dir: str
    loop = 0
    
    while True:
        row,col,dir = walking_tiles[-1]
        #stampa(grid,row,col,dir)
        #print()
        new_row,new_col = row+M[dir][0],col+M[dir][1]
        if any([
            new_row <0,
            new_row >= len(grid),
            new_col <0,
            new_col > len(grid[0])
        ]):
            #end of labirinth!
            break
        if grid[new_row][new_col] == "#":
            new_dir = D[dir]
            walking_tiles.append([row,col,new_dir])
        else:
            new_walking = [new_row,new_col,dir]
            walking_tiles.append(new_walking)
            new_tyle = [row,col]
            if new_tyle not in visited_tiles: visited_tiles.append(new_tyle)
    

    visited_tiles.append([row,col])
    import concurrent.futures
    def process_tile(tile):
        new_grid = make_new_grid(grid, tile)
        if is_loop(new_grid):
            return 1
        return 0
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_tile, visited_tiles))

    loop = sum(results)
    
    return loop
    


if __name__ == "__main__":
    test = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")