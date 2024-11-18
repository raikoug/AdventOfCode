from starter import AOC, CURRENT_YEAR
from pathlib import Path
from hashlib import md5

class TooHigh(Exception):
    pass

class AlreadyEvaluated(Exception):
    pass

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    seed = inputs_1
    i = 0
    code = ""
    while True:
        res = md5(f"{seed}{i}".encode()).hexdigest()
        if res.startswith("00000"):
            code += res[5]
            print(f"Trovato! {code}")
            if len(code) == 8:
                return code
        
        i += 1 
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    seed = inputs_1
    i = 0
    found = 0
    code = [None]*8
    while True:
        res = md5(f"{seed}{i}".encode()).hexdigest()
        i += 1
        if res.startswith("00000"):
            print(f"Found  a good hash: {res}")
            try:
                pos = int(res[5])
                if pos > 7: raise TooHigh
                if code[pos] != None: raise AlreadyEvaluated
            except ValueError as e:
                print(f"    Discarded because char {res[5]} is not int")
            except TooHigh as e:
                print(f"    Discarded index {pos} is too high")
            except AlreadyEvaluated as e:
                print(f"    Discarded index {pos} is not {None}: {code[pos]}")
            else:
                code[pos] = res[6]
                found += 1
                print(f"    code is now {code}")
                if found == 8:
                    print(f"        Finished!")
                    return "".join(code)
                
            
            
if __name__ == "__main__":
    #print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")