from random import randint, choice
from typing import Any
import heapq

## custom class with hashing and comparison methods
class Point:
    x: int
    y: int
    hashing: int
    cost: int

    def __init__(self, x, y, hashing):
        self.x = x
        self.y = y
        self.hashing = hashing
        self.cost = 0

    def __hash__(self) -> int:
        return self.hashing
    
    def __eq__(self, o: object) -> bool:
        return self.cost == o.cost
    
    def __lt__(self, o: object) -> bool:
        return self.cost < o.cost
    
    def __le__(self, o: object) -> bool:
        return self.cost <= o.cost
    
    def __gt__(self, o: object) -> bool:
        return self.cost > o.cost
    
    def __ge__(self, o: object) -> bool:
        return self.cost >= o.cost
    
    def __repr__(self) -> str:
        return f"({self.x}, {self.y}) -> {self.cost}"
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __add__(self, o: object) -> object:
        return Point(self.x + o.x, self.y + o.y, self.hashing*o.hashing*256*256)
    
    def distance(self, o: object) -> int:
        ## these are points in a carthesian plane, distance
        ## is the pitagorean distance
        dx = abs(self.x - o.x)
        dy = abs(self.y - o.y)
        return int((dx*dx + dy*dy)**0.5)

class Grid:
    points: list
    width: int
    height: int

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.points = list()
        self.init_points()
    
    def init_points(self):
        i = 0
        for row in range(self.height):
            tmp_row = list()
            for col in range(self.width):
                tmp_row.append(Point(col, row, i))
                i += 1
            self.points.append(tmp_row)

    def __str__(self) -> str:
        res = ""
        for row in self.points:
            for point in row:
                res += f"{point} "
            res += "\n"
        return res


my_set = set()
my_grid = Grid(10, 10)


# fake a path from (0,0) to (9,9)
Q = [[0, my_grid.points[0][0]]]
while Q:
    cost, point = heapq.heappop(Q)
    if point in my_set: continue
    my_set.add(point)
    if point.x == 9 and point.y == 9: break
    for dx, dy in [[-1,0], [0,1], [1,0], [0,-1]]:
        nx, ny = point.x + dx, point.y + dy
        if nx < 0 or ny < 0:
            continue
        else:
            try:
                new_point = my_grid.points[ny][nx]
                new_point.cost = cost + 1
                heapq.heappush(Q, [new_point.cost, new_point])
            except:
                pass

print(point)