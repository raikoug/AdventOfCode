from starter import AOC, CURRENT_YEAR
from pathlib import Path
import string

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def word_shift(word: str, key: int) -> str:
    letters = [{i:val} for i,val in enumerate(string.ascii_lowercase)]
    mod = len(letters)
    res = ""
    # ord("a") = 97
    # ord("z") = 122
    for char in word:
        if char in string.ascii_letters:
            res += chr((((ord(char) - 97) + key )%26)+97)
        else:
            res += char
    return res

def checksum(p: str)-> str:
    mapping = dict()
    for char in p: 
        if char in string.ascii_lowercase:
            if char in mapping:
                mapping[char] += 1
            else:
                mapping[char] = 1
    
    listing = [(key,val) for key,val in mapping.items()]
    ordering = sorted(listing, key=lambda el: el[1]+(1/ord(el[0])), reverse=True)
    return "".join([el[0] for el in ordering[:5]])

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    res = 0
    correct_rooms = list()
    for line in inputs_1.splitlines():
        full_sector = line.split("[")[0]
        sect_id = int(full_sector.split("-")[-1])
        expected = line.split("[")[1].replace("]", "")
        check = checksum(full_sector)
        
        if check == expected:
            res += sect_id
            sector = full_sector.split("-")[:-1]
            correct_rooms.append([sector, sect_id])
        

    return res, correct_rooms
    
def solve_2(correct_rooms: list) -> int:
    # test
    #correct_rooms = [[["qzmt","zixmtkozy","ivhz"],343]]
    for el in correct_rooms:
        sector,key = el[0], el[1]
        sector = " ".join(sector)
        res = word_shift(sector, key)
        if "north" in res:
            return key
        
    return 1


if __name__ == "__main__":
    test = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
""" 
    res, correct_rooms = solve_1()
    print(f"Part 1: {res}")
    print(f"Part 2: {solve_2(correct_rooms)}")