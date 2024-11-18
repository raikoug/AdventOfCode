import heapq
from icecream import ic

D = [[-1,0], [0,1], [1,0], [0,-1]] # directions


## custom class with hashing and comparison methods
class Point:
    row: int
    col: int
    hashing: int
    cost: int
    value: str

    def __init__(self, row, col, value, hashing):
        self.row = row
        self.col = col
        self.hashing = hashing
        self.cost = 0
        self.value = value

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
        return Point(self.row + o.row, self.col + o.col, self.hashing*o.hashing*256*256)
    
    def distance(self, o: object) -> int:
        ## these are points in a carthesian plane, distance
        ## is the pitagorean distance
        drow = abs(self.row - o.row)
        dcol = abs(self.col - o.col)
        return int((drow*drow + dcol*dcol)**0.5)

class Grid:
    points: list
    width: int
    height: int

    def __init__(self, tf):
        self.width = 0
        self.height = 0
        self.points = list()
        self.init_points(tf)
    
    def init_points(self, tf):
        i = 0
        for x, row in enumerate(tf):
            tmp_row = list()
            for y,col in enumerate(row):
                tmp_row.append(Point(x, y, col, i))
                i += 1
            self.points.append(tmp_row)
        self.width = len(self.points[0])
        self.height = len(self.points)

    def __str__(self) -> str:
        res = ""
        for row in self.points:
            for point in row:
                res += f"{point} "
            res += "\n"
        return res

    def get_neighbors(self, row, col):
        for d in D:
            nr = row + d[0]
            nc = col + d[1]
            if 0 <= nr < self.height and 0 <= nc < self.width:
                point = self.points[nr][nc]
                if point.value != '#':
                    yield point

    def next_path_options(self, path) -> list:
        row, col = path.visited[-1]
        for neighbor in self.get_neighbors(row, col):
            if (neighbor.row, neighbor.col) not in path.visited:
                yield neighbor

class MyPath:
    visited: set
    cost: int
    row: int
    col: int

    def __init__(self, row, col):
        self.visited = list()
        self.row = row
        self.col = col
        self.add(row, col)
        cost = 0


    def __str__(self) -> str:
        return str(self.visited)
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def add(self, row, col):
        if (row, col) not in self.visited:
            self.visited.append((row, col))

if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    test = False
    tf = aoc_utils.get_day_input(day, test)

    grid = Grid(tf)
    paths = list()
    start_x = 0
    start_y = 1
    end_x = grid.height - 1
    end_y = grid.width - 2
    best = None
    
    # add a first path
    paths.append(MyPath(start_x, start_y))
    Q = [paths[0]]
    ic(paths)

    # For part one: False, for part 2 True
    ignore_slopes = True

    # we want the longest path without visiting the same point twice
    while Q:
        for path in Q:
            if path.row == end_x and path.col == end_y:
                cost = len(path.visited)
                if not best:
                    best = path
                elif len(best.visited) < cost:
                    best = path
                Q.remove(path)
                continue
            for neighbor in grid.next_path_options(path):
                # we already exluded visited points, and impossible points
                # if the actual point value is v or >, we have to take 2 steps in that direction

                # we kill the actual path and new path for each neighbor
                new_p = MyPath(neighbor.row, neighbor.col)
                new_p.visited = path.visited.copy()
                new_p.cost = len(new_p.visited) - 1

                if ignore_slopes:
                    # move the neighbors, it is a .
                    new_p.cost = new_p.cost + 1
                    new_p.add(neighbor.row, neighbor.col)
                    Q.append(new_p)
                elif neighbor.value == 'v':
                    new_p.cost = new_p.cost + 2
                    # move 2 steps down and add them in the visited
                    new_p.add(neighbor.row, neighbor.col)
                    # check if the next step is already visited
                    if (neighbor.row + 1, neighbor.col) not in new_p.visited:
                        new_p.add(neighbor.row + 1, neighbor.col)
                        Q.append(new_p)
                elif neighbor.value == '>':
                    new_p.cost = new_p.cost + 2
                    # move 2 steps right and add them in the visited
                    new_p.add(neighbor.row, neighbor.col)
                    # check if the next step is already visited
                    if (neighbor.row, neighbor.col + 1) not in new_p.visited:
                        new_p.add(neighbor.row, neighbor.col + 1)
                        Q.append(new_p)
                else:
                    # move the neighbors, it is a .
                    new_p.cost = new_p.cost + 1
                    new_p.add(neighbor.row, neighbor.col)
                    Q.append(new_p)
            Q.remove(path)
    print(best.cost)




