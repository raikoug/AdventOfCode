import pygame
import sys
import threading
from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List
from queue import PriorityQueue

# Inizializza Pygame
pygame.init()

# Dimensioni della finestra
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cracking Visualization")

# Definisci i colori
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Imposta i font
FONT = pygame.font.SysFont(None, 24)

# Inizializza AOC
CURRENT_DAY = 17
aoc = AOC(CURRENT_YEAR)

# Variabili globali per tracciare le cifre possibili e i risultati
possible_digits = [set() for _ in range(16)]  # pos 0 a 15
result = []
lock = threading.Lock()  # Per sincronizzare l'accesso a possible_digits e result

def solve_1(test_string=None, new_A: int = 0) -> (str, str):
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    R = {
        "A": 0,
        "B": 0,
        "C": 0
    }

    for line in inputs_1.splitlines():
        if "Register" in line:
            _, reg, val = line.split(" ")
            reg = reg.replace(":", "")
            val = int(val)
            R[reg] = val
        if "Program" in line:
            _, instructions = line.split(" ")
            I: List[int] = [int(el) for el in instructions.split(",")]

    if new_A != 0:
        R["A"] = new_A
    i: int = 0
    out: List[int] = list()

    def get_operand(value: int) -> int:
        if value < 4:
            return value
        if value == 4:
            return R["A"]
        if value == 5:
            return R["B"]
        if value == 6:
            return R["C"]
        raise ValueError

    while i < len(I):
        opcode = I[i]
        operand = I[i + 1]
        match opcode:  # opcode
            case 0:  # ADV
                R["A"] = R["A"] // (2 ** get_operand(operand))
            case 1:  # BXL
                R["B"] = R["B"] ^ operand
            case 2:  # BST
                R["B"] = get_operand(operand) % 8
            case 3:  # JNZ
                if R["A"] != 0:
                    i = operand
                    continue
            case 4:  # BXC
                R["B"] = R["B"] ^ R["C"]
            case 5:  # OUT
                out.append(str(get_operand(operand) % 8))
            case 6:  # BDV
                R["B"] = R["A"] // (2 ** get_operand(operand))
            case 7:  # CDV
                R["C"] = R["A"] // (2 ** get_operand(operand))
            case _:
                raise ValueError(f"Unknown opcode: {opcode}")
        i += 2

    return ",".join(out), instructions

def solve_2(test_string=None):
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string

    def add_i_in_pos(base, i, pos):
        # pos va da 15 a 0
        list_oct = list(f"{base:o}".zfill(16))  # Assicurati che ci siano 16 cifre
        list_oct = [int(el) for el in list_oct]
        new_val = list_oct[pos] + i
        new_val = new_val if new_val < 8 else 1
        list_oct[pos] = new_val
        f_oct = "".join([str(el) for el in list_oct])
        int_oct = int(f_oct, 8)
        return int_oct

    def get_pos_es(csv_1: str, csv_2: str, pos):
        return csv_1.split(",")[pos], csv_2.split(",")[pos]

    base = int(0o1000000000000000)
    pos = 0
    q = PriorityQueue()
    q.put((base, pos, []))  # Includi il percorso

    while not q.empty():
        base, pos, path = q.get()
        for i in range(8):
            new_base = add_i_in_pos(base, i, pos)
            new_path = path + [i]
            res, target = solve_1(new_A=new_base)
            l, r = get_pos_es(res, target, (15 - pos))
            if l == r:
                with lock:
                    # Aggiungi la cifra valida alla posizione corrente
                    if i not in possible_digits[pos]:
                        possible_digits[pos].add(i)
                if pos == 15:
                    with lock:
                        result.append(new_base)
                if pos < 15:
                    q.put((new_base, pos + 1, new_path))
    
def draw_screen(screen, possible_digits, results):
    screen.fill(BLACK)
    # Titolo
    title_text = FONT.render("Possibili cifre per ciascuna posizione (da destra a sinistra)", True, WHITE)
    screen.blit(title_text, (20, 20))
    
    # Disegna le posizioni
    for p in range(16):
        y = 60 + p * 30
        pos_num = 15 - p  # Da destra a sinistra
        pos_text = FONT.render(f"Posizione {pos_num:2}:", True, WHITE)
        screen.blit(pos_text, (20, y))
        # Disegna le cifre 0-7
        for d in range(8):
            x = 150 + d * 40
            rect = pygame.Rect(x, y, 30, 25)
            pygame.draw.rect(screen, GRAY, rect, 2)
            if d in possible_digits[p]:
                pygame.draw.circle(screen, GREEN, rect.center, 10)
            digit_text = FONT.render(str(d), True, WHITE)
            screen.blit(digit_text, (x + 10, y + 5))
    
    # Mostra i risultati
    result_text = FONT.render("Risultati trovati:", True, WHITE)
    screen.blit(result_text, (20, HEIGHT - 100))
    with lock:
        for idx, res in enumerate(results[:5]):  # Mostra solo i primi 5 risultati
            res_text = FONT.render(f"{idx+1}: {oct(res)}", True, WHITE)
            screen.blit(res_text, (20, HEIGHT - 80 + idx * 20))
    
    pygame.display.flip()

def main():
    global result
    # Avvia la ricerca in un thread separato
    search_thread = threading.Thread(target=solve_2)
    search_thread.start()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        with lock:
            draw_screen(screen, possible_digits, result)

        clock.tick(10)  # Limita a 10 frame al secondo

if __name__ == "__main__":
    main()
