from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    s: str = inputs_1
    i = 0
    new_line = ""
    while True:
        if s[i] == "(":
            i+=1
            chars=""
            times=""
            flag=False
            while True:
                if s[i].isdigit() and (not flag):
                    chars+= s[i]
                elif s[i].isdigit() and flag:
                    times += s[i]
                elif s[i] =="x":
                    flag = True
                else: # s[i] == ")":
                    break
                i += 1
            # i index is on ")" now
            chars = int(chars)
            times = int(times)
            # chars will start from +1...+chars
            new_line += s[i+1:i+chars+1]*times
            i = i+chars
        else:
            new_line += s[i]
        i+=1
        if i >= len(s):
            break
    return len(new_line)
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # new approach
    # Each char has value of 1.
    s = inputs_1
    total  = 0
    v = [1]*len(inputs_1)
    i = 0
    while True:
        if s[i] != "(":
            total += v[i]
            i+=1
            if i >= len(v):
                break
            
            continue
        
        # s[i] = "("
        i+=1
        start = i
        while s[i] != ")":
            i += 1
        # s[i] = ")"
        pattern = s[start:i]
        lenght,times = pattern.split("x")
        lenght = int(lenght)
        times =  int(times)
        i+=1 
        for j in range(i,i+lenght):
            v[j] *= times
        
        # apply pattern to lenght of next s char, times times
        #print(v)
        if i >= len(v):
            break
            
    return total


if __name__ == "__main__":
    test1 = """(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN"""
    #print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")