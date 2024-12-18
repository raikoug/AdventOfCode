from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List
from queue import PriorityQueue
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
import time

# Initialize the console for rich output
console = Console()

# Determine the current day from the filename
CURRENT_DAY = int(Path(__file__).stem.replace('day_', ''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string=None, new_A: int = 0) -> str:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    R = {
        "A": 0,
        "B": 0,
        "C": 0
    }
    
    # Logic: Parse input lines to initialize registers and instructions
    for line in inputs_1.splitlines():
        if "Register" in line: 
            _, reg, val = line.split(" ")
            reg = reg.replace(":", "")
            val = int(val)
            R[reg] = val
        if "Program" in line:
            _, instructions = line.split(" ")
            I: List[int] = [int(el) for el in instructions.split(",")]
    
    # Logic: Update register A if a new value is provided
    if new_A != 0:
        R["A"] = new_A
    i: int = 0
    out: List[int] = list()
    
    def parse_instr():
        # Logic: Parse and execute a single instruction
        nonlocal i, R, out, I
        
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
        
        match I[i]:  # opcode
            case 0:  # ADV
                R["A"] = R["A"] // (2 ** get_operand(I[i+1]))
            case 1:  # BXL
                R["B"] = R["B"] ^ I[i+1]
            case 2:  # BST
                R["B"] = get_operand(I[i+1]) % 8
            case 3:  # JNZ
                if R["A"] != 0:
                    i = I[i+1]
                    return True
            case 4:  # BCX
                R["B"] = R["B"] ^ R["C"]
            case 5:  # OUT
                out.append(str(get_operand(I[i+1]) % 8))
            case 6:  # BDV
                R["B"] = R["A"] // (2 ** get_operand(I[i+1]))
            case 7:  # CDV
                R["C"] = R["A"] // (2 ** get_operand(I[i+1]))
        
        i += 2
        return True
            
    # Logic: Execute all instructions
    while i < len(I):
        parse_instr()

    return ",".join(out), instructions

def solve_2(test_string=None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    
    def add_i_in_pos(base, i, pos):
        # Logic: Modify the octal digit at the specified position
        list_oct = list(f"{base:o}".zfill(16))
        new_val = int(list_oct[pos]) + i
        new_val = new_val if new_val < 8 else 1
        list_oct[pos] = str(new_val)
        return int("".join(list_oct), 8)
    
    def get_pos_es(csv_1: str, csv_2: str, pos):
        # Logic: Retrieve values at a specific position from two CSV strings
        return csv_1.split(",")[pos], csv_2.split(",")[pos]
    
    base = int(0o1000000000000000)
    pos = 0
    q = PriorityQueue()
    q.put([base, pos])
    result = list()
    nodes_processed = 0  # Logic: Counter for processed nodes
    
    def create_table(current_base, current_pos, current_digit, match_status, nodes_proc):
        # Visual: Create a table to display the current state
        table = Table(title="[bold bright_green]✨ 2024 Day 17 Solution Tree Visualization ✨[/bold bright_green]", box=None)
        table.add_column("[bold green]Parameter[/bold green]", style="bright_green")
        table.add_column("[bold white]Value[/bold white]", style="white")
        table.add_row("Base (octal)", f"[bold bright_white]{current_base:o}".zfill(16))
        table.add_row("Position", f"[bold bright_yellow]{15 - current_pos}[/bold bright_yellow]")
        table.add_row("Test Value", f"[bold bright_cyan]{current_digit}[/bold bright_cyan]")
        if match_status == "Match":
            table.add_row("Status", "[bold bright_green]✅ Match[/bold bright_green]")
        else:
            table.add_row("Status", "[bold bright_red]❌ No Match[/bold bright_red]")
        table.add_row("Visited Nodes", f"[bold bright_magenta]{nodes_proc}[/bold bright_magenta]")
        return table

    # Visual: Define colors for the pulsating border effect
    border_colors = ["bright_green", "green", "bright_cyan", "cyan", "bright_magenta", "magenta"]
    color_index = 0  # Visual: Index to cycle through border colors

    with Live(console=console, screen=True, auto_refresh=False) as live:
        while not q.empty():
            current = q.get()
            base, pos = current
            for i in range(8):
                new_base = add_i_in_pos(base, i, pos)
                res, target = solve_1(new_A=new_base)
                l, r = get_pos_es(res, target, (15 - pos))
                
                nodes_processed += 1  # Logic: Increment node counter
                
                if l == r:
                    # Logic: If values match, update results and enqueue next position
                    if pos == 15:
                        result.append(new_base)
                    if pos < 15:
                        q.put([new_base, pos + 1])
                    
                    # Visual: Create table with match status
                    table = create_table(new_base, pos, i, "Match", nodes_processed)
                else:
                    # Visual: Create table with no match status
                    table = create_table(new_base, pos, i, "No Match", nodes_processed)
                
                # Visual: Update display with pulsating border effect
                border_color = border_colors[color_index % len(border_colors)]
                border_color_text = f"bold {border_color}"
                panel = Panel(table, border_style=border_color_text)
                live.update(panel)
                live.refresh()
                
                color_index += 1  # Visual: Update color index for next cycle
                
                # Visual: Introduce delay to create video-like effect
                time.sleep(0.005)  # Adjust the value to speed up or slow down
        
    # Visual: Display final results after search completion
    if result:
        console.print(Panel(f"[bold bright_green]Part 2: {min(result):o}[/bold bright_green]", style="bright_green on black"))
    else:
        console.print(Panel("[bold bright_red]No solution found....[/bold bright_red]", style="bright_red on black"))

# Introduce a short delay before execution starts (only for video recording purpose :D)
#time.sleep(5)

if __name__ == "__main__":
    test = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
    # Logic: Execute and display Part 1 result
    res1, _ = solve_1()
    console.print(Panel(f"[bold bright_green]Part 1: {res1}[/bold bright_green]", style="bright_green on black"))
    
    # Logic: Execute Part 2 with dynamic visualization
    solve_2()
