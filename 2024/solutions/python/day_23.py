from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional, Dict, Set
from dataclasses import dataclass, field


CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

@dataclass
class Node:
    name:str
    connected_to:List[str]

def find_same_nodes(list1: List[str], list2: List[str]):
    for el1 in list1:
        if el1 in list2:
            yield el1

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    nodes: Dict[str,Node] = dict()
    for line in inputs_1.splitlines():
        a,b = line.split("-")
        if a not in nodes:
            nodes[a] = Node(a,[b])
        else:
            nodes[a].connected_to.append(b)
        
        if b not in nodes:
            nodes[b] = Node(b,[a])
        else:
            nodes[b].connected_to.append(a)
    total = 0
    triplettes = list()
    for key,node in nodes.items():
        if len(node.connected_to) >= 3:
            # first node self
            for second_node in node.connected_to:
                #second node
                # check if they share another connected node in their lists
                for third_node in find_same_nodes(node.connected_to, nodes[second_node].connected_to):
                    # third node found, one of these have to start with t
                    if any([key.startswith("t"),
                            second_node.startswith("t"),
                            third_node.startswith("t")
                           ]):
                        triplette = sorted([key,second_node,third_node])
                        if triplette not in triplettes:
                            total += 1
                            triplettes.append(triplette)
    return total
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    nodes: Dict[str,Node] = dict()
    for line in inputs_1.splitlines():
        a,b = line.split("-")
        if a not in nodes:
            nodes[a] = Node(a,[b])
        else:
            nodes[a].connected_to.append(b)
        
        if b not in nodes:
            nodes[b] = Node(b,[a])
        else:
            nodes[b].connected_to.append(a)
    
    
    def dfs(computer:str, network:Set[str]):
        if computer in network:
            return
        elif all([computer in nodes[other].connected_to for other in network]):
            network.add(computer)
            for connection in nodes[computer].connected_to:
                dfs(connection, network)
    
    
    largest = set()
    for computer in nodes.keys():
        network = set()
        dfs(computer, network)
        if len(network) > len(largest):
            largest = network
    return ",".join(sorted(list(largest)))
    
    


if __name__ == "__main__":
    test = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")