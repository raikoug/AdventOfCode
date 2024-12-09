from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    line = list(inputs_1.strip())
    files_list = line[::2]
    frees_list = line[1::2]
    files = {i:v for i,v in enumerate(files_list)}
    
    filesystem = list()
    for i,el in files.items():
        filesystem += [str(i)] * int(el)
        try:
            filesystem += ["."] * int(frees_list[i])
        except:
            pass
    
    #print("".join(filesystem))
    end = False
    for i in range(len(filesystem)-1,0,-1):
        if filesystem[i] != ".":
            #search from left the first "." before i
            for j in range(i):
                if filesystem[j] == ".":
                    filesystem[i],filesystem[j] = filesystem[j],filesystem[i]
                    break
            else:
                #no more movements!
                end = True
        #print("".join(filesystem), i)
        if end:
            break
    
    checksum = 0
    for i,el in enumerate(filesystem):
        if el == ".":
            break
        checksum += i*int(el)
        
    return checksum
    

def solve_2(test_string = None) -> int:
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    line = list(inputs_1.strip())
    files_list = line[::2]
    frees_list = line[1::2]
    files = {i:v for i,v in enumerate(files_list)}
    
    filesystem = list()
    for i,el in files.items():
        filesystem += [str(i)] * int(el)
        try:
            filesystem += ["."] * int(frees_list[i])
        except:
            pass

    def get_file_start_end(fs, file_id):
        try:
            start = fs.index(str(file_id))
        except ValueError:
            return None, None  # 404! file not found

        length = int(files_list[file_id])
        end = start + length - 1
        return start, end

    def get_frees_start_end(fs, block_length, max_pos):
        current_block_start = None
        current_block_length = 0

        for idx in range(max_pos):
            if fs[idx] == '.':
                if current_block_start is None:
                    current_block_start = idx
                    current_block_length = 1
                else:
                    current_block_length += 1
                if current_block_length == block_length:
                    return current_block_start
            else:
                current_block_start = None
                current_block_length = 0
        return None

    max_file_id = len(files_list) - 1
    for fid in range(max_file_id, -1, -1):
        f_len = int(files_list[fid])
        if f_len == 0:
            continue 
        start, end = get_file_start_end(filesystem, fid)
        if start is None:
            continue  # 404 ! File not found (shouldn't happen, but instead of panic...)
        # Find a free block of length f_len to the left of 'start'
        free_start = get_frees_start_end(filesystem, f_len, start)
        if free_start is not None:
            for i in range(start, end+1):
                filesystem[i] = '.'
            for i in range(f_len):
                filesystem[free_start + i] = str(fid)

    checksum = 0
    for i, el in enumerate(filesystem):
        if el != '.':
            checksum += i * int(el)

    return checksum


if __name__ == "__main__":
    test = "2333133121414131402"
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")