from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import Self, List, Dict

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

class Button:
    val: int
    U: Self
    R: Self
    D: Self
    L: Self
    
    def __init__(self, val):
        self.val = str(val)



def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    res = ""
    uno:     Button = Button(1)
    due:     Button = Button(2)
    tre:     Button = Button(3)
    quattro: Button = Button(4)
    cinque:  Button = Button(5)
    sei:     Button = Button(6)
    sette:   Button = Button(7)
    otto:    Button = Button(8)
    nove:    Button = Button(9)

    uno.U     = uno
    uno.R     = due
    uno.D     = quattro
    uno.L     = uno
    due.U     = due
    due.R     = tre
    due.D     = cinque
    due.L     = uno
    tre.U     = tre
    tre.R     = tre
    tre.D     = sei
    tre.L     = due
    quattro.U = uno
    quattro.R = cinque
    quattro.D = sette
    quattro.L = quattro
    cinque.U  = due
    cinque.R  = sei
    cinque.D  = otto
    cinque.L  = quattro
    sei.U     = tre
    sei.R     = sei
    sei.D     = nove
    sei.L     = cinque
    sette.U   = quattro
    sette.R   = otto
    sette.D   = sette
    sette.L   = sette
    otto.U    = cinque
    otto.R    = nove
    otto.D    = otto
    otto.L    = sette
    nove.U    = sei
    nove.R    = nove
    nove.D    = nove
    nove.L    = otto

    actual = cinque
    for line in inputs_1.splitlines():
        for move in line:
            if move == "R": actual = actual.R
            elif move == "L": actual = actual.L
            elif move == "D": actual = actual.D
            elif move == "U": actual = actual.U
        
        res += actual.val
        
    
    return res
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    res = ""
    uno:     Button = Button(1)
    due:     Button = Button(2)
    tre:     Button = Button(3)
    quattro: Button = Button(4)
    cinque:  Button = Button(5)
    sei:     Button = Button(6)
    sette:   Button = Button(7)
    otto:    Button = Button(8)
    nove:    Button = Button(9)
    A:       Button = Button("A")
    B:       Button = Button("B")
    C:       Button = Button("C")
    D:       Button = Button("D")
    

    uno.U     = uno
    uno.R     = uno
    uno.D     = tre
    uno.L     = uno
    due.U     = due
    due.R     = tre
    due.D     = sei
    due.L     = due
    tre.U     = uno
    tre.R     = quattro
    tre.D     = sette
    tre.L     = due
    quattro.U = quattro
    quattro.R = quattro
    quattro.D = otto
    quattro.L = tre
    cinque.U  = cinque
    cinque.R  = sei
    cinque.D  = cinque
    cinque.L  = cinque
    sei.U     = due
    sei.R     = sette
    sei.D     = A
    sei.L     = cinque
    sette.U   = tre
    sette.R   = otto
    sette.D   = B
    sette.L   = sei
    otto.U    = quattro
    otto.R    = nove
    otto.D    = C
    otto.L    = sette
    nove.U    = nove
    nove.R    = nove
    nove.D    = nove
    nove.L    = otto
    A.U    = sei
    A.R    = B
    A.D    = A
    A.L    = A
    B.U    = sette
    B.R    = C
    B.D    = D
    B.L    = A
    C.U    = otto
    C.R    = C
    C.D    = C
    C.L    = B
    D.U    = B
    D.R    = D
    D.D    = D
    D.L    = D
    
    actual = cinque
    for line in inputs_1.splitlines():
        for move in line:
            if move == "R": actual = actual.R
            elif move == "L": actual = actual.L
            elif move == "D": actual = actual.D
            elif move == "U": actual = actual.U
        
        res += actual.val
        
    
    return res

if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")