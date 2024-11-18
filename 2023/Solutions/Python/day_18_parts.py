from icecream import ic

DIRECTIONS = {
	'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0), # part1
	'0': (0, 1), '1': (1, 0), '2': (0, -1), '3': (-1, 0), # part2
}

def iter_2(iterable: list):
    for i in range(len(iterable)-1):
        yield iterable[i],iterable[i+1]

def shoelace(vertices):
	area = 0
	for (r1, c1), (r2, c2) in iter_2(vertices):
		area += (r2 + r1) * (c2 - c1)

	return abs(area) // 2


def get_vertices_and_permiters(steps: list) -> dict:
    """
        Calculates the vertices of the walk made with steps.
        Fo part_1 only the first two value of each step is used:
        'R 6 (#70c710)' -> 'R 6' -> direction distance
    """
    result = {
        "part_1": {"vertices": list(), "perimeter": 0},
        "part_2": {"vertices": list(), "perimeter": 0}
    }
    r1 = c1 = 0 
    r2 = c2 = 0

    for step in steps:
        direction, distance, hexval = step.split()
        
        # PART 1
        distance = int(distance)
        p1row, p1col = DIRECTIONS[direction[0]]
        r1 += p1row * distance
        c1 += p1col * distance
        result['part_1']['vertices'].append((r1, c1))
        result['part_1']['perimeter'] += distance

        # PART 2
        distance = int(hexval[2:-2], 16)
        p2row, p2col  = DIRECTIONS[hexval[-2]]
        r2 += p2row * distance
        c2 += p2col * distance
        result['part_2']['vertices'].append((r2, c2))
        result['part_2']['perimeter'] += distance
        

    return result

def solve(vertices: list, perimeter: int) -> int:
    """
        Calculates the area of the polygon defined by vertices, permiter included.
    """
    area = shoelace(vertices)
    return int(area - perimeter / 2 + 1) + perimeter



if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)
    elaborates = get_vertices_and_permiters(tf)
    #ic(elaborates)
    for part, v in elaborates.items():
        #ic(part, v['vertices'], v['perimeter'])
        v['result'] = solve(v['vertices'], v['perimeter'])
        ic(part, v['result'])
    #result = solve(elaborates['part_1']['vertices'], elaborates['part_1']['perimeter'])
    