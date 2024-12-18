from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional, Set
from dataclasses import dataclass, field
from queue import PriorityQueue
import numpy as np
from queue import Queue


CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)


def in_boundaries(point, size):
    """Verifica se un punto è dentro i confini della griglia."""
    x, y = point
    return 0 <= x < size and 0 <= y < size

def navigate_grid(grid, start, end):
    """Trova il percorso più breve dalla partenza alla fine."""
    size = grid.shape[0]
    queue = Queue()
    queue.put((start, 0))
    visited = set()
    visited.add(start)

    while not queue.empty():
        (x, y), steps = queue.get()

        # Controlla se abbiamo raggiunto la destinazione
        if (x, y) == end:
            return steps

        # Esplora i vicini
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if in_boundaries((nx, ny), size) and grid[ny, nx] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.put(((nx, ny), steps + 1))

    return -1  # Nessun percorso trovato


def solve_1(test_string = None, maxytes: int = 0) -> int:
    size = 71 if not test_string else 7
    maxytes = maxytes if maxytes else 1024
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    
    def read_input(data: str, size:int, corrupted:int):
        """Legge i dati e costruisce la lista delle coordinate."""
        grid = np.zeros((size, size), dtype=int)
        for line in data.splitlines()[0:corrupted]:
            col, row = map(int, line.split(","))
            grid[row, col] = 1  # 1 rappresenta un ostacolo
        return grid
    
    grid = read_input(inputs_1,size,maxytes)
    # Definisci i punti di partenza e arrivo
    start = (0, 0)
    end = (size - 1, size - 1)

    # Trova il percorso più breve
    return navigate_grid(grid, start, end)
    
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    total_bytes = len(inputs_1.splitlines())
    # brute force
    #for i in range(1024,total_bytes):
    #    if solve_1(maxytes=i) < 0:
    #        return inputs_1.splitlines()[i]
    
    #smart?
    top = total_bytes
    low = 1024
    old_half = 1024
    while True:
        half = (top+low) // 2
        if old_half == half: return inputs_1.splitlines()[half]
        print(f"Testing {half: >5}")
        if solve_1(maxytes=half) < 0:
            # under half!
            top = half
        else:
            # over half!
            low = half
        
        old_half = half
        
        
        

if __name__ == "__main__":
    test = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")