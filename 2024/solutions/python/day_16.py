from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional, Set, Dict
from dataclasses import dataclass, field
import heapq
import os
from time import sleep

def clear_screen(): 
    os.system('cls' if os.name == 'nt' else 'clear')

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

@dataclass
class Point:
    row:int
    col:int
    
    def __hash__(self) -> int:
        return self.row*100000 + self.col
    
    def __eq__(self, other: 'Point') -> bool:
        return (self.row == other.row) and (self.col == other.col)
    
    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.row+other.row,self.col+other.col)
    
    def __floordiv__(self, other: 'Point') -> float:
        return ((other.row-self.row)**2 + (other.col-self.col)**2)**0.5
    
    def __lt__(self, other: 'Point') -> bool:
        return (self.row < other.row) or (self.row == other.row and self.col < other.col)

    def __le__(self, other: 'Point') -> bool:
        return self < other or self == other

    def __gt__(self, other: 'Point') -> bool:
        return (self.row > other.row) or (self.row == other.row and self.col > other.col)

    def __ge__(self, other: 'Point') -> bool:
        return self > other or self == other
    
    def from_grid(self, grid: List[List[str]]) -> str:
        return grid[self.row][self.col]
    
    def __str__(self) -> str:
        return str(self.row) + "," + str(self.col)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __format__(self, format_spec) -> str:
        return self.__str__()
    

@dataclass
class NextPoint:
    point: Point
    direc: Point
    cost : int
    char : str


D = [
    Point(1,0),
    Point(0,1),
    Point(-1,0),
    Point(0,-1)
]

fake_huge_cost = 100000000000000000000000000000000000000000

visited: Dict[Point,int] = dict()

def next_points(score: int, loc: Point, face: Point, grid: Dict[Point,str],
                path: List[Point], queue) -> List[NextPoint]:
    result : List[NextPoint] = list()
    
    for d in D:
        if grid.get(loc+d,'#')=='#': continue
        cost = 1001 if d!=face else 1
        if visited.get((loc+d,d),float("inf")) > score+cost:
            heapq.heappush(queue, (score+cost, loc+d, d, path+[loc+d]))
        
    
    return queue


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    splitted = inputs_1.splitlines()
    grid: Dict[Point,str] = {Point(x,y):c for y,r in enumerate(splitted) for x,c in enumerate(r)}
    start = next(z for z in grid if grid[z]=='S')
    end = next(z for z in grid if grid[z]=='E')
    best = set()
    low = float("inf")
    
    queue = [(0, start, Point(0,1), [start])]
    
    while queue:
        score, loc, face, path = heapq.heappop(queue)
        if score>low: break
        if loc == end:
            if low>score: best.clear()
            low = score
            best |= set(path)
        visited[loc,face] = score

        queue = next_points(score,loc,face,grid,path,queue)
    
    return low, len(best)
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
        
    return 1


if __name__ == "__main__":
    test = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""
    test_2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""
    part_1, part_2 = solve_1()
    print(f"Part 1: {part_1}")
    print(f"Part 2: {part_2}")