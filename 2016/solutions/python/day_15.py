from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

class Disk():
    n: int
    module: int
    initial: int
    state: int
    
    def __init__(self, n: int, module: int,
                       initial: int):
        self.n = n
        self.module = module
        self.initial = initial
        self.state = initial
        self.rotate(n)
    
    def rotate(self, n: int):
        self.state = (self.state + n) % self.module

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # let's ingore the rotation, offest each disk with his position
    disks : List[Disk] = list()
    for line in inputs_1.splitlines():
        _, h, _, module, _, _, _, _, _, _, _, initial = line.split(" ")
        n = int(h.replace("#", ""))
        module = int(module)
        initial = int(initial.replace(".", ""))
        disk: Disk = Disk(n,module,initial)
        disks.append(disk)
    # math is for nooooobs, let's rotate all disk untill all are state 0!!!!!!!
    time = 0
    while True:
        time += 1
        states = list()
        for disk in disks:
            disk.rotate(1)
            states.append(disk.state)
        #print(f"Time: {time} - states: {states}")
        if sum(states) == 0:
            # win!
            break
    return time
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # let's ingore the rotation, offest each disk with his position
    disks : List[Disk] = list()
    for line in inputs_1.splitlines():
        _, h, _, module, _, _, _, _, _, _, _, initial = line.split(" ")
        n = int(h.replace("#", ""))
        module = int(module)
        initial = int(initial.replace(".", ""))
        disk: Disk = Disk(n,module,initial)
        disks.append(disk)
    disks.append(Disk(n+1,11,0))
    # math is for nooooobs, let's rotate all disk untill all are state 0!!!!!!!
    time = 0
    while True:
        time += 1
        states = list()
        for disk in disks:
            disk.rotate(1)
            states.append(disk.state)
        #print(f"Time: {time} - states: {states}")
        if sum(states) == 0:
            # win!
            break
    return time


if __name__ == "__main__":
    test = """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")