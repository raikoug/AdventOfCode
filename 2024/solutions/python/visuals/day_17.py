from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
from icecream import ic
from queue import PriorityQueue
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import time
import sys

#ic.disable()

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

console = Console()

def solve_1(test_string = None, new_A: int = 0) -> str:
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
            #print("instr", instructions)
            I : List[int] = [int(el) for el in instructions.split(",")]
    
    if new_A != 0:
        R["A"] = new_A
    i: int = 0
    out: List[int] = list()
    
    def parse_instr():
        #after parsing instruction and manipulating the register, change the i to the next one
        nonlocal i
        nonlocal R
        nonlocal out
        nonlocal I
        
        def get_operand(value: int) -> int:
            nonlocal R
            if value < 4:
                return value
            if value == 4:
                return R["A"]
            if value == 5:
                return R["B"]
            if value == 6:
                return R["C"]
            raise ValueError
            
        
        match I[i]: #opcode
            case 0:#ADV
                R["A"] = R["A"] // (2 ** get_operand(I[i+1]))
            case 1: #BXL
                R["B"] = R["B"] ^ I[i+1]
            case 2: #BST
                R["B"] = get_operand(I[i+1]) % 8
            case 3: #JNZ
                if R["A"] != 0:
                    i = I[i+1]
                    return True
            case 4: #bcx
                R["B"] = R["B"] ^ R["C"]
            case 5: # out
                out.append(str(get_operand(I[i+1]) % 8))
            case 6: # bdv
                R["B"] = R["A"] // (2 ** get_operand(I[i+1]))
            case 7: # cdv
                R["C"] = R["A"] // (2 ** get_operand(I[i+1]))
        
        i += 2
        return True
            
    while i < len(I):
         parse_instr()

    
    return ",".join(out), instructions
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    
    def add_i_in_pos(base,i,pos):
        # pos goes from 15 to 0
        #    <------------------
        #    15                0
        list_oct = list(f"{base:o}".zfill(16))
        new_val = int(list_oct[pos]) + i
        new_val = new_val if new_val < 8 else 1
        list_oct[pos] = str(new_val)
        int_oct = int("".join(list_oct),8)
        return int_oct
    
    def get_pos_es(csv_1: str, csv_2: str, pos):
        return csv_1.split(",")[pos], csv_2.split(",")[pos]
        

    base = int(0o1000000000000000)
    pos  = 0
    q = PriorityQueue()
    q.put([base, pos])
    result = list()
    nodes_processed = 0  # Contatore per i nodi elaborati
    
    # Definizione della struttura di visualizzazione
    def create_table(current_base, current_pos, current_digit, match_status, nodes_proc):
        table = Table(title="[bold bright_green]Visualizzazione Albero di Risoluzione[/bold bright_green]", box=None)
        table.add_column("[bold green]Parametro[/bold green]", style="bright_green")
        table.add_column("[bold white]Valore[/bold white]", style="white")
        table.add_row("Base (ottale)", f"[bold bright_white]{current_base:o}".zfill(16))
        table.add_row("Posizione", f"[bold bright_yellow]{15 - current_pos}[/bold bright_yellow]")
        table.add_row("Cifra Provata", f"[bold bright_cyan]{current_digit}[/bold bright_cyan]")
        if match_status == "Match":
            table.add_row("Stato", "[bold bright_green]Match[/bold bright_green]")
        else:
            table.add_row("Stato", "[bold bright_red]No Match[/bold bright_red]")
        table.add_row("Nodi Elaborati", f"[bold bright_magenta]{nodes_proc}[/bold bright_magenta]")
        return table

    # Definizione dei colori per l'effetto di pulsazione
    border_colors = ["bright_green", "green", "bright_cyan", "cyan", "bright_magenta", "magenta"]
    color_index = 0  # Indice per i colori del bordo

    with Live(console=console, screen=True, auto_refresh=False) as live:
        while not q.empty():
            current = q.get()
            base, pos = current
            for i in range(8):
                new_base = add_i_in_pos(base, i, pos)
                res, target = solve_1(new_A=new_base)
                l, r = get_pos_es(res, target, (15 - pos))
                
                nodes_processed += 1  # Incremento del contatore
                
                if l == r:
                    # Aggiornamento dei risultati
                    if pos == 15:
                        result.append(new_base)
                    if pos < 15:
                        q.put([new_base, pos + 1])
                    
                    # Creazione della tabella per la visualizzazione
                    table = create_table(new_base, pos, i, "Match", nodes_processed)
                else:
                    table = create_table(new_base, pos, i, "No Match", nodes_processed)
                
                # Aggiornamento del display con effetto di pulsazione
                border_color = border_colors[color_index % len(border_colors)]
                border_color_text = f"bold {border_color}"
                panel = Panel(table, border_style=border_color_text)
                live.update(panel)
                live.refresh()
                
                # Aggiornamento dell'indice del colore per il prossimo ciclo
                color_index += 1
                
                # Introduzione del ritardo per creare l'effetto "video"
                #time.sleep(0.05)  # Puoi regolare il valore per velocizzare o rallentare
    
    # Dopo la ricerca, visualizza i risultati finali
    if result:
        console.print(Panel(f"[bold bright_green]Soluzione Trovata: {min(result):o}[/bold bright_green]", style="bright_green on black"))
    else:
        console.print(Panel("[bold bright_red]Nessuna soluzione trovata.[/bold bright_red]", style="bright_red on black"))


if __name__ == "__main__":
    test = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
    # Stampa il risultato della Parte 1
    res1, _ = solve_1()
    console.print(Panel(f"[bold bright_green]Part 1: {res1}[/bold bright_green]", style="bright_green on black"))
    
    # Esegue la Parte 2 con visualizzazione dinamica
    solve_2()
