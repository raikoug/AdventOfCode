from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import Self

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)


class Pos:
    x: int
    y: int
    
    def __init__(self, clone: Self = None):
        if clone:
            self.x = clone.x
            self.y = clone.y
        else:
            self.x = 0
            self.y = 0
    
    def move_x(self, delta: int) -> None:
        self.x += delta
    
    def move_y(self, delta: int) -> None:
        self.y += delta
    
    def __str__(self) -> str:
        return f"x: {self.x}, y: {self.y}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def __format__(self, _) -> str:
        return self.__str__()  
    
    def __eq__(self, other: Self):
        return (self.x == other.x) and (self.y == other.y)
    
    
    

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    pos = Pos()
    movements = inputs_1.split(", ")
    direction = "N"
    while movements:
        move = movements.pop(0)
        move_dir = move[0]
        move_dis = int(move[1:])
        if direction == "N":  # NORTH
            if move_dir == "R":
                direction = "E"
            elif move_dir == "L":
                direction = "O"
        elif direction == "S": # SOUTH
            if move_dir == "R":
                direction = "O"
            elif move_dir == "L":
                direction = "E"
        elif direction == "E": # EAST
            if move_dir == "R":
                direction = "S"
            elif move_dir == "L":
                direction = "N"
        elif direction == "O": # OVEST
            if move_dir == "R":
                direction = "N"
            elif move_dir == "L":
                direction = "S"
        
        if direction ==   "N" : 
            pos.move_y(move_dis)
        elif direction == "E" : 
            pos.move_x(move_dis)
        elif direction == "S" : 
            pos.move_y(-move_dis)
        elif direction == "O" : 
            pos.move_x(-move_dis)
        
        
        #print(f"direction: {direction}, move: {move}, move_dir: {move_dir}, move_dis: {move_dis}, new_post: {pos}")
    
    # the taxicab distance between p=(p1,p2) and q=(q1,q2) is |p1−q1|+|p2−q2| 
    res = abs(0-pos.x)+abs(0-pos.y)
    
    return res
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    pos = Pos()
    visited = list()
    visited.append(Pos(pos))
    movements = inputs_1.split(", ")
    direction = "N"
    found = False
    while movements:
        move = movements.pop(0)
        move_dir = move[0]
        move_dis = int(move[1:])
        if direction == "N":  # NORTH
            if move_dir == "R":
                direction = "E"
            elif move_dir == "L":
                direction = "O"
        elif direction == "S": # SOUTH
            if move_dir == "R":
                direction = "O"
            elif move_dir == "L":
                direction = "E"
        elif direction == "E": # EAST
            if move_dir == "R":
                direction = "S"
            elif move_dir == "L":
                direction = "N"
        elif direction == "O": # OVEST
            if move_dir == "R":
                direction = "N"
            elif move_dir == "L":
                direction = "S"
        
        if direction ==   "N" : 
            for i in range(move_dis):
                pos.move_y(1)
                if pos in visited: 
                    found = True
                    break
                else: visited.append(Pos(pos))
        elif direction == "E" : 
            for i in range(move_dis):
                pos.move_x(1)
                if pos in visited: 
                    found = True
                    break
                else: visited.append(Pos(pos))
        elif direction == "S" : 
            for i in range(move_dis):
                pos.move_y(-1)
                if pos in visited: 
                    found = True
                    break
                else: visited.append(Pos(pos))
        elif direction == "O" : 
            for i in range(move_dis):
                pos.move_x(-1)
                if pos in visited: 
                    found = True
                    break
                else: visited.append(Pos(pos))
        
        if found:
            break
        
        #print(f"direction: {direction}, move: {move}, move_dir: {move_dir}, move_dis: {move_dis}, new_post: {pos}")
    
    # the taxicab distance between p=(p1,p2) and q=(q1,q2) is |p1−q1|+|p2−q2| 
    res = abs(0-pos.x)+abs(0-pos.y)
    
    return res


if __name__ == "__main__":
    test = "R5, L5, R5, R3"
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")