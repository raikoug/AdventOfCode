from itertools import product
import aoc_utils
from pathlib import Path

day = int(Path(__file__).name.split('_')[1])
tf = aoc_utils.get_day_input(day)


larghezza = len(tf[0])
altezza = len(tf)

def is_int(ch):
    try:
        int(ch)
        return True
    except:
        return False
    
def get_whole_number(i, j):
    # go left until something different from number, then go right until something different from number
    #  get all the numbers inside and compose the result
    number = ""
    while True:
        if is_int(tf[i][j]):
            j -= 1
        else:
            break
    j += 1
    while True:
        if is_int(tf[i][j]):
            number += tf[i][j]
            j += 1
        else:
            break

    return number

def check_sourrounding(i, j):
    # check if in the matrix, around the array in row i, starting from start ending in end, there are only dots
    # if so, return True
    # else return False

    righe = [i-1, i, i+1]
    colonne = [j-1, j, j+1]
    numbers = list()

    coppie = product(righe, colonne)
    for coppia in coppie:
        # check if coppia is not the same as [i][start:end]
        if coppia[0] != i or coppia[1] != j:
            # check if coppia[0] and coppia[1] is >= 0
            if coppia[0] >= 0 and coppia[1] >= 0:
                try:
                    if is_int(tf[coppia[0]][coppia[1]]):
                        print(f"trovato {tf[coppia[0]][coppia[1]]} in {coppia[0]} {coppia[1]}")
                        numbers.append(get_whole_number(coppia[0], coppia[1]))
                except:
                    pass
    return numbers

total = 0
for i in range(0, altezza):
    for j in range(0, larghezza):
        if tf[i][j] == "*":
            numbers = check_sourrounding(i, j)
            numbers = list(set(numbers))
            if len(numbers) == 2:
                print(f"{numbers}")
                total += (int(numbers[0]) * int(numbers[1]))

print(total)