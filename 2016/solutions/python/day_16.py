from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def create_disk(start: str, lenght: int) -> str:
    # start IS less than lenght if we are here
    a = start
    b = "".join(["0" if el == "1" else "1" for el in start[::-1]])
    new = f"{a}0{b}"
    if len(new) < lenght:
        return create_disk(new, lenght)
    return new[:lenght]

def checksum(data: str):
    return "".join(["1" if el in ["11","00"] else "0" for el in [f"{data[i]}{data[i+1]}" for i in range(0,len(data),2)]])
    

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    disk = create_disk(inputs_1, 272)
    while True:
        disk = checksum(disk)
        if len(disk) % 2 == 1:
            break
    return disk
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    disk = create_disk(inputs_1, 35651584)
    while True:
        disk = checksum(disk)
        if len(disk) % 2 == 1:
            break
    return disk


if __name__ == "__main__":
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")