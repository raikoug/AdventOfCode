from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

V = {
    "<" : (-1, 0),
    "^" : (+0, -1),
    "v" : (+0, +1),
    ">" : (+1, +0)
}

def vector_sum(a,b):
    return (a[0]+b[0], a[1]+b[1])


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    nodes = dict()
    current_node = (0,0)
    nodes[(current_node)] = 0
    for mov in inputs_1:
        v = V[mov]
        new_node = vector_sum(current_node,v)
        if new_node not in nodes:
            nodes[(new_node)] = 0
        else:
            nodes[(new_node)] += 1
        current_node = new_node
        
    return len(nodes)
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    nodes = dict()
    current_node = (0,0)
    nodes[(current_node)] = 0
    santas_houses = inputs_1[0::2]
    robosantas_houses = inputs_1[1::2]
    for mov in santas_houses:
        v = V[mov]
        new_node = vector_sum(current_node,v)
        if new_node not in nodes:
            nodes[(new_node)] = 0
        else:
            nodes[(new_node)] += 1
        current_node = new_node
    current_node = (0,0)
    for mov in robosantas_houses:
        v = V[mov]
        new_node = vector_sum(current_node,v)
        if new_node not in nodes:
            nodes[(new_node)] = 0
        else:
            nodes[(new_node)] += 1
        current_node = new_node
    return len(nodes)


if __name__ == "__main__":
    print(solve_2())