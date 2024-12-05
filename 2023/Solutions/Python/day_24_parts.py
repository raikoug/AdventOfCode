from icecream import ic
from dataclasses import dataclass
from itertools import combinations
from sympy import Symbol, nonlinsolve

def edge_intersection(x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, x4: int, y4: int) -> list:
    """Intersection point of two line segments in 2 dimensions

    params:
    ----------
    x1, y1, x2, y2 -> coordinates of line a, p1 ->(x1, y1), p2 ->(x2, y2), 

    x3, y3, x4, y4 -> coordinates of line b, p3 ->(x3, y3), p4 ->(x4, y4)

    Return:
    ----------
    list
        A list contains x and y coordinates of the intersection point,
        but return an empty list if no intersection point.

    """
    # None of lines' length could be 0.
    if ((x1 == x2 and y1 == y2) or (x3 == x4 and y3 == y4)):
        return []

    # The denominators for the equations for ua and ub are the same.
    den = ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))

    # Lines are parallel when denominator equals to 0,
    # No intersection point
    if den == 0:
        return []

    # Avoid the divide overflow
    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / (den + 1e-16)
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / (den + 1e-16)

    # if ua and ub lie between 0 and 1.
    # Whichever one lies within that range then the corresponding line segment contains the intersection point.
    # If both lie within the range of 0 to 1 then the intersection point is within both line segments.
    if (ua < 0 or ua > 1 or ub < 0 or ub > 1):
        return []

    # Return a list with the x and y coordinates of the intersection
    x = x1 + ua * (x2 - x1)
    y = y1 + ua * (y2 - y1)
    return [x, y]

class Input:
    def __init__(self, path: str):
        with open(path, "r") as file:
            self._raw = file.read()
            file.seek(0)
            self._lines = [line.rstrip() for line in file.readlines()]

    @property
    def raw(self) -> str:
        return self._raw
    
    @property
    def lines(self) -> list[str]:
        return self._lines

@dataclass(eq = True)
class Vec3:
    x: float
    y: float
    z: float

    def __getitem__(self, index):
        match index:
            case 0: return self.x
            case 1: return self.y
            case 2: return self.z

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        return Vec3(self.x * other, self.y * other, self.z * other)
    
    def dot2d(lhs, rhs):
        return lhs.x * rhs.x + lhs.y * rhs.y

def parse_input(input: Input) -> list[tuple[Vec3, Vec3]]:
    return [tuple(Vec3(*[int(n) for n in part.split(",")]) for part in line.split("@")) for line in input.lines]


def det(a, b):
    return a.x * b.y - a.y * b.x

def line_intersection(start0, dir0, start1, dir1) -> Vec3 | None:
    end1 = start0 + dir0
    end2 = start1 + dir1
    xdiff = Vec3(start0.x - end1.x, (start1.x - end2.x), 0)
    ydiff = Vec3(start0.y - end1.y, (start1.y - end2.y), 0)
    
    div = det(xdiff, ydiff)
    if div == 0:
        return None
    
    d = Vec3(det(start0, end1), det(start1, end2), 0)
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    intersection = Vec3(x, y, 0)

    if Vec3.dot2d(intersection - start0, dir0) < 0 or Vec3.dot2d(intersection - start1, dir1) < 0:
        return None    
    return intersection

def solve_first(input: Input) -> object:
    hails = parse_input(input)
    area = (200000000000000, 400000000000000)
    sum = 0
    for h0, h1 in combinations(hails, 2):
        if i := line_intersection(*h0, *h1):
            if i.x >= area[0] and i.x <= area[1] and i.y >= area[0] and i.y <= area[1]:
                sum += 1
    return sum

def solve_second(input: Input) -> object:
    hails = parse_input(input)

    # Find 3 hails with different velocity to solve
    selected_hails = [hails[0]]
    for h in hails:
        if len(selected_hails) < 3 and not any(n for n in selected_hails if n[1] == h[1]):
            selected_hails.append(h)

    # Solve nonlinear system where the thrown rock collides with each of the other 3 rocks at a (different) time
    # start_pos + start_vel * t[n] == hail_pos + hail_vel * t[n]    (n = 0, 1, 2)
    start_pos = [Symbol("s_x"), Symbol("s_y"), Symbol("s_z")]
    start_vel = [Symbol("vel_x"), Symbol("vel_y"), Symbol("vel_z")]
    times = [Symbol("t0"), Symbol("t1"), Symbol("t2")]
    equations = []
    for i, h in enumerate(selected_hails):
        # pos.x + vel.x * t == hail.x + hail_vel.x * t   =>   0 = pos.x + vel.x * t - (hail.x + hail_vel.x * t)
        # pos.y + vel.y * t == hail.y + hail_vel.y * t   =>   0 = pos.y + vel.y * t - (hail.y + hail_vel.y * t)
        # pos.z + vel.z * t == hail.z + hail_vel.z * t   =>   0 = pos.z + vel.z * t - (hail.z + hail_vel.z * t)
        t = times[i]
        equations.append((start_pos[0] + start_vel[0] * t) - (h[0].x + h[1].x * t))
        equations.append((start_pos[1] + start_vel[1] * t) - (h[0].y + h[1].y * t))
        equations.append((start_pos[2] + start_vel[2] * t) - (h[0].z + h[1].z * t))
    res = tuple(nonlinsolve(equations, [*start_pos, *start_vel, *times]))[0]
    return res[0] + res[1] + res[2]

class Line:
    def __init__(self, line: str):
        """
            line is a string like: '19, 13, 30 @ -2,  1, -2'
                                    x0, y0, z0 @ dx, dy, dz
        """

        self.x0, self.y0, self.z0, self.dx, self.dy, self.dz = [int(el.strip())  for part in line.split("@") for el in part.split(',')]

        
    def __repr__(self):
        return f'({self.x0}, {self.y0}, {self.z0}) @ ({self.dx}, {self.dy}, {self.dz})'
    
    def __str__(self):
        return self.__repr__()

    def intersection(self, other, minB = 0, maxB = 0):
        """
            check if 2 lines sintersect between the x,y> min and x,y< max
                intersection must be after the starting point of the line
        """

        x, y, z, dx, dy, dz = self.x0, self.y0, self.z0, self.dx, self.dy, self.dz
        x1, y1, z1, dx1, dy1, dz1 = other.x0, other.y0, other.z0, other.dx, other.dy, other.dz
        
        """
         find if two lines intersect in 3D
        """
        # check if both lines are parallel
        if (dx == dx1 and dy == dy1 and dz == dz1):
            return False
        
        # create the segment from starting point to boundaries.
        # find the t value for self that mek the line hit the border
        # for x and dx
        if dx == 0:
            # line is vertical, won't touch the x border, t = 1e9
            tx = 1e9
        elif dx != 0:
            # getting the max t value for x, and I need t to be positive
            tx = max( (minB - x)/dx, (maxB - x)/dx )
        
        # for y and dy
        if dy == 0:
            ty = 1e9
        elif dy != 0:
            ty = max( (minB - y)/dy, (maxB - y)/dy )
        
        t1 = min(tx, ty) # the first to hit win.

        # creating the points to pass to the function
        p1, p2, p3, p4 = x, y, x+t1*dx, y+t1*dy

        # for x1 and dx1
        if dx1 == 0:
            tx1 = 1e9
        elif dx1 != 0:
            tx1 = max( (minB - x1)/dx1, (maxB - x1)/dx1 )
        
        # for y1 and dy1
        if dy1 == 0:
            ty1 = 1e9
        elif dy1 != 0:
            ty1 = max( (minB - y1)/dy1, (maxB - y1)/dy1 )
        
        t2 = min(tx1, ty1) # the first to hit win.

        # creating the points to pass to the function
        p5, p6, p7, p8 = x1, y1, x1+t2*dx1, y1+t2*dy1
        
        intr = edge_intersection(p1, p2, p3, p4, p5, p6, p7, p8)

        part_1 = 1 if len(intr) > 0 else 0
        part_2 = 0

        return part_1, part_2


if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    test = True
    if test:
        bmin = 7
        bmax = 27
    else:
        bmin = 200000000000000
        bmax = 400000000000000
    tf = aoc_utils.get_day_input(day, test)       
    input = Input(r'C:\Users\raikoug\SyncThing\shared_code_tests\adventOfCode\2023\day_24\input.txt')
    input_test= Input(r'C:\Users\raikoug\SyncThing\shared_code_tests\adventOfCode\2023\day_24\test_input.txt')
    part_1 = solve_first(input)
    part_2 = solve_second(input)
    ic(part_1, part_2)
