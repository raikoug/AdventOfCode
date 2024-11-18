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

total = 0

def is_coppia_not_inside(coppia, i, start, end):
    # check if the couple is not inside the array [i][start:end]
    if coppia[0] == i and coppia[1] >= start and coppia[1] <= end:
        return False
    else:
        return True

def check_sourrounding(i, start, end):
    # check if in the matrix, around the array in row i, starting from start ending in end, there are only dots
    # if so, return True
    # else return False

    righe = [i-1, i, i+1]
    colonne = range(start-1, end+2) 

    coppie = product(righe, colonne)
    for coppia in coppie:
        # check if coppia is not the same as [i][start:end]
        if is_coppia_not_inside(coppia, i, start, end):
            # check if coppia[0] and coppia[1] is >= 0
            if coppia[0] >= 0 and coppia[1] >= 0:
                try:
                    if tf[coppia[0]][coppia[1]] != ".":
                        #print(f"trovato {tf[coppia[0]][coppia[1]]} in {coppia[0]} {coppia[1]}")
                        return True
                except:
                    pass
    return False
            

for i in range(0, altezza):
    number = ""
    found_n = False
    for j in range(0, larghezza):
        if is_int(tf[i][j]):
            if found_n:
                number += tf[i][j]
            else:
                found_n = True
                number = tf[i][j]
                start = j
        else:
            if found_n:
                found_n = False
                end = j -1
                #print(f"riga {i} da {start} a {end} = {number}")
                if check_sourrounding(i, start, end):
                    total += int(number)
                number = ""
    if found_n:
        # number ends at the end of the line
        end = larghezza
        #print(f"riga {i} da {start} a {end} = {number}")
        if check_sourrounding(i, start, end):
            total += int(number)
        number = ""
    
            
print(total)