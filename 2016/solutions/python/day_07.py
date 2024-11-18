from starter import AOC, CURRENT_YEAR
from pathlib import Path
from re import findall

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

regex = r'(\w)(\w)\2\1'
regex2 = r'(\w)(\w)\1'

def abba_in_str(piece: str) -> bool:
    for el in findall(regex, piece):
        if el[0] != el[1]:
            return True
    return False
    
def check(line: str)-> bool:
    good = list()
    nook = list()
    tmp = ""
    parsing_g = True
    for char in line:
        if parsing_g: div = "["
        else: div = "]"
        if char == div:
            if parsing_g: good.append(tmp)
            else: nook.append(tmp)
            parsing_g = not parsing_g
            tmp = ""
        else:
            tmp += char
    
    if parsing_g: good.append(tmp)
    else: nook.append(tmp)
    #print(good, nook)
    
    can_go = False
    for piece in good:
        if abba_in_str(piece):
            can_go = True

    if not can_go:
        return False

    for piece in nook:
        if abba_in_str(piece):
            return False
    
    
    return True

def aba_in_str(piece: str) -> bool:
    for el in findall(regex2, piece):
        coppie = set()
        if el[0] != el[1]:
            coppie.add(el)

    if len(coppie) == 0: return coppie
    else: return False
    
def check2(line: str)-> bool:
    good = list()
    nook = list()
    tmp = ""
    parsing_g = True
    for char in line:
        if parsing_g: div = "["
        else: div = "]"
        if char == div:
            if parsing_g: good.append(tmp)
            else: nook.append(tmp)
            parsing_g = not parsing_g
            tmp = ""
        else:
            tmp += char
    
    if parsing_g: good.append(tmp)
    else: nook.append(tmp)
    #print(good, nook)
    
    can_go = False
    for piece in good:
        if abba_in_str(piece):
            can_go = True

    if not can_go:
        return False

    for piece in nook:
        if abba_in_str(piece):
            return False
    
    
    return True


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    abba_ips = list()
    for line in inputs_1.splitlines():
        if check(line): abba_ips.append(line)
    
    return abba_ips
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
        
    return 1


if __name__ == "__main__":
    test = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
"""
    print(f"Part 1: {len(solve_1())}")
    print(f"Part 2: {solve_2()}")