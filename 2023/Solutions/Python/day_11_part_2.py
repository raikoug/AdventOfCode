import re
from icecream import ic
from itertools import combinations

def get_column_as_string(m: list, col: int):
    """
        Get a column as a string
    """
    return "".join([row[col] for row in m])

def get_row_cols_with_galaxies(m: list)-> list:
    """
        Get the ROWs and COLs with galaxies
    """
    rows = list()
    cols = list()
    for i, row in enumerate(m):
        if "#" not in row:
            rows.append(i)
    for i in range(len(m[0])):
        column = get_column_as_string(m, i)
        if "#" not in column:
            cols.append(i)
    
    ic(rows, cols)
    return rows, cols 

def get_galaxies(m: list)-> list:
    galaxies = list()
    for i, row in enumerate(m):
        tmpgalaxies = [m.start() for m in re.finditer('#', row)]
        if tmpgalaxies:
            galaxies.extend([(i, g) for g in tmpgalaxies])    
    return galaxies   

def write_universe(m: list):
    """
        Write the universe to a file
    """
    with open("universe.txt", "w") as f:
        for row in m:
            f.write(row+"\n")

def calc_distance(points: list, rows: list ,cols: list, expansion: int)-> int:
    """
        Calculate the distance between two points, if row or cols pass through the rows or cols,
        add expansion to the distance for each them
    """
    g1 = points[0]
    g2 = points[1]

    # we cannot go diagonal, so we need to calculate the distance
    #  as the (sum of the horizontal and vertical distance ) 

    # horizontal distance
    hd = abs(g1[0] - g2[0])
    # vertical distance
    vd = abs(g1[1] - g2[1])

    # check how many rows in the rows list are between the 2 galaxys
    galaxy_rows = [min(g1[0], g2[0]), max(g1[0], g2[0])]
    galaxy_cols = [min(g1[1], g2[1]), max(g1[1], g2[1])]

    rows_between = [r for r in rows if r > galaxy_rows[0] and r < galaxy_rows[1]]
    cols_between = [c for c in cols if c > galaxy_cols[0] and c < galaxy_cols[1]]


    exp = (len(rows_between) + len(cols_between)) * expansion


    return hd + vd + exp

if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)
    
    expansion = 1000000
    #expand the universe! (and map galaxies)
    galaxies = get_galaxies(tf)
    rows,cols = get_row_cols_with_galaxies(tf)

    total = 0
    points = list(combinations(galaxies, 2))
    for point in points:
        distance = calc_distance(point,rows,cols, expansion-1)
        total += distance

    ic(total)