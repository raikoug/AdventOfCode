from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # a b c d -> spoons for ingredients 1 2 3 4
    ingr = [
        [
            int(line.split(" ")[2].replace(",","")),
            int(line.split(" ")[4].replace(",","")),
            int(line.split(" ")[6].replace(",","")),
            int(line.split(" ")[8].replace(",","")) 
        ] for line in inputs_1.splitlines()
    ]
    
    massimo = 0
    for a in range(0,101):
        for b in range(0,101):
            if a+b > 100:
                pass
            for c in range(0,101):
                if (a+b+c) <= 100:
                    d = 100 - a - b - c
                    
                    ingr0 = max(0, a * ingr[0][0] + b * ingr[1][0] + c * ingr[2][0] + d * ingr[3][0])
                    ingr1 = max(0, a * ingr[0][1] + b * ingr[1][1] + c * ingr[2][1] + d * ingr[3][1])
                    ingr2 = max(0, a * ingr[0][2] + b * ingr[1][2] + c * ingr[2][2] + d * ingr[3][2])
                    ingr3 = max(0, a * ingr[0][3] + b * ingr[1][3] + c * ingr[2][3] + d * ingr[3][3])
                    totale = ingr0 * ingr1 * ingr2 * ingr3
                    massimo = max(totale,massimo)
    
    return massimo
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    # a b c d -> spoons for ingredients 1 2 3 4
    ingr = [
        [
            int(line.split(" ")[2].replace(",","")),
            int(line.split(" ")[4].replace(",","")),
            int(line.split(" ")[6].replace(",","")),
            int(line.split(" ")[8].replace(",","")),
            int(line.split(" ")[10].replace(",",""))
        ] for line in inputs_1.splitlines()
    ]
    
    massimo = 0
    for a in range(0,101):
        for b in range(0,101):
            if a+b > 100:
                pass
            for c in range(0,101):
                if (a+b+c) <= 100:
                    d = 100 - a - b - c
                    if (a * ingr[0][4] + b * ingr[1][4] + c * ingr[2][4] + d * ingr[3][4]) == 500:
                        
                        
                        ingr0 = max(0, a * ingr[0][0] + b * ingr[1][0] + c * ingr[2][0] + d * ingr[3][0])
                        ingr1 = max(0, a * ingr[0][1] + b * ingr[1][1] + c * ingr[2][1] + d * ingr[3][1])
                        ingr2 = max(0, a * ingr[0][2] + b * ingr[1][2] + c * ingr[2][2] + d * ingr[3][2])
                        ingr3 = max(0, a * ingr[0][3] + b * ingr[1][3] + c * ingr[2][3] + d * ingr[3][3])
                        ckal = a * ingr[0][4] + b * ingr[1][4] + c * ingr[2][4] + d * ingr[3][4]
                        totale = ingr0 * ingr1 * ingr2 * ingr3
                        massimo = max(totale,massimo)
    
    return massimo


if __name__ == "__main__":
    
    print("part 1", solve_1())
    print("part 2", solve_2())