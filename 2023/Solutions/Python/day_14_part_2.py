from icecream import ic
import re

def tilt_to_right_platform(platform: list) -> list:
    """
       given a list of line line like this: .#O.#O.... 
         make the O roll to right untill it hits a #, a O or EOL
         then return the new list of lines
    """
    new_platform = list()
    for line in platform:
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
        new_platform.append(new_line)
    return new_platform
    
def calc_weight_platform(platform: list) -> int:
    """
        given a line like this: '##....OOOO'
          calculate the weight of the line where only the O have weight
          and it's equal to the column index he is on, index starts with 1 instead of 0
    """
    total = 0
    for line in platform:
        total += sum([m.start()+1 for m in re.finditer('O', line)])

    return total


def rotate_platform(platform: list) -> list:
    """
        given a platform, rotate it to the right
    """
    new_platform = [''.join(el) for el in (zip(*platform[::-1]))]
    return new_platform

def cycle(platform: list) -> list:
    """
        given a platform, on the right we have north, tilt to right
        rotate, now west is on the right, tilt to right
        rotate, now south is on the right, tilt to right
        rotate, now east is on the right, tilt to right
          now should be a good moment for a print
        rotate, now north is on the right, return the platform

    """
    # tilt to right (north)
    new_platform = tilt_to_right_platform(platform)
    # rotate
    new_platform = rotate_platform(new_platform)

    # tilt to right (west)
    new_platform = tilt_to_right_platform(new_platform)
    # rotate
    new_platform = rotate_platform(new_platform)

    # tilt to right (south)
    new_platform = tilt_to_right_platform(new_platform)
    # rotate
    new_platform = rotate_platform(new_platform)

    # tilt to right (east)
    new_platform = tilt_to_right_platform(new_platform)
    #ic(new_platform)
    # rotate
    new_platform = rotate_platform(new_platform)

    return new_platform


if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)
    ic(tf)
    cycles = 1000000000
    # the weights will always moved left to right, and the rotation of the platform will be:
    #  north -> west -> south -> east 
    #  so i can just rotate the platform and tilt it to the right

    # start position is north
    starting_platform = [''.join(el) for el in (zip(*tf[::-1]))]
    new_p = cycle(starting_platform)
    old_platforms = list()
    old_platforms.append(starting_platform) # startin point, cycle 0
    old_platforms.append(new_p)             # cycle 1
    for i in range(cycles-1):
        if i % 100000 == 0:
            print(f"cycle {i}", end="\r")
        
        new_p = cycle(new_p)
        if new_p in old_platforms:
            ic("cycle,", i+2,  "is equal to",  old_platforms.index(new_p))
            break

        old_platforms.append(new_p)           # cycle i+2
        
    # cycle found, (i+2) -  {old_platforms.index(new_p)} = module of the cycle, but it 
    #   doesn't start from 0, it starts from {old_platforms.index(new_p)}
    #   creating a mapping module based of the cycle, where 
    #   the index of the platform at cycle X is the value of the module at cycle X
    # STARTING PLATFORM
    starting_platform = old_platforms.index(new_p)
    # ENDING PLATFORM
    ending_platform = i+2
    # MODULE
    module = ending_platform - starting_platform
    ic(module)
    # new platform list of the needed lenght with placeholder value '0'
    mapped_platforms = [0] * module
    # fill the list with the values of the old_platforms needed from index i+1 to module-1
    for i in range(starting_platform, ending_platform):
        mapped_platforms[i%module] = old_platforms[i]
    
    ending_platform = mapped_platforms[cycles%module]
    ic(ending_platform)
    weight = calc_weight_platform(ending_platform)
    ic(weight)

