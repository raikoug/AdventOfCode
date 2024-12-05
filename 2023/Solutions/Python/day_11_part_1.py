import re
from icecream import ic
from itertools import combinations

def get_column_as_string(m: list, col: int):
    """
        Get a column as a string
    """
    return "".join([row[col] for row in m])

def expand_universe(m: list):
    """
        Expand the universe by doubling the ROWs and COLs not containing a galaxy ("#")
         Space is "." and galaxy is "#" 
    """
    
    for i in reversed(range(len(m))):
        if "#" not in m[i]:
            m.insert(i, "."*len(m[i]))
    
    for i in reversed(range(len(m[0]))):
        column = get_column_as_string(m, i)
        if "#" not in column:
            m = [row[:i] + "." + row[i:] for row in m]
    
    galaxies = list()
    for i, row in enumerate(m):
        tmpgalaxies = [m.start() for m in re.finditer('#', row)]
        if tmpgalaxies:
            galaxies.extend([(i, g) for g in tmpgalaxies])    
    return m, galaxies   

def write_universe(m: list):
    """
        Write the universe to a file
    """
    with open("universe.txt", "w") as f:
        for row in m:
            f.write(row+"\n")

def calc_distance(points: list)-> int:
    """
        Calculate the distance between two points
    """
    g1 = points[0]
    g2 = points[1]

    # we cannot go diagonal, so we need to calculate the distance
    #  as the (sum of the horizontal and vertical distance ) 

    # horizontal distance
    hd = abs(g1[0] - g2[0])
    # vertical distance
    vd = abs(g1[1] - g2[1])
    return hd + vd 

if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)
    #expand the universe! (and map galaxies)
    universe, galaxies = expand_universe(tf)


    total = 0
    points = list(combinations(galaxies, 2))
    for point in points:
        distance = calc_distance(point)
        total += distance

    ic(total)