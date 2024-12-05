from collections import deque
from icecream import ic
import heapq

D = {
    "n": (-1, 0),
    "s": (1, 0),
    "e": (0, 1),
    "w": (0, -1),
}

class Tyle:
    type: str
    row: int
    col: int
    neighbors: dict
    feasible_neighbors: list
    best_steps: int
    hashing: int   #have to add an hasing unique for set XD
    is_visited: bool

    def __init__(self, type, row, col, hashing):
        self.type = type
        self.row = row
        self.col = col
        self.neighbors = dict()
        self.best_steps = 1e9
        self.feasible_neighbors = list()
        self.hashing = hashing
        self.is_visited = False

    def add_neighbor(self, direction, neighbor):
        self.neighbors[direction] = neighbor

    def __hash__(self):  # here is the set magic... -.-'
        return self.hashing

    def __lt__(self, other):
        return self.best_steps < other.best_steps
    
    def __gt__(self, other):
        return self.best_steps > other.best_steps
    
    def __eq__(self, other):
        try:
            return self.best_steps == other.best_steps
        except:
            ic(self, other, type(self), type(other))
            import sys; sys.exit(0)
    
    def __le__(self, other):
        return self.best_steps <= other.best_steps
    
    def __ge__(self, other):
        return self.best_steps >= other.best_steps
    
    def __ne__(self, other):
        return self.best_steps != other.best_steps
    
    def clone(self):
        return Tyle(self.type, self.row, self.col, self.hashing)

    def is_rock(self):
        return self.type == '#'
    
    def is_garden_plot(self):
        return self.type in ['.', 'S']

    def __str__(self):
        return self.type
    
    def __repr__(self):
        return self.__str__()
    
    def pretty_print(self):
        """
        printed in the form
         ----   N.type    ----
        W.type,self.type,E.type
         ----   S.type    ----
        """
        res =  f" {self.neighbors['n'].type if 'n' in self.neighbors else ""} \n"
        res += f"{self.neighbors['w'].type if 'w' in self.neighbors else " "}{self.type}{self.neighbors['e'].type if 'e' in self.neighbors else " "}\n"
        res += f" {self.neighbors['s'].type if 's' in self.neighbors else " "} \n"
        print(res)

class Grid:
    f: list
    end_tyles: set
    visited: set
    current_tyle_hash = int
    all_tyles = set
    coords = set

    def __init__(self, tf):
        self.end_tyles = set()
        self.visited = set()
        self.all_tyles = set()
        self.current_tyle_hash = 0
        self.coords = set()
        self.init_grid(tf)

    def __str__(self):
        res = ""
        for row in self.f:
            for col in row:
                res += str(col)
            res += "\n"
        return res

    def __repr__(self):
        return self.__str__()

    def reset(self):
        self.end_tyles = set()
        self.visited = set()
        for t in self.all_tyles:
            t.is_visited = False
            t.best_steps = 1e9
        
    
    def print_with_end_tyles(self):
        for row in self.f:
            for col in row:
                if col in self.end_tyles:
                    print("O", end="")
                else:
                    print(col, end="")
            print()

    def add_visited(self, tyle)-> bool:
        """
        return True if tyle has not been visited and add it to list
            else return False, and the code should continue to next step
        """
        self.visited.add(tyle)

    def p2_neighbord(self, tyle) -> list:
        """
        return a list of neighbors that are feasible, but in an infinite grid where grid is repeated ininitely
        """
        for d in D.values():
            n_row = tyle.row + d[0]
            n_col = tyle.col + d[1]
            mod_row = n_row % len(self.f)
            mod_col = n_col % len(self.f[0])
            if (n_row, n_col) not in self.coords:
                self.coords.add((n_row, n_col))
                the_tyle = Tyle(self.f[mod_row][mod_col], mod_row, mod_col, self.current_tyle_hash)
                self.all_tyles.add(the_tyle)
                self.current_tyle_hash += 1
            else:
                the_tyle = self.f[mod_row][mod_col]

            if isinstance(the_tyle, str):
                ic(the_tyle, type(the_tyle), mod_row, mod_col, n_row, n_col)
                import sys; sys.exit(0)
                
            try:
                if the_tyle.is_garden_plot():
                    yield the_tyle
            except Exception as e:
                ic(the_tyle, type(the_tyle), e, mod_row, mod_col, n_row, n_col)
                import sys; sys.exit(0)

    def init_grid(self,tf):
        grid = list()
        self.current_tyle_hash = 0
        for ri,row in enumerate(tf):
            tmp_row = list()
            for ci,col in enumerate(row):
                tmp_tyle = Tyle(col, ri, ci, self.current_tyle_hash)
                self.all_tyles.add(tmp_tyle)
                self.coords.add((ri,ci))
                self.current_tyle_hash += 1
                tmp_row.append(tmp_tyle)
                if col == "S":
                    start = [ri,ci]
            grid.append(tmp_row)
        
        self.f = grid
        self.calc_neighbors()
        self.start = grid[start[0]][start[1]]

    def calc_neighbors(self):
        for ri,row in enumerate(self.f):
            for ci,col in enumerate(row):
                for r,d in D.items():
                    n_row = ri + d[0]
                    n_col = ci + d[1]
                    if n_row < 0 or n_col < 0:
                        continue
                    try:
                        neighbor = self.f[n_row][n_col]
                        col.add_neighbor(r, neighbor)
                        if neighbor.is_garden_plot():
                            col.feasible_neighbors.append(neighbor)
                    except IndexError:
                        pass
            

def part_1(grid: Grid, max_steps: int, neigh_override = None)-> int:
    Q = [[0, grid.start]]
    total = 0
    ic("start")
    while Q:
        step, tyle = heapq.heappop(Q)

        if step > max_steps:
            # I use heapq, then if here the step is > to max_steps
            #   i know all the others do
            break

        if tyle.is_visited:
            continue

        if step%2 == 0:
            total += 1

        tyle.is_visited = True

        if neigh_override != None:
            neighbors = neigh_override(tyle)
        else:
            neighbors = tyle.feasible_neighbors
        for t in neighbors:
            heapq.heappush(Q, [step+1, t])
    
    #grid.print_with_end_tyles()
    return total



if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    test = False
    tf = aoc_utils.get_day_input(day, test)
    steps_to_take = 6 if test else 64
    grid = Grid(tf)
    part_1_res = part_1(grid, steps_to_take)

    W, H = len(tf[0]), len(tf)
    
    ic(part_1_res)

    grid.reset()

    mod = 26501365 % H

    a = part_1(grid, mod, grid.p2_neighbord)
    ic(a)
    b = part_1(grid, mod+H, grid.p2_neighbord)
    c = part_1(grid, mod+H*2, grid.p2_neighbord)

    diff1 = b-a
    diff2 = c-b
    diff3 = diff2-diff1

    # quadradic sequence
    A = diff3//2
    B = diff1 - 3*A
    C = a - A - B
    fc = lambda x: A*x**2 + B*x + C

    from math import ceil
    part_2_res = fc(ceil(26501365%H))
    ic(part_2_res)
    


    
    
    
    
    
    
    
    
    
    
    
    
    
        

    