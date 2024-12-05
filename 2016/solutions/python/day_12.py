from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    instructions: List[str] = [line for line in inputs_1.split("\n") if line]
    register = {'a': 0, 'b': 0, 'c': 0, 'd': 0}
    place = 0
    while True:
        if "inc" in instructions[place]:
            _, reg = instructions[place].split(" ")
            register[reg] += 1
            place += 1
        if "dec" in instructions[place]:
            _, reg = instructions[place].split(" ")
            register[reg] -= 1
            place += 1
        elif "cpy" in instructions[place]:
            _, source, dest = instructions[place].split(" ")
            try:
                val = int(source)
            except:
                val = register[source]
            register[dest] = val
            place += 1
        elif "jnz" in instructions[place]:
            _, source, jmp = instructions[place].split(" ")
            try:
                val = int(source)
            except:
                val = register[source]
            if val == 0:
                place += 1
            else:
                jmp = int(jmp)
                place += jmp
                
        if place >= len(instructions):
            break

    return register["a"]
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    instructions: List[str] = [line for line in inputs_1.split("\n") if line]
    register = {'a': 0, 'b': 0, 'c': 1, 'd': 0}
    place = 0
    while True:
        if "inc" in instructions[place]:
            _, reg = instructions[place].split(" ")
            register[reg] += 1
            place += 1
        if "dec" in instructions[place]:
            _, reg = instructions[place].split(" ")
            register[reg] -= 1
            place += 1
        elif "cpy" in instructions[place]:
            _, source, dest = instructions[place].split(" ")
            try:
                val = int(source)
            except:
                val = register[source]
            register[dest] = val
            place += 1
        elif "jnz" in instructions[place]:
            _, source, jmp = instructions[place].split(" ")
            try:
                val = int(source)
            except:
                val = register[source]
            if val == 0:
                place += 1
            else:
                jmp = int(jmp)
                place += jmp
                
        if place >= len(instructions):
            break

    return register["a"]


if __name__ == "__main__":
    test = """cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")