from starter import AOC, CURRENT_YEAR
from pathlib import Path
from queue import PriorityQueue

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def is_wall(x: int,y: int,m: int):
    if ((bin((x*x + 3*x + 2*x*y + y + y*y) + m).count("1")) % 2) == 0:
        return False
    return True

def around_me(x: int,y: int, diagonal = False) -> list:
    res = list()
    #mosse certe
    res.append([x+1,y])
    res.append([x,y+1])
    
    if x >= 0: res.append([x-1,y])
    if y >= 0 : res.append([x,y-1])
    if diagonal:
        #mosse certe
        res.append([x+1,y+1])
        
        if x >= 0: res.append([x,y])
        if y >= 0: res.append([x,y])
        if (x >= 0) and (y >= 0): res.append([x,y])
    
    return res

Distance: float = lambda x1,y1,x2,y2: ((x2-x1)**2 + (y2-y1)**2)**0.5
    
Priority: float = lambda steps,distance: distance/steps

    
def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    dx, dy = 31,39
    magic = int(inputs_1)
    q = PriorityQueue()
    visited = list()
    # queue will have items with: [priority,(x,y),steps_until_now]
    # priority will be the key to be fast XD (I hope..)
    q.put([0,(1,1),1])
    
    while 1:
        priority, points, steps = q.get()
        x,y = points
        new_steps = steps + 1
        for el in around_me(x,y):
            if el == [dx,dy]:
                return steps
            if is_wall(*el, magic):
                continue
            if el in visited:
                continue
            d = Distance(*el, dx, dy)
            p = Priority(new_steps, d)
            q.put([p, el, new_steps])
            visited.append(el)
        
    
    return 1

def stampa(visited,m):
    for y in range(30):
        for x in range(30):
            if [x,y] in visited:
                print(".", end="")
            elif is_wall(x,y,m):
                print("#", end="")
            else:
                print(" ", end="")
        print()

def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    magic = int(inputs_1)
    q = PriorityQueue()
    visited = list()
    visited.append([1,1])
    # queue will have items with: [steps,(x,y)]
    # priority will be the key to be fast XD (I hope..)
    q.put([0,(1,1)])
    
    while 1:
        steps, points = q.get()
        x,y = points
        new_steps = steps + 1
        if new_steps == 50:
            break
        for el in around_me(x,y):
            if el in visited:
                continue
            if is_wall(*el, magic):
                continue
            q.put([new_steps, el])
            visited.append(el)
        
    
    return len(visited) - 1 # ????


if __name__ == "__main__":
    t = "10"
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")