from starter import AOC, CURRENT_YEAR
from pathlib import Path

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None, test=False) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    if test: inputs_1 = aoc.get_input(CURRENT_DAY, 9)
    total = 0
    for char in inputs_1:
        if char not in ["","\n"]:
            total += 1
            #print(char)
    print(f"totale: {total}")
    evaluated = 0
    for line in inputs_1.splitlines():
        new = eval(line)
        evaluated += len(new)
    return total, evaluated
    
def solve_2(test_string = None, test=False) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    if test: inputs_1 = aoc.get_input(CURRENT_DAY, 9)
    
    # input2 has been done manually with replaces:
    # 1) replace \ with \\
    # 2) replace " with \"
    # 3) regex replace (.*) with "$1"
    
    inputs_2 = aoc.get_input(CURRENT_DAY, 2) if not test_string else test_string
    if test: inputs_2 = aoc.get_input(CURRENT_DAY, 8)
    
    old_total = 0
    for char in inputs_1:
        if char not in ["","\n"]:
            old_total += 1
            #print(char)
    print(f"Old total: {old_total}")
    new_total = 0
    for char in inputs_2:
        if char not in ["","\n"]:
            new_total += 1
            #print(char)
    print(f"new_total : {new_total}")

    return(new_total - old_total)

def solve_2_new(test_string=None, test=False) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    total_code_length = 0
    total_encoded_length = 0

    for line in inputs_1.splitlines():
        line = line.strip()
        # Lunghezza del codice originale (compresi i doppi apici)
        code_length = len(line)
        total_code_length += code_length

        # Codifica della stringa secondo le regole
        # 1. Sostituisci '\' con '\\'
        # 2. Sostituisci '"' con '\"'
        # 3. Aggiungi '"' all'inizio e alla fine
        encoded_line = '"' + line.replace('\\', '\\\\').replace('"', '\\"') + '"'
        encoded_length = len(encoded_line)
        total_encoded_length += encoded_length

    # Calcola la differenza totale
    difference = total_encoded_length - total_code_length
    print(f"Totale lunghezza codice originale: {total_code_length}")
    print(f"Totale lunghezza codificata: {total_encoded_length}")
    print(f"Differenza totale: {difference}")
    return difference


if __name__ == "__main__":
    print(solve_2())