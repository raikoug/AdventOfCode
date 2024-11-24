from starter import AOC, CURRENT_YEAR
from pathlib import Path
from re import findall

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

regex = r'(\w)(\w)\2\1'
regex2 = r'(?=((\w)(\w))\2)'
#regex2 = r'(\w)(\w)\1'

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
    coppie = list()
    for el in findall(regex2, piece):
        # print("aba_in_str", piece, findall(regex2, piece))
        if el[1] != el[2]:
            tmp_coppia = [el[1],el[2]]
            if tmp_coppia not in coppie: coppie.append(tmp_coppia)
    
    if coppie: 
        return coppie
    
    else: return False

def coppia_in_str(coppie: list, piece: str) -> bool:
    for coppia in coppie:
        ricerca = f"{coppia[1]}{coppia[0]}{coppia[1]}"
        if ricerca in piece:
             return True
    
    return False
    
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
    coppie = list()
    for piece in good:
        tmp_coppie = aba_in_str(piece)
        if tmp_coppie:
            can_go = True
            for coppia in tmp_coppie:
                if coppia not in coppie:
                    coppie.append(coppia)
    # print("check2",coppie)

    if not can_go:
        return False

    # ora devo controllare che almeno in un pezzo bad ci sia almeno una delle coppie trovate
    for piece in nook:
        res = coppia_in_str(coppie,piece)
        # print("check nook", line, coppie, piece, res)
        if res:
            return True
    
    return False


def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    abba_ips = list()
    for line in inputs_1.splitlines():
        if check(line): abba_ips.append(line)
    
    return abba_ips
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    aba_ips = list()
    for line in inputs_1.splitlines():
        if check2(line): 
            aba_ips.append(line)
    
    return aba_ips


if __name__ == "__main__":
    test = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
"""
    test2 = """aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb
aaa[bbb]ccc
"""
    print(f"Part 1: {len(solve_1())}")
    print(f"Part 2: {len(solve_2())}")
