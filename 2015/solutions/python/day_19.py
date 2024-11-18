from starter import AOC, CURRENT_YEAR
from pathlib import Path
from queue import PriorityQueue

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def map_line(s: str):
    key: str = ""
    val: str = ""
    #Al => ThF
    #Al => ThRnFAr
    key, val = s.split(" => ")
    return key, val
    

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    source_map = dict()
    for line in inputs_1.splitlines():
        if "=>" in line:
            key,val = map_line(line)
            if key in source_map:
                source_map[key].append(val)
            else:
                source_map[key] = [val]
        elif line != '':
            molecule = line
    
    
    sources = dict()
    keys_in_molecule = dict()
    for key in source_map:
        keys_in_molecule[key] = molecule.count(key)
        sources[key] = len(source_map[key])
    
    possible_molecules = set()
    
    transition_monlecule = molecule
    for key in source_map.keys():
        transition_monlecule = transition_monlecule.replace(key,f",{key},")
    molecule_in_list = [el for el in transition_monlecule.split(',') if el]
    #print(molecule_in_list)
    for i,el in enumerate(molecule_in_list):
        key = el
        if key in source_map:
            for new_el in source_map[key]:
                tmp_list = list(molecule_in_list)
                tmp_list[i] = new_el
                possible_molecules.add("".join(tmp_list))
            
    #print(possible_molecules)
    return len(possible_molecules)

def one_step(source_map, molecule)-> set:
    sources = dict()
    keys_in_molecule = dict()
    for key in source_map:
        keys_in_molecule[key] = molecule.count(key)
        sources[key] = len(source_map[key])
    
    possible_molecules = set()
    
    transition_monlecule = molecule
    for key in source_map.keys():
        transition_monlecule = transition_monlecule.replace(key,f",{key},")
    molecule_in_list = [el for el in transition_monlecule.split(',') if el]
    #print(molecule_in_list)
    for i,el in enumerate(molecule_in_list):
        key = el
        if key in source_map:
            for new_el in source_map[key]:
                tmp_list = list(molecule_in_list)
                tmp_list[i] = new_el
                possible_molecules.add("".join(tmp_list))
            
    #print(possible_molecules)
    return list(possible_molecules)

def reverse_step(source_map: dict, molecule):
    
    
    sources = dict()
    keys_in_molecule = dict()
    for key in source_map:
        keys_in_molecule[key] = molecule.count(key)
        sources[key] = len(source_map[key])
    
    possible_molecules = set()
    
    transition_monlecule = molecule
    for key in source_map.keys():
        transition_monlecule = transition_monlecule.replace(key,f",{key},")
    molecule_in_list = [el for el in transition_monlecule.split(',') if el]
    #print(molecule_in_list)
    for i,el in enumerate(molecule_in_list):
        key = el
        if key in source_map:
            for new_el in source_map[key]:
                tmp_list = list(molecule_in_list)
                tmp_list[i] = new_el
                possible_molecules.add("".join(tmp_list))
            
    #print(possible_molecules)
    return list(possible_molecules)
    
    
def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    source_map = dict()
    for line in inputs_1.splitlines():
        if "=>" in line:
            key,val = map_line(line)
            if key in source_map:
                source_map[key].append(val)
            else:
                source_map[key] = [val]
        elif line != '':
            target_molecule = line
    
    new_mapping = dict()
    for k,v in source_map.items():
        for el in v:
            if el in new_mapping:
                new_mapping[el].append(k)
            else:
                new_mapping[el] = [k]
    source_map = new_mapping
    print(source_map)
    
    molecule_queue = PriorityQueue()
    molecule_queue.put([1,target_molecule,0])
    while True:
        lenght, current_molecule, cycle = molecule_queue.get()
        print(lenght, current_molecule, cycle)
        for mol in reverse_step(source_map, current_molecule):
            if mol == "e":
                print(current_molecule, mol)
                return cycle
            molecule_queue.put([len(mol), mol, cycle+1])




if __name__ == "__main__":
    test_string_1 = """H => HO
H => OH
O => HH

HOH"""
    test_string_2 = """e => H
e => O
H => HO
H => OH
O => HH

HOH"""
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")