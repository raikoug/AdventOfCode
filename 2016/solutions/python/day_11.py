from starter import AOC, CURRENT_YEAR
from pathlib import Path
import re
from itertools import chain, combinations
from collections import deque, Counter


CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

# I DIDNT like this problem AT ALL, now is 2024 and I decided I didn't need to
#   solve this myself.. :D
# THIS is not mine, credits to Edd Mann https://eddmann.com/
# https://eddmann.com/posts/advent-of-code-2016-day-11-radioisotope-thermoelectric-generators/

def parse_floors(input):
    return [set(re.findall(r'(\w+)(?:-compatible)? (microchip|generator)', line))
            for line in input.splitlines()]

def is_valid_transition(floor):
    return len(set(type for _, type in floor)) < 2 or \
           all((obj, 'generator') in floor
               for (obj, type) in floor
               if type == 'microchip')

def next_states(state):
    moves, elevator, floors = state

    possible_moves = chain(combinations(floors[elevator], 2), combinations(floors[elevator], 1))

    for move in possible_moves:
        for direction in [-1, 1]:
            next_elevator = elevator + direction
            if not 0 <= next_elevator < len(floors):
                continue

            next_floors = floors.copy()
            next_floors[elevator] = next_floors[elevator].difference(move)
            next_floors[next_elevator] = next_floors[next_elevator].union(move)

            if (is_valid_transition(next_floors[elevator]) and is_valid_transition(next_floors[next_elevator])):
                yield (moves + 1, next_elevator, next_floors)

def is_all_top_level(floors):
    return all(not floor
               for number, floor in enumerate(floors)
               if number < len(floors) - 1)

def min_moves_to_top_level(floors):
    seen = set()
    queue = deque([(0, 0, floors)])

    while queue:
        state = queue.popleft()
        moves, _, floors = state

        if is_all_top_level(floors):
            return moves

        for next_state in next_states(state):
            if (key := count_floor_objects(next_state)) not in seen:
                seen.add(key)
                queue.append(next_state)

def count_floor_objects(state):
    _, elevator, floors = state
    return elevator, tuple(tuple(Counter(type for _, type in floor).most_common()) for floor in floors)


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    
    return min_moves_to_top_level(parse_floors(inputs_1))

    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    floors = parse_floors(inputs_1)
    floors[0] = floors[0].union([('elerium', 'generator'), ('elerium', 'microchip'),
                                 ('dilithium', 'generator'), ('dilithium', 'microchip')])
    return min_moves_to_top_level(floors)


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")