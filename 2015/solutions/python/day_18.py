from starter import AOC, CURRENT_YEAR
from pathlib import Path
import pygame as pg

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

TILE_ON = f'{Path(__file__).parent}/assets/1.gif'
TILE_OFF = f'{Path(__file__).parent}/assets/2.gif'
TILE_FADED = f'{Path(__file__).parent}/assets/3.gif'

TITLE = "Conway's Game of Life"
WINDOW_SIZE = 800

class Grid:
    def __init__(self, surface, cell_size, s, v2: bool):
        self.surface = surface
        self.cell_size = cell_size
        self.width = len(s.splitlines()[0])
        self.height = len(s.splitlines())
        self.v2 = v2
        
        self.grid = [[1 if el == "#" else 0 for el in list(l)] for l in s.splitlines()]
        # if v2, the corner leds are stuck :D
        if self.v2:
            self.grid[0][0]   = 1
            self.grid[0][-1]  = 1
            self.grid[-1][0]  = 1
            self.grid[-1][-1] = 1
        
        self.alives = sum([sum(l) for l in self.grid])

        # Carica e ridimensiona le immagini dei tiles
        self.tile_on = pg.transform.scale(pg.image.load(TILE_ON), (cell_size, cell_size))
        self.tile_off = pg.transform.scale(pg.image.load(TILE_OFF), (cell_size, cell_size))
        self.tile_faded = pg.transform.scale(pg.image.load(TILE_FADED), (cell_size, cell_size))


    
    def update(self):
        new_grid = [[0 for _ in range(self.height)] for _ in range(self.width)]
        self.alives = 0
        for x in range(self.width):
            for y in range(self.height):
                # Conta i vicini vivi
                live_neighbors = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if self.grid[nx][ny] == 1:
                                live_neighbors += 1

                if self.grid[x][y] == 1:
                    if live_neighbors < 2 or live_neighbors > 3:
                        new_grid[x][y] = 0  
                    else:
                        new_grid[x][y] = 1
                        self.alives += 1
                else:
                    if live_neighbors == 3:
                        new_grid[x][y] = 1
                        self.alives += 1
                    else:
                        new_grid[x][y] = 0
        if self.v2:
            if new_grid[0][0]   == 0: self.alives += 1
            if new_grid[0][-1]  == 0: self.alives += 1
            if new_grid[-1][0]  == 0: self.alives += 1
            if new_grid[-1][-1] == 0: self.alives += 1
            new_grid[0][0]   = 1
            new_grid[0][-1]  = 1
            new_grid[-1][0]  = 1
            new_grid[-1][-1] = 1
        
        self.grid = new_grid

    def draw(self):
        for x in range(self.width):
            for y in range(self.height):
                pos = (x * self.cell_size, y * self.cell_size)
                if self.grid[x][y] == 1:
                    self.surface.blit(self.tile_on, pos)
                else:
                    self.surface.blit(self.tile_off, pos)

class Game:
    def __init__(self, s: str, v2: bool = False):
        pg.init()
        self.clock = pg.time.Clock()
        pg.display.set_caption(TITLE)
        self.surface = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.loop = True
        self.width = len(s.splitlines()[0])
        self.height = len(s.splitlines())

        # Calcola la dimensione di ogni cella
        self.cell_size = WINDOW_SIZE // self.width

        # Crea la griglia
        self.grid = Grid(self.surface, self.cell_size, s, v2)

    def main(self):
        
        self.surface.fill((0, 0, 0))
        self.handle_events()
        self.grid.draw()
        pg.display.update()
        self.clock.tick(100)
        
        i = 1
        while self.loop:
            self.surface.fill((0, 0, 0))
            self.handle_events()
            self.grid.update()
            self.grid.draw()
            pg.display.update()
            self.clock.tick(100)  # Imposta il frame rate a 10 FPS
            if i == 100:
                print(f"Iteration {i:>4}: Alives {self.grid.alives:>05}")
                break
            i +=1 
        
        import time
        time.sleep(10)
        pg.quit()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.loop = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.loop = False
            elif event.type == pg.MOUSEBUTTONUP:
                pos = pg.mouse.get_pos()
                x = pos[0] // self.cell_size
                y = pos[1] // self.cell_size
                # Inverte lo stato della cella cliccata
                self.grid.grid[x][y] = 1 if self.grid.grid[x][y] == 0 else 0


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    game = Game(inputs_1)
    print(f"Grid Alives: {game.grid.alives}")
    game.main()

    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    game = Game(inputs_1,True)
    print(f"Grid Alives: {game.grid.alives}")
    game.main()


if __name__ == "__main__":
    test_case = """##.#.#
...##.
#....#
..#...
#.#..#
####.#"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")