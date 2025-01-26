from icecream import ic
import re

def til_To_north_line(line: list) -> list:
    """
       given a line like this: .#O.#O.... 
         make the O roll to right untill it hits a #, a O or EOL
         then return the line
    """
    # split line by "#"
    sub_lines = line.split("#")
    new_parts = list()
    # for each sub_line i create the line again putting the O at the end, filling with "." if needed
    for part in sub_lines:
        if part == '':
            new_parts.append(part)
            continue
        
        Os = part.count("O")
        part = f"{'O'*Os:.>{len(part)}}"
        new_parts.append(part)
        # replace the part in the original line

    new_line = "#".join(new_parts)
    return new_line
    
def calc_weight(line: list) -> int:
    """
        given a line like this: '##....OOOO'
          calculate the weight of the line where only the O have weight
          and it's equal to the column index he is on, index starts with 1 instead of 0
    """
    total = 0
    for i in range(len(line)):
        if line[i] == "O":
            return i+1


if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)

    # this i by far easier to do rotated
    platform = [''.join(el) for el in (zip(*tf[::-1]))]
    new_platform = list()
    total_weight = 0
    for line in platform:
        new_line = til_To_north_line(line)
        weight = sum([m.start()+1 for m in re.finditer('O', new_line)])
        total_weight += weight
        new_platform.append(new_line)
    
    
    ic(total_weight)
    