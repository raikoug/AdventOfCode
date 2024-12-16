from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional, Tuple
from dataclasses import dataclass, field
import os
from time import sleep

def clear_screen(): 
    os.system('cls' if os.name == 'nt' else 'clear')

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

M = {
    "^": (-1,0),
    ">": (0,1),
    "v": (1,0),
    "<": (0,-1)
}

@dataclass
class Warehouse:
    @dataclass
    class Point:
        row: int = 0
        col: int = 0
    
    @dataclass
    class Robot:
        row: int = 0
        col: int = 0
        
        def __str__(self) -> str:
            return "🤖"
        
        def __repr__(self):
            return self.__str__()
        
        def __format__(self, format_spec):
            return self.__str__()
        
        
    
    @dataclass
    class Box:
        row: int = 0
        col: int = 0  # per part2 consideriamo questa come la cella sinistra del box
        
        def __str__(self) -> str:
            return "🧺"
        
        def __repr__(self):
            return self.__str__()
        
        def __format__(self, format_spec):
            return self.__str__()
        
    @dataclass
    class Wall:
        row: int = 0
        col: int = 0
        
        def __str__(self) -> str:
            return "🧱"
        
        def __repr__(self):
            return self.__str__()
        
        def __format__(self, format_spec):
            return self.__str__()
    
    @dataclass
    class Empty:
        row: int = 0
        col: int = 0
        
        def __str__(self) -> str:
            return "  "
        
        def __repr__(self):
            return self.__str__()
        
        def __format__(self, format_spec):
            return self.__str__()
    
    
    
    max_row: int = 0
    max_col: int = 0
    robot: Robot = field(default_factory=Robot)
    boxes: List[Box] = field(default_factory=list)
    walls: List[Wall] = field(default_factory=list)
    instructions: str = ""
    actual_move: int = 0
    grid: List[List[Robot|Wall|Box|Empty]] = field(default_factory=list)
    part2: bool = False  # default False per la parte 1

    def add_wall(self, row, col):
        if not self.part2:
            self.walls.append(Warehouse.Wall(row,col))
            self.grid[row][col] = self.walls[-1]
            return
        #part2
        self.walls.append(Warehouse.Wall(row,col))
        self.grid[row][col]  = self.walls[-1]
        self.grid[row][col+1] = self.walls[-1]

    
    def add_box(self, row, col):
        if not self.part2:
            # Parte 1: box 1 cella
            self.boxes.append(Warehouse.Box(row,col))
            self.grid[row][col] = self.boxes[-1]
            return
        #part2
        self.boxes.append(Warehouse.Box(row,col))
        self.grid[row][col]   = self.boxes[-1]
        self.grid[row][col+1] = self.boxes[-1]


        
    def add_empty(self, row, col):
        if not self.part2:
            self.grid[row][col] = Warehouse.Empty(row,col)
            return
        #part2
        self.grid[row][col]   = Warehouse.Empty(row,col)
        self.grid[row][col+1] = Warehouse.Empty(row,col)

            
    def set_robot(self, row, col):
        if not self.part2:
            self.robot =  Warehouse.Robot(row,col)
            self.grid[row][col] = self.robot
            return
        #part2
        self.robot =  Warehouse.Robot(row,col)
        self.grid[row][col] = self.robot
        self.grid[row][col+1] = Warehouse.Empty(row,col)

    
    def can_push(self, box: Box, m: Tuple[int,int]):
        if not self.part2:
            next_place = self.grid[box.row+m[0]][box.col+m[1]]
        
            if isinstance(next_place, Warehouse.Box):
                return self.can_push(next_place, m)
            elif isinstance(next_place, Warehouse.Wall):
                return False
            elif isinstance(next_place, Warehouse.Empty):
                return True
        
        # siamo alla parte 2
        # se il movimento è orizzontale, rimaniamo sulla stessa row
        if m[0] == 0:
            # il box ha sempre come coordinate il posto più a sinistra, quindi in caso si vada a destra...
            next_place = self.grid[box.row+m[0]][box.col+m[1]]
            if next_place is box:
                next_place = self.grid[next_place.row+m[0]][next_place.col+m[1]]
            
            if isinstance(next_place, Warehouse.Box):
                return self.can_push(next_place, m)
            elif isinstance(next_place, Warehouse.Wall):
                return False
            elif isinstance(next_place, Warehouse.Empty):
                return True
        
        # siamo alla parte 2 con verticale...
        # il box è fatto di 2 pezzi [XY] e la coordinato di `box` è la X
        # controllo sia sopra/sotto X che Y
        next_place_X = self.grid[box.row+m[0]][box.col+m[1]]
        next_place_Y = self.grid[box.row+m[0]][box.col+1+m[1]]
        
        if isinstance(next_place_X, Warehouse.Wall) or isinstance(next_place_Y, Warehouse.Wall):
            return False
        possible_boxes : List[Warehouse.Box] = list()
        if isinstance(next_place_X, Warehouse.Box):
            possible_boxes.append(next_place_X)
        if isinstance(next_place_Y, Warehouse.Box):
            possible_boxes.append(next_place_Y)
        
        if len(possible_boxes) == 0:
            return True
        
        return all([self.can_push(box,m) for box in possible_boxes])
            
        
        
    def move_box_to(self, box: Box, m: Tuple[int,int]):
        # CALL THIS ONLY IF CAN PUSH IS TRUE! no more checks here, broken is broken!
        old_row = box.row
        old_col = box.col
        new_row = old_row + m[0]
        new_col = old_col + m[1]
        self.grid[new_row][new_col] =  box
        box.row = new_row
        box.col = new_col
        self.grid[old_row][old_col] = Warehouse.Empty(old_row,old_col)
    
    def move_robot_to(self, m):
        new_row = self.robot.row + m[0]
        new_col = self.robot.col + m[1]
        old_row = self.robot.row
        old_col = self.robot.col
        self.grid[new_row][new_col] =  self.robot
        self.robot.row = new_row
        self.robot.col = new_col
        self.grid[old_row][old_col] = Warehouse.Empty(old_row,old_col)
        
    
    def get_last_box(self, actual_place: Box|Robot, m: Tuple[int,int]) -> Box|Robot:
        next_place = self.grid[actual_place.row+m[0]][actual_place.col+m[1]]
        if isinstance(next_place, Warehouse.Box):
            return self.get_last_box(next_place, m)
        elif isinstance(next_place, Warehouse.Empty):
            return actual_place
    
    def reverse_push(self, m:Tuple[int,int]):
        last_box: Warehouse.Box|Warehouse.Robot = self.get_last_box(self.robot,m)
        while not isinstance(last_box, Warehouse.Robot):
            self.move_box_to(last_box, m)
            last_box: Warehouse.Box|Warehouse.Robot = self.get_last_box(self.robot,m)
        self.move_robot_to(m)
        
    def move(self):
        m: Tuple[int,int] = M[self.instructions[self.actual_move]]
        self.actual_move += 1
        next_place = self.grid[self.robot.row + m[0]][self.robot.col + m[1]]
        can_move: bool = False
        if isinstance(next_place, Warehouse.Box):
            can_move = self.can_push(next_place,m)
            if not can_move:
                return 
            
            #part 2 tests
            
            
            self.reverse_push(m)
            return 
        if isinstance(next_place, Warehouse.Wall):
            return
        if isinstance(next_place, Warehouse.Empty):
            self.move_robot_to(m)
        return can_move
    
    def start(self):
        while self.actual_move < len(self.instructions):
            self.move()
            #self.stampa()
    
    def calculate_boxes(self) -> int:
        total = 0
        for box in self.boxes:
            total += (box.row * 100) + box.col
        return total
    
    def stampa(self):
        for line in self.grid:
            for el in line:
                print(el, end= "")
            print()


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    splitted = inputs_1.splitlines()
    max_row = len(splitted[0])
    max_col = len(splitted[0])
    w = Warehouse()
    w.grid = [[" " for _ in range(max_col)] for _ in range(max_row)]
    w.max_row = max_row
    maze = True
    for row,line in enumerate(splitted):
        if ">" in line:
            maze = False

        if maze:
            for col,char in enumerate(line):
                if    char == "#": w.add_wall(row,col)
                elif  char == "O": w.add_box(row,col)
                elif  char == "@": w.set_robot(row,col)
                elif  char == ".": w.add_empty(row,col)
        else:
            w.instructions += line
    
    #w.stampa()
    w.start()  # usa i metodi originali parte 1
    return w.calculate_boxes()
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    splitted = inputs_1.splitlines()
    splitted = inputs_1.splitlines()
    max_row = len(splitted[0])
    max_col = len(splitted[0])
    w = Warehouse(part2=True, max_row = max_row, max_col=max_col*2)
    w.grid = [[" " for _ in range(max_col*2)] for _ in range(max_row)]

    maze = True
    for row,line in enumerate(splitted):
        if (">" in line) or ("<" in line) or ("^" in line) or ("v" in line):
            maze = False

        if maze:
            for col,char in enumerate(line):
                if    char == "#": w.add_wall(row,col*2)
                elif  char == "O": w.add_box(row,col*2)
                elif  char == "@": w.set_robot(row,col*2)
                elif  char == ".": w.add_empty(row,col*2)
        else:
            w.instructions += line
    
    w.stampa()
    w.start()
    w.stampa()
    return w.calculate_boxes()


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    test_v2 = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""

    test_v3 = """#######
#...#.#
#.....#
#.@OO.#
#..O..#
#.....#
#######

>>v<<^^<<^^
"""
    test_up_1 = """#######
#...#.#
#.....#
#..OO.#
#..O@.#
#.....#
#######

^^^^
"""

    test_up_2 = """#######
#...#.#
#...O.#
#..OO.#
#..O@.#
#.....#
#######

^^
"""
    # part 2 not yet visually implemented
    #print(f"Part 2: {solve_2(test_up_1)}")
