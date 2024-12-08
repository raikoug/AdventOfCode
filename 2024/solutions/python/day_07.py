from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional
import itertools
from dataclasses import dataclass, field
from queue import PriorityQueue

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

@dataclass
class Equation:
    result: int
    values: List[int]
    good_ones : List = field(default_factory=list)
    ok: Optional[bool] = False

def count_ok_equations(equations: List[Equation]) -> int:
    return len([eq for eq in equations if eq.ok])

def sum_ok_equation_results(equations: List[Equation]) -> int:
    return sum([eq.result for eq in equations if eq.ok])

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    equations : List[Equation] = list()
    for line in inputs_1.splitlines():
        result, values = line.split(":")
        result = int(result)
        values = [int(el) for el in values.strip().split(" ")]
        
        equations.append(Equation(result,values))
    good_ones = list()
    total: int = 0
    for eq in equations:
        #print(eq)
        symbols = [[int.__add__, "+"], [int.__mul__, "*"]]
        q = PriorityQueue()
        found = False
        # first value fo the queue is manual:
        # [result-tmp_res,tmp_res,index,operations] 
        #    result-tmp_res the priority
        #    tmp_res        actual result for the val
        #    index          index, inclusive, of the numbers ivolved
        #    operations     used so far to reach here (who knows, maybe we need it)
        operations: list[str] = list()
        index = 0
        q.put([eq.result - eq.values[index], eq.values[index], index, operations])
        lenght = len(eq.values)
        while True:
            priority, tmp_res, index, operations = q.get()
            #print(f"     tmp_res: {tmp_res}, index: {index}, operations: {operations}, target: {eq.result}")
            index += 1
            if index == lenght:
                if tmp_res == eq.result:
                    eq.ok = True
                    total += 1
                    eq.good_ones.append(operations)
                    
                if q.empty():
                    break
                continue
            
            new_value = eq.values[index]
            add = tmp_res + new_value
            mul = tmp_res * new_value
            
            if add <= eq.result:
                new_op = operations + ["+"]
                q.put([eq.result - add, add, index, new_op])
            
            if mul <= eq.result:
                new_op = operations + ["*"]
                q.put([eq.result - mul, mul, index, new_op])
            
            if q.empty():
                break
                
        
    return sum_ok_equation_results(equations)
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    equations : List[Equation] = list()
    for line in inputs_1.splitlines():
        result, values = line.split(":")
        result = int(result)
        values = [int(el) for el in values.strip().split(" ")]
        
        equations.append(Equation(result,values))
    good_ones = list()
    total: int = 0
    for eq in equations:
        #print(eq)
        symbols = [[int.__add__, "+"], [int.__mul__, "*"]]
        q = PriorityQueue()
        found = False
        # first value fo the queue is manual:
        # [result-tmp_res,tmp_res,index,operations] 
        #    result-tmp_res the priority
        #    tmp_res        actual result for the val
        #    index          index, inclusive, of the numbers ivolved
        #    operations     used so far to reach here (who knows, maybe we need it)
        operations: list[str] = list()
        index = 0
        q.put([eq.result - eq.values[index], eq.values[index], index, operations])
        lenght = len(eq.values)
        while True:
            priority, tmp_res, index, operations = q.get()
            #print(f"     tmp_res: {tmp_res}, index: {index}, operations: {operations}, target: {eq.result}")
            index += 1
            if index == lenght:
                if tmp_res == eq.result:
                    eq.ok = True
                    total += 1
                    eq.good_ones.append(operations)
                    
                if q.empty():
                    break
                continue
            
            new_value = eq.values[index]
            add = tmp_res + new_value
            mul = tmp_res * new_value
            con = int(str(tmp_res) + str(new_value))
            
            if add <= eq.result:
                new_op = operations + ["+"]
                q.put([eq.result - add, add, index, new_op])
            
            if mul <= eq.result:
                new_op = operations + ["*"]
                q.put([eq.result - mul, mul, index, new_op])
            
            if con <= eq.result:
                new_op = operations + ["||"]
                q.put([eq.result - con, con, index, new_op])
            
            if q.empty():
                break
                
        
    return sum_ok_equation_results(equations)


if __name__ == "__main__":
    test = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")