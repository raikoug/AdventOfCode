from starter import AOC, CURRENT_YEAR
from pathlib import Path
from queue import PriorityQueue

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    #print("Initializing IPs...")
    #available_ips = [True] * (2 ** 32)
    #print("Ips Initialized...")
    
    minmax = [[int(line.split("-")[0]),int(line.split("-")[1])] for line in inputs_1.splitlines()]
    q = PriorityQueue()
    for couple in minmax:
        q.put(couple)
    
    best = 0
    
    while not q.empty():
        lower, higher = q.get()
        if lower <= best <= higher:
            best = higher + 1
        
    
    return best
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    print("Initializing IPs...")
    available_ips = [True] * (2 ** 32)
    print("Ips Initialized...")
    print("Initializing Ranges...")
    lines = [[int(line.split("-")[0]),int(line.split("-")[1])] for line in inputs_1.splitlines()]
    print("Ranges Initialized...")
    total = len(lines)
    
    
    i = 0
    for line in lines:
        lower, higher = line
        number = (higher - lower) + 1
        
        available_ips[lower:higher+1] = [False] * number
        i += 1
        print(f"Elbaorated {i: >5} lines out of {total}", end="\r")
    print()
    return sum(available_ips)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")