from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def rotate(in_data: list, times: int, direction: str) -> str:
    data = list(in_data)
    times = times % (len(data))
    if direction == "r":
        for i in range(times):
            data = [data.pop(-1)] + data
    elif direction == "l":
        for i in range(times):
            data = data + [data.pop(0)]
    return data
        
        

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # tes is abcde, prod is abcdefgh
    password = list("abcdefgh")
    passlen = len(password)
    for line in inputs_1.splitlines():
        if line.startswith("swap position"):
            #swap position X with position Y
            _, _, X, _, _, Y = line.split(" ")
            X, Y = int(X), int(Y)
            password[X], password[Y] = password[Y], password[X]
        elif line.startswith("swap letter"):
            #swap position X with position Y
            _, _, X, _, _, Y = line.split(" ")
            for i in range(passlen):
                if password[i] == X:
                    password[i] = Y
                elif password[i] == Y:
                    password[i] = X
        elif line.startswith("rotate based"):
            #rotate based on position of letter e
            _, _, _, _, _, _, letter = line.split(" ")
            rotation = password.index(letter)
            if rotation >= 4: rotation += 2
            else:             rotation += 1
            password = rotate(password, rotation, "r")
        elif line.startswith("rotate"):
            #rotate right 3 steps
            _, direction, times, _,= line.split(" ")
            direction = direction[0]
            rotation = int(times)
            password = rotate(password, rotation, direction)
        elif line.startswith("reverse positions"):
            #reverse positions X through Y (inclusive)
            _, _, X, _, Y = line.split(" ")
            X, Y = int(X), int(Y)+1
            password = password[:X] + password[X:Y][::-1] + password[Y:]
        elif line.startswith("move position"):
            #move position X to position Y
            _, _, X, _, _, Y = line.split(" ")
            X, Y = int(X), int(Y)
            letter = password.pop(X)
            password.insert(Y,letter)
    
    return "".join(password)
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # tes is abcde, prod is abcdefgh
    password = list("fbgdceah")
    passlen = len(password)
    for line in inputs_1.splitlines()[::-1]:
        if line.startswith("swap position"):
            #swap position X with position Y
            _, _, X, _, _, Y = line.split(" ")
            X, Y = int(X), int(Y)
            password[X], password[Y] = password[Y], password[X]
        elif line.startswith("swap letter"):
            #swap position X with position Y
            _, _, X, _, _, Y = line.split(" ")
            for i in range(passlen):
                if password[i] == X:
                    password[i] = Y
                elif password[i] == Y:
                    password[i] = X
        elif line.startswith("rotate based"):
            # bastardo!
            #rotate based on position of letter e
            _, _, _, _, _, _, letter = line.split(" ")
            what_if = list(password)
            while True:
                what_if = rotate(what_if, 1, "l")
                
                rotation = what_if.index(letter)
                if rotation >= 4: rotation += 2
                else:             rotation += 1
                
                if rotate(what_if,rotation,"r") == password:
                    break
            password = list(what_if)
        elif line.startswith("rotate"):
            #rotate right 3 steps
            _, direction, times, _,= line.split(" ")
            direction = direction[0]
            direction = "r" if direction == "l" else "l"
            rotation = int(times)
            password = rotate(password, rotation, direction)
        elif line.startswith("reverse positions"):
            #reverse positions X through Y (inclusive)
            _, _, X, _, Y = line.split(" ")
            X, Y = int(X), int(Y)+1
            password = password[:X] + password[X:Y][::-1] + password[Y:]
        elif line.startswith("move position"):
            #move position X to position Y
            # the reverse would be
            #move position Y to position X
            _, _, X, _, _, Y = line.split(" ")
            Y, X = int(X), int(Y)
            letter = password.pop(X)
            password.insert(Y,letter)
    
    return "".join(password)


if __name__ == "__main__":
    test = """swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")