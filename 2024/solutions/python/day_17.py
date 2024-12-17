from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
from icecream import ic
from queue import PriorityQueue


#ic.disable()

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

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
        # pos gos from 15 to 0
        #    <------------------
        #    15                0
        list_oct = list([int(el) for el in f"{base:o}"])
        new_val = list_oct[pos] + i
        new_val = new_val if new_val < 8 else 1
        list_oct[pos] = new_val
        f_oct = "".join([str(el) for el in list_oct])
        int_oct = int(f_oct,8)
        return int(f_oct,8)
    
    def get_pos_es(csv_1: str, csv_2: str, pos):
        return csv_1.split(",")[pos], csv_2.split(",")[pos]
        

    base = int(0o1000000000000000)
    pos  = 0
    q = PriorityQueue()
    q.put([base, pos])
    result = list()
    
    while not q.empty():
        base, pos  = q.get()
        for i in range(8):
            new_base = add_i_in_pos(base,i,pos)
            res, target = solve_1(new_A=new_base)
            l,r = get_pos_es(res,target,(15-pos))
            if l == r:
                print(f"     Possible Cracked position {15-pos: <2} -> {i: >3}: {oct(new_base)} -> {res} - {target}")
                if pos == 15:
                    result.append(new_base)
                if pos  <15 :
                    q.put([new_base, pos+1])
    print(result)
    print(min(result))
            

if __name__ == "__main__":
    test = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""
    print(f"Part 1: {solve_1()[0]}")
    print(f"Part 2: {solve_2()}")