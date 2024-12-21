from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
from functools import lru_cache

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def parse(src: str) -> List[str]:
    return [line for line in src.splitlines() if line != '']

def distance(start, end):
    return end[0] - start[0], end[1] - start[1]

numeric_coord = {
    'A': (2, 3),
    '0': (1, 3),
    '1': (0, 2),
    '2': (1, 2),
    '3': (2, 2),
    '4': (0, 1),
    '5': (1, 1),
    '6': (2, 1),
    '7': (0, 0),
    '8': (1, 0),
    '9': (2, 0)
}

coord_numeric = {
    (2, 3): 'A',
    (1, 3): '0',
    (0, 2): '1',
    (1, 2): '2',
    (2, 2): '3',
    (0, 1): '4',
    (1, 1): '5',
    (2, 1): '6',
    (0, 0): '7',
    (1, 0): '8',
    (2, 0): '9'
}

direction_coord = {
    'A': (2, 0),
    '^': (1, 0),
    '>': (2, 1),
    'v': (1, 1),
    '<': (0, 1)
}

coord_direction = {
    (2, 0): 'A',
    (1, 0): '^',
    (2, 1): '>',
    (1, 1): 'v',
    (0, 1): '<'
}

@lru_cache(None)
def move(button, next_button, numeric):
    if button == next_button:
        return 'A'
    if numeric:
        button_coord = numeric_coord
        coord_button = coord_numeric
    else:
        button_coord = direction_coord
        coord_button = coord_direction
    first_coord = button_coord[button]
    next_coord = button_coord[next_button]
    dx, dy = distance(first_coord, next_coord)
    if dx >= 0:
        move_x = '>' * dx
    else:
        move_x = '<' * -dx
    if dy >= 0:
        move_y = 'v' * dy
    else:
        move_y = '^' * -dy
    if dx == 0:
        return move_y + 'A'
    elif dy == 0:
        return move_x + 'A'
    r = []
    if (next_coord[0], first_coord[1]) in coord_button:
        r.append(move_x + move_y + 'A')
    if (first_coord[0], next_coord[1]) in coord_button:
        r.append(move_y + move_x + 'A')
    if len(r) != 2 or dx < 0:
        return r[0]
    return r[1]

@lru_cache(None)
def get_sequence_length(sequence, indirection, numeric):
    if indirection == 0:
        return len(sequence)
    sequence = 'A' + sequence
    total = 0
    for b, nb in zip(sequence, sequence[1:]):
        total += get_sequence_length(move(b, nb, numeric), indirection - 1, False)
    return total

def solve_1(test_string: Optional[str] = None) -> int:
    data = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    inner_robots = 2
    return sum(get_sequence_length(code, inner_robots + 1, True) * int(code[:-1]) for code in parse(data))

def solve_2(test_string: Optional[str] = None) -> int:
    data = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    inner_robots = 25
    return sum(get_sequence_length(code, inner_robots + 1, True) * int(code[:-1]) for code in parse(data))

if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")
