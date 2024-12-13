import pygame
import random
import string
from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional, Self, Set
from dataclasses import dataclass, field
from queue import PriorityQueue
from collections import defaultdict
from time import sleep

CURRENT_DAY = 12
aoc = AOC(CURRENT_YEAR)

cell_size = 7
BG_COLOR = (255,255,255)
VISITED_COLOR = (165, 224, 27) # color for visited cells
CURRENT_AREA_COLOR = (255, 0, 238) # color for cells currently being processed in the area
BORDER_COLOR = (232, 169, 169) 
BORDEAUX_COLOR = (128,0,0)  # color for the perimeter borders of completed areas
DELAY = 1

random.seed(42)
COLOR_MAP = {}
for ch in string.ascii_uppercase:
    COLOR_MAP[ch] = (random.randint(100,255), random.randint(100,255), random.randint(100,255))

@dataclass
class Point:
    row: int
    col: int
    char: str
    
    def __hash__(self):
        return self.row*1000000+self.col
    
    def __eq__(self, other: Self):
        return (self.row == other.row) and (self.col == other.col)

    def __lt__(self, other: Self):
        return (self.row < other.row) and (self.col < other.col)
    
    def __gt__(self, other: Self):
        return (self.row > other.row) and (self.col > other.col)

def draw_cell(screen, point: Point, color, cell_size, border=True):
    # Draw a single cell with the specified color.
    # If border=True, a border is drawn around the cell.
    rect = pygame.Rect(point.col*cell_size, point.row*cell_size, cell_size, cell_size)
    pygame.draw.rect(screen, color, rect)
    if border:
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
    return rect

def initialize_screen(grid, screen, cell_size):
    # Draw the initial state of the grid: all cells are drawn with their base color.
    rows = len(grid)
    cols = len(grid[0])
    screen.fill(BG_COLOR)
    update_rects = []
    for r in range(rows):
        for c in range(cols):
            p = Point(r,c,grid[r][c])
            base_color = COLOR_MAP.get(p.char, BG_COLOR)
            rect = draw_cell(screen, p, base_color, cell_size)
            update_rects.append(rect)
    pygame.display.update(update_rects)

def list_neighbors(grid, point: Point):
    # Return all valid orthogonal neighbors of the given point.
    row = point.row
    col = point.col
    res: List[Point] = list()
    
    if row > 0:
        res.append(Point(row-1,col,grid[row-1][col]))
    if col < (len(grid[0]) -1):
        res.append(Point(row,col+1,grid[row][col+1]))
    if row < (len(grid) -1):
        res.append(Point(row+1,col,grid[row+1][col]))
    if col > 0:
        res.append(Point(row,col-1,grid[row][col-1]))
    return res

def get_first_non_visited(grid: List[List[int]], visited: Set[Point]):
    # Find the first cell in the grid that is not in the visited set.
    for row,line in enumerate(grid):
        for col,char in enumerate(line):
            point = Point(row, col, char)
            if point not in visited:
                return point

def count_sides_of(area: List[Point]) -> int:
    # Count the corners of the region's perimeter to adjust the area perimeter calculation.
    reg = {(p.row, p.col) for p in area}

    left = set()
    right = set()
    up = set()
    down = set()
    
    for (r, c) in reg:
        if (r - 1, c) not in reg:
            up.add((r, c))
        if (r + 1, c) not in reg:
            down.add((r, c))
        if (r, c + 1) not in reg:
            right.add((r, c))
        if (r, c - 1) not in reg:
            left.add((r, c))

    corners = 0
    # upper corners
    for (r, c) in up:
        if (r, c) in left:
            corners += 1
        if (r, c) in right:
            corners += 1
        if (r - 1, c - 1) in right and (r, c) not in left:
            corners += 1
        if (r - 1, c + 1) in left and (r, c) not in right:
            corners += 1

    # lower corners
    for (r, c) in down:
        if (r, c) in left:
            corners += 1
        if (r, c) in right:
            corners += 1
        if (r + 1, c - 1) in right and (r, c) not in left:
            corners += 1
        if (r + 1, c + 1) in left and (r, c) not in right:
            corners += 1

    return corners

def draw_bordeaux_borders(screen, area: List[Point], grid, cell_size):
    # Draw the bordeaux borders around the perimeter of the completed area.
    reg = {(p.row, p.col) for p in area}
    update_rects = []

    for p in area:
        x = p.col * cell_size
        y = p.row * cell_size
        # Check each side of the cell and if it's a perimeter side, draw a bordeaux line.
        # up
        if p.row == 0 or (p.row - 1, p.col) not in reg:
            pygame.draw.line(screen, BORDEAUX_COLOR, (x, y), (x + cell_size, y), 2)
        # down
        if p.row == len(grid)-1 or (p.row + 1, p.col) not in reg:
            pygame.draw.line(screen, BORDEAUX_COLOR, (x, y + cell_size), (x + cell_size, y + cell_size), 2)
        # left
        if p.col == 0 or (p.row, p.col - 1) not in reg:
            pygame.draw.line(screen, BORDEAUX_COLOR, (x, y), (x, y + cell_size), 2)
        # right
        if p.col == len(grid[0])-1 or (p.row, p.col + 1) not in reg:
            pygame.draw.line(screen, BORDEAUX_COLOR, (x + cell_size, y), (x + cell_size, y + cell_size), 2)

        update_rects.append(pygame.Rect(x, y, cell_size, cell_size))
    
    pygame.display.update(update_rects)

def solve_1(test_string = None, visualize_steps=False):
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    grid = inputs_1.splitlines()
    
    current_point = Point(0,0, grid[0][0])
    current_area: List[Point] = [current_point]
    visited: Set[Point] = set()
    q = PriorityQueue()
    q.put([current_point,current_area])
    current_fences = 0  
    total = 0
    max_visited = len(grid)*len(grid[0])

    if visualize_steps:
        pygame.init()
        rows = len(grid)
        cols = len(grid[0])
        screen = pygame.display.set_mode((cols*cell_size, rows*cell_size))
        pygame.display.set_caption("Garden Visualization")
        
        # Draw the initial full grid
        initialize_screen(grid, screen, cell_size)
    else:
        screen = None

    while len(visited) < max_visited:
        if visualize_steps:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return total

        current_point, current_area = q.get()
        visited.add(current_point)

        # If visualizing, update only the currently visited cell
        if visualize_steps and screen:
            rect = draw_cell(screen, current_point, VISITED_COLOR, cell_size)
            pygame.display.update(rect)
            if DELAY > 0:
                pygame.time.delay(DELAY)

        neighbors = list_neighbors(grid,current_point)
        current_fences += 4 - len(neighbors)
        
        for neighbor in neighbors:
            if neighbor.char != current_point.char:
                current_fences += 1
                continue
            
            if neighbor in current_area:
                continue
            
            if neighbor.char == current_point.char:
                current_area.append(neighbor)
                q.put([neighbor,current_area])
                # If visualizing, highlight the new cell in the current area color
                if visualize_steps and screen:
                    rect = draw_cell(screen, neighbor, CURRENT_AREA_COLOR, cell_size)
                    pygame.display.update(rect)
                    if DELAY > 0:
                        pygame.time.delay(DELAY)

        if q.empty():
            # Completed area
            total += current_fences * len(current_area)
            current_fences = 0

            # All cells in the area become "visited" without internal borders
            if visualize_steps and screen:
                update_rects = []
                for p in current_area:
                    rect = draw_cell(screen, p, VISITED_COLOR, cell_size, border=False)
                    update_rects.append(rect)
                pygame.display.update(update_rects)
                if DELAY > 0:
                    pygame.time.delay(DELAY)
                
                # Draw the bordeaux borders around the completed area
                draw_bordeaux_borders(screen, current_area, grid, cell_size)
                if DELAY > 0:
                    pygame.time.delay(DELAY)

            current_area.clear()
            
            new_point = get_first_non_visited(grid,visited)
            if new_point is None:
                break
            current_area.append(new_point)
            q.put([new_point,current_area])
            
            # If visualizing, highlight the new starting cell of the next area
            if visualize_steps and screen and new_point:
                rect = draw_cell(screen, new_point, CURRENT_AREA_COLOR, cell_size)
                pygame.display.update(rect)
                if DELAY > 0:
                    pygame.time.delay(DELAY)

        print(f"Percent complete: {((len(visited)/max_visited)*100):0.2f}%", end="\r")

    print()
    if visualize_steps and screen:
        pygame.time.delay(2000)
        pygame.quit()
    return total


if __name__ == "__main__":
    test_1 = """OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""
    print(f"Part 1: {solve_1(visualize_steps=True)}")
