from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from collections import defaultdict


CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

@dataclass
class Instruction:
    one: str
    two: str
    operand: str
    dest: str
    
    def calc(self, gates) -> int:
        if all([self.one in gates, self.two in gates]):
            if self.operand == "AND":
                return gates[self.one] & gates[self.two]
            elif self.operand == "OR":
                return gates[self.one] | gates[self.two]
            elif self.operand == "XOR":
                return gates[self.one] ^ gates[self.two]
        else: return -1

def stampa_gates(gates: Dict[str,int], z:bool = False):
    keys = sorted(list(gates.keys()))
    for key in keys:
        if not z:
            print(f"{key: <3}: {gates[key]}")
        elif z and key.startswith("z"):
            print(f"{key: <3}: {gates[key]}")
    

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    
    gates: Dict[str,int] = dict()
    instructions: List[Instruction] = list()
    zetas : List[str] = list()

    
    for line in inputs_1.splitlines():
        if ":" in line:
            gate,value = line.split(": ")
            value = int(value)
            gates[gate] = value
        elif "->" in line:
            one,operand,two = line.split(" -> ")[0].split(" ")
            destination = line.split(" -> ")[1]
            instr = Instruction(one, two, operand,destination)
            res = instr.calc(gates)
            if res >= 0:
                gates[destination] = res
                if instr.dest.startswith("z"):
                    zetas.append(instr.dest)
            else:
                instructions.append(instr)
    
    times = 0
    while instructions:
        found = False
        for i in range(len(instructions)):
            instr = instructions.pop(0)
            res = instr.calc(gates)
            if res >= 0:
                gates[instr.dest] = res
                if instr.dest.startswith("z"):
                    zetas.append(instr.dest)
                found = True
            else:
                instructions.append(instr)
        if not found:
            times +=1
            if times >= 3:
                break
        
        
    #stampa_gates(gates, True)
    zetas = sorted(zetas)
    res: str = ""
    #print(zetas)
    for z in zetas:
        res = str(gates[z]) + res
        
            
    return f"{res} -> {int(res,2)}"
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    
    for i,line in enumerate(inputs_1.splitlines()):
        if ":" in line:
            pass
        elif "->" in line:
            break
    
    lines = inputs_1.splitlines()[i:]

    res = ""
    res += "digraph circuito {\n"
    res += "    rankdir=LR;\n"
    res += '    node [shape=box, style=filled, fillcolor="#CCCCFF"];\n'

    gate_counter = 0
    wire_nodes = set()  # per evitare di ripetere definizioni

    for line in lines:
        # Esempio di parsing semplice
        # "ntg XOR fgs -> mjb"
        # Splitta in "ntg XOR fgs", "mjb"
        left, wireOut = line.split(" -> ")
        wireA, op, wireB = left.split()

        gate_name = f"gate{gate_counter}"
        gate_counter += 1

        # Stampa il nodo gate
        res += f'    {gate_name} [label="{op}"];\n'

        # Aggiungi i nodi-wire, se non già definiti
        if wireA not in wire_nodes:
            res += f'    {wireA} [shape=ellipse, fillcolor="#FFFFCC", style=filled];\n'
            wire_nodes.add(wireA)
        if wireB not in wire_nodes:
            res += f'    {wireB} [shape=ellipse, fillcolor="#FFFFCC", style=filled];\n'
            wire_nodes.add(wireB)
        if wireOut not in wire_nodes:
            res += f'    {wireOut} [shape=ellipse, fillcolor="#FFFFCC", style=filled];\n'
            wire_nodes.add(wireOut)

        # Stampa le connessioni
        res += f'    {wireA} -> {gate_name};\n'
        res += f'    {wireB} -> {gate_name};\n'
        res += f'    {gate_name} -> {wireOut};\n'

    res += "}\n"
    dest = Path(__file__).parent / Path("day_24.dot")
    
    dest.write_text(res)
    # dot -Tsvg day_24.dot -o day_24.svg
    # visually search for errors

    
if __name__ == "__main__":
    test1 = """x00: 1
x01: 1
x02: 1
y00: 0
y01: 1
y02: 0

x00 AND y00 -> z00
x01 XOR y01 -> z01
x02 OR y02 -> z02
"""
    test2 = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")