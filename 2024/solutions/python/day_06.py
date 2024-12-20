from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Tuple, Optional, Set

CURRENT_DAY = int(Path(__file__).stem.replace('day_', ''))
aoc = AOC(CURRENT_YEAR)

# Direzioni: N, E, S, W
DIRECTIONS = ["^", ">", "v", "<"]
M = {
    "^": (-1, 0),
    ">": (0, 1),
    "v": (1, 0),
    "<": (0, -1)
}
D = {
    "^": ">",
    ">": "v",
    "v": "<",
    "<": "^"
}

def solve_1(test_string: Optional[str] = None, 
            grid: Optional[List[List[str]]] = None,
            start: Optional[Set[int]] = None) -> Tuple[List[List[str]], Set[Tuple[int, int]], Optional[Tuple[int, int]]]:
    if not grid:
        inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
        grid: List[List[str]] = [list(line) for line in inputs_1.splitlines()]
    
        # Utilizzo di set per posizioni visitate
        visited_tiles: Set[Tuple[int, int]] = set()
        # Utilizzo di set per stati visti
        seen_states: Set[Tuple[int, int, str]] = set()
        start: Set[int] = set()
        
        # Trova la posizione iniziale del guardiano
        start_found = False
        for i, row in enumerate(grid):
            try:
                guard_col = row.index("^")
                current_row, current_col, current_dir = i, guard_col, "^"
                visited_tiles.add((current_row, current_col))
                start = (current_row,current_col)
                # Aggiungi lo stato iniziale a seen_states
                seen_states.add((current_row, current_col, current_dir))
                # Sostituisci il simbolo del guardiano con un punto
                grid[i][guard_col] = '.'
                start_found = True
                break
            except ValueError:
                continue  # '^' non trovato in questa riga, continua alla successiva
    else:
        
        # Utilizzo di set per posizioni visitate
        visited_tiles: Set[Tuple[int, int]] = set()
        # Utilizzo di set per stati visti
        seen_states: Set[Tuple[int, int, str]] = set()
        current_row, current_col, current_dir = start[0], start[1], "^"
        visited_tiles.add((current_row, current_col))
        seen_states.add((current_row, current_col, current_dir))
        start_found = True
    
    if not start_found:
        raise ValueError("Guardiano non trovato nella mappa.")
    
    while True:
        # Calcola la nuova posizione basata sulla direzione attuale
        delta_row, delta_col = M[current_dir]
        new_row = current_row + delta_row
        new_col = current_col + delta_col
        
        # Verifica se il guardiano esce dalla mappa
        if (new_row < 0 or new_row >= len(grid) or
            new_col < 0 or new_col >= len(grid[0])):
            break  # Fine del percorso
        
        # Controlla se c'è un ostacolo
        if grid[new_row][new_col] == "#":
            # Gira a destra
            current_dir = D[current_dir]
        else:
            # Muovi il guardiano avanti
            current_row, current_col = new_row, new_col
            # Controlla se lo stato corrente è già stato visto
            current_state = (current_row, current_col, current_dir)
            if current_state in seen_states:
                # Loop rilevato
                return [], set(), list()  # Lista vuota come risultato
            # Aggiungi lo stato a seen_states
            seen_states.add(current_state)
            # Aggiungi la nuova posizione a visited_tiles
            visited_tiles.add((current_row, current_col))
    
    return grid, visited_tiles, start

def generate_new_grid(grid: List[List[str]], place: Set[int]) -> List[List[str]]:
    pass

def solve_2(grid: List[List[str]], visited: Set[int], start: Set[int]) -> int:
    visited.discard(start)
    loops = 0
    max_visited = len(visited)
    for i,point in enumerate(visited):
        print(f"Evaluating position {i+1: >3} of {max_visited}", end="")
        grid[point[0]][point[1]] = "#"
        # do stufff
        _, result, _ = solve_1(grid=grid,start=start)
        if not result:
            loops += 1
        #rollback
        print(f" Done! Looop count: {loops}", end="\r")
        grid[point[0]][point[1]] = "."
    print()
    return loops
    
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
    # Utilizzo del test input
    grid, visited, start = solve_1()
    if visited: 
        print(f"Part 1: {len(visited)}")
        print(f"Part 2: {solve_2(grid,visited, start)}")
        # Se vuoi visualizzare le posizioni visitate sulla griglia:
    else:
        print("Loop rilevato! Nessuna posizione unica restituita.")
