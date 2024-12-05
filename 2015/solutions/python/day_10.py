from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    for k in range(40):
        old = ""
        times = 0
        new_string = ""
        i = 0
        while True:
            if i == 0:
                old = inputs_1[i]
                times = 1
                i += 1
                continue
            
            if i == len(inputs_1):
                new_string += f"{times}{old}"
                break
            
            c = inputs_1[i]
            if c == old:
                times +=1
            elif c != old:
                new_string += f"{times}{old}"
                old = c
                times = 1
            
            i += 1
        
        inputs_1 = new_string
        
    return len(new_string)
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    for k in range(50):
        old = ""
        times = 0
        new_string = ""
        i = 0
        while True:
            if i == 0:
                old = inputs_1[i]
                times = 1
                i += 1
                continue
            
            if i == len(inputs_1):
                new_string += f"{times}{old}"
                break
            
            c = inputs_1[i]
            if c == old:
                times +=1
            elif c != old:
                new_string += f"{times}{old}"
                old = c
                times = 1
            
            i += 1
        
        inputs_1 = new_string
        
    return len(new_string)


if __name__ == "__main__":
    print(solve_2())