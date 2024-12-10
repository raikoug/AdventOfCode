import pygame
import sys
from queue import Queue
from starter import AOC, CURRENT_YEAR
from pathlib import Path
import time


CURRENT_DAY = 10
aoc = AOC(CURRENT_YEAR)
pygame.init()

not_visited = {
    
}

inputs_1 = aoc.get_input(CURRENT_DAY, 1)
grid = [[int(el) for el in line] for line in inputs_1.splitlines()]

# Parametri finestra
CELL_SIZE =15
ROWS = len(grid)
COLS = len(grid[0])
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animazione Percorso")

# Contatore visite celle (r,c)
visit_count = {}

def color_for_zero_height(visits):
    # Gradient dal chiaro allo scuro per 9 visite
    R_start, G_start, B_start = (30,129,176)
    R_end, G_end, B_end = (10,10,20)
    steps = 9
    v = min(visits, steps)
    if steps > 1:
        R = int(R_start + (R_end - R_start)*(v-1)/(steps-1))
        G = int(G_start + (G_end - G_start)*(v-1)/(steps-1))
        B = int(B_start + (B_end - B_start)*(v-1)/(steps-1))
    else:
        R,G,B = R_start,G_start,B_start
    return (R,G,B)

def height_to_color(h, visits=0):
    if visits == 0:
        if h == 0:
            return (0,204,204)
        elif h == 1:
            return (208,255,216)
        elif h == 2:
            return (195,255,106)
        elif h == 3:
            return (182,255,196)
        elif h == 4:
            return (169,255,186)
        elif h == 5:
            return (156,255,176)
        elif h == 6:
            return (143,255,166)
        elif h == 7:
            return (130,255,156)
        elif h == 8:
            return (117,255,135)
        elif h == 9:
            return (254,107,64)
    else:
        if h == 0:
            return (0,204,204)
        return color_for_zero_height(visits)

def draw_grid():
    for r in range(ROWS):
        for c in range(COLS):
            rect = pygame.Rect(c*CELL_SIZE, r*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            h = grid[r][c]
            visits = visit_count.get((r,c), 0)
            color = height_to_color(h, visits)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (50,50,50), rect, 1)
    pygame.display.flip()

def possible_next_steps(row, col):
    moves = [(1,0),(-1,0),(0,1),(0,-1)]
    res = []
    max_r = len(grid)-1
    max_c = len(grid[0])-1
    for dr,dc in moves:
        nr,nc = row+dr, col+dc
        if 0 <= nr <= max_r and 0 <= nc <= max_c:
            if grid[nr][nc] == grid[row][col] + 1:
                res.append((nr,nc))
    return res

start_points = []
for r in range(ROWS):
    for c in range(COLS):
        if grid[r][c] == 0:
            start_points.append((r,c))  # Usa un punto di partenza noto, assicurati che abbia h=0
# Se vuoi usare quelli dalla griglia:
# start_points = []
# for r in range(ROWS):
#     for c in range(COLS):
#         if grid[r][c] == 0:
#             start_points.append((r,c))

draw_grid()

clock = pygame.time.Clock()
running = True
queue = Queue()
time.sleep(5)
# Loop principale
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for sp in start_points:
        queue.put(sp)
        while not queue.empty():
            current = queue.get()
            visit_count[current] = visit_count.get(current, 0) + 1
            r,c = current
            next_steps = possible_next_steps(r,c)
            for ns in next_steps:
                queue.put(ns)
            draw_grid()
        clock.tick(1000)
    print("start point finiti")
    time.sleep(10)
    break
    

pygame.quit()
sys.exit()
