from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional, Dict, Self, Set
from dataclasses import dataclass, field
from math import gcd


CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

@dataclass
class Node:
    row: int
    col: int
    
    
    def __str__(self):
        return f"row: {self.row}, col: {self.col}"
    
    def __repr__(self):
        return f"row: {self.row}, col: {self.col}"
    
    def __format__(self, format_spec):
        return f"row: {self.row}, col: {self.col}"
    
    def __eq__(self, other: Self):
        return (self.row == other.row) and (self.col == other.col)

    def q1(self, other: Self):
        # return true if self is in q1 from other
        if (self.row <= other.row) and (self.col < other.col):
            return True
        return False
    
    def q2(self, other: Self):
        # return true if self is in q2 from other
        if (self.row < other.row) and (self.col >= other.col):
            return True
        return False

    def q3(self, other: Self):
        # return true if self is in q3 from other
        if (self.row >= other.row) and (self.col > other.col):
            return True
        return False
            
    def q4(self, other: Self):
        # return true if self is in q4 from other
        if (self.row > other.row) and (self.col <= other.col):
            return True
        return False
    
    def __hash__(self):
        return self.row * 10000 + self.col 

@dataclass
class Antenna(List[Node]):
    a_type: str
    antinodes: Optional[Set[Node]] = field(default_factory=set)
    max_row: Optional[int] = 0
    max_col: Optional[int] = 0
    v2: Optional[bool] =  False
    
    
    def is_valid_node(self, node: Node) -> bool:
        if all([ node.row >= 0,
                 node.col >= 0,
                 node.row <= self.max_row,
                 node.col <= self.max_col
                 ]):
            return True
        return False
    
    
    def add_antinodes(self, one: Node, two: Node):
        if not self.v2:
            antinode1 : Node= Node(2*one.row - two.row, 2*one.col - two.col)
            antinode2 : Node= Node(2*two.row - one.row, 2*two.col - one.col)
            
            
            if self.is_valid_node(antinode1):
                #print(f"      antinode1 valid")
                self.antinodes.add(antinode1)
                
            if self.is_valid_node(antinode2):
                #print(f"      antinode2 valid")
                self.antinodes.add(antinode2)
        else:
            # logic for v2
            dr = two.row - one.row
            dc = two.col - one.col
            g = gcd(abs(dr), abs(dc))
            ur = dr//g
            uc = dc//g
            # rows interval 0 <= one.row + n*ur <= max_row
            # cols interval 0 <= one.col + n*uc <= max_col
            n = 0
            while True:
                row = one.row + n*ur
                col = one.col + n*uc
                antinode = Node(row,col)
                if self.is_valid_node(antinode):
                    self.antinodes.add(antinode)
                    n += 1
                else:
                    break
            
            n = -1 
            while True:
                row = one.row + n*ur
                col = one.col + n*uc
                antinode = Node(row,col)
                if self.is_valid_node(antinode):
                    self.antinodes.add(antinode)
                    n -= 1
                else:
                    break

            
    
    def post_append(self, node: Node):
        #print(f"Post append for {node}")
        if len(self) == 1:
            pass
        for other in self[:-1]:
            #print("  evaluating antinodes")
            self.add_antinodes(node, other)
    
    def add_antenna(self, node: Node):
        self.append(node)
        self.post_append(node)
    
    def __str__(self):
        return f"Nodes: {self}, type: {self.a_type}, antinodes: {self.antinodes}"
    
    def __repr__(self):
        return f"{self}, type: {self.a_type}, antinodes: {self.antinodes}"
    
    def __format__(self, format_spec):
        return f"[{[(n.row, n.col) for n in self]}]"

@dataclass
class Antennas(Dict[str,Antenna]):
    max_row: Optional[int] = 0
    max_col: Optional[int] = 0
    v2: bool = False
    

    def __new_antenna(self, antenna_type: str, node: Node):
        self[antenna_type] = Antenna(a_type=antenna_type, max_row=self.max_row, max_col=self.max_col, v2=self.v2)
        self.__update_antenna(antenna_type, node)
    
    def __update_antenna(self, antenna_type: str, node: Node):
        self[antenna_type].add_antenna(node)        
    
    def add(self, antenna_type: str, row: int, col: int):
        if antenna_type in self:
            self.__update_antenna(antenna_type, Node(row,col))
        else:
            self.__new_antenna(antenna_type, Node(row,col))

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    antennas: Antennas = Antennas()
    rows: List[str] = inputs_1.splitlines()
    max_row = len(rows) - 1
    max_col = len(rows[0]) - 1
    antennas.max_row = max_row
    antennas.max_col = max_col
    for row,line in enumerate(rows):
        for col,char in enumerate(list(line)):
            if char != ".":
                antennas.add(char,row,col)
    
    all_nodes : List[Node] = [node for antenna in antennas.values() for node in antenna]
    all_antinodes: Set[Node] = set([node for antenna in antennas.values() for node in antenna.antinodes])
        
    return len(all_antinodes)
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    antennas: Antennas = Antennas()
    rows: List[str] = inputs_1.splitlines()
    max_row = len(rows) - 1
    max_col = len(rows[0]) - 1
    antennas.max_row = max_row
    antennas.max_col = max_col
    antennas.v2 = True
    for row,line in enumerate(rows):
        for col,char in enumerate(list(line)):
            if char != ".":
                antennas.add(char,row,col)
    
    all_nodes : List[Node] = [node for antenna in antennas.values() for node in antenna]
    all_antinodes: Set[Node] = set([node for antenna in antennas.values() for node in antenna.antinodes])
        
    return len(all_antinodes)


if __name__ == "__main__":
    test = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")