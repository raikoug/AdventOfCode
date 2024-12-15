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
        col: int = 0
        
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
    grid: List[List[Robot|Wall|Box|str]] = field(default_factory=list)

    def add_wall(self, row, col):
        self.walls.append(Warehouse.Wall(row,col))
        self.grid[row][col] = self.walls[-1]
    
    def add_box(self, row, col):
        self.boxes.append(Warehouse.Box(row,col))
        self.grid[row][col] = self.boxes[-1]
        
    def add_empty(self, row, col):
        self.grid[row][col] = Warehouse.Empty(row,col)
        
    def set_robot(self, row, col):
        self.robot =  Warehouse.Robot(row,col)
        self.grid[row][col] = self.robot
    
    def can_push(self, box: Box, m: Tuple[int,int]):
        next_place = self.grid[box.row+m[0]][box.col+m[1]]
        if isinstance(next_place, Warehouse.Box):
            return self.can_push(next_place, m)
        elif isinstance(next_place, Warehouse.Wall):
            return False
        elif isinstance(next_place, Warehouse.Empty):
            return True
        
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
        #print(f"   get_last_box: actual_place: {actual_place}, {actual_place.row},{actual_place.col}")
        next_place = self.grid[actual_place.row+m[0]][actual_place.col+m[1]]
        #print(f"   get_last_box: next_place: {next_place}, {next_place.row},{next_place.col}")
        if isinstance(next_place, Warehouse.Box):
            return self.get_last_box(next_place, m)
        elif isinstance(next_place, Warehouse.Empty):
            #print(f"     get_last_box: empty found, returning it!")
            return actual_place
    
    def reverse_push(self, m:Tuple[int,int]):
        # I get last box, and swap it with empty space, the again, again..
        #print("Getting last box")
        last_box: Warehouse.Box|Warehouse.Robot = self.get_last_box(self.robot,m)
        #print(f"last_box: {last_box}, {last_box.row},{last_box.col}")
        while not isinstance(last_box, Warehouse.Robot):
            #print(f" reverse_push: pushing last_box {last_box}, {last_box.row},{last_box.col} to {m}")
            self.move_box_to(last_box, m)
            #print(f" reverse_push: pushed last box:")
            #self.stampa()
            last_box: Warehouse.Box|Warehouse.Robot = self.get_last_box(self.robot,m)
            
        # robot turnn!
        #print(f"reverse_push: Robot turn!")
        self.move_robot_to(m)
        #print(f"reverse_push: Robot moved!")
        #self.stampa()
        
            
    
    def move(self):
        #print(f"Next move: {self.instructions[self.actual_move]}")
        m: Tuple[int,int] = M[self.instructions[self.actual_move]]
        self.actual_move += 1
        next_place = self.grid[self.robot.row + m[0]][self.robot.col + m[1]]
        can_move: bool = False
        if isinstance(next_place, Warehouse.Box):
            can_move = self.can_push(next_place,m)
            if not can_move:
                return 
            
            self.reverse_push(m)
            return 
        
        if isinstance(next_place, Warehouse.Wall):
            return
        
        if isinstance(next_place, Warehouse.Empty):
            self.move_robot_to(m)
        return can_move
    
    def start(self):
        #clear_screen()
        while self.actual_move < len(self.instructions):
            #clear_screen()
            #print(f"Actual move: {self.instructions[self.actual_move]}")
            self.move()    
            #self.stampa()
            #sleep(0.05)
            #input("Press enter to continue!")
    
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
    
    w.stampa()
    w.start()
    return w.calculate_boxes()
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
        
    return 1


if __name__ == "__main__":
    test = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""
    mini_test = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")