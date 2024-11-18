from icecream import ic
import heapq
import aoc_utils
from pathlib import Path

# variant of Dijkstra's algorithm, with the constraing of not going straight 3 times in row
#  "straight" has no sense in Dijkstra's algorithm, implementing this constraint is not fun.

# possible Next Moves
N = [[-1,0], [0,1], [1,0], [0,-1]]
#      0      1      2      3  
# (i+2) % 4 of any of the above directions is it's opposite direction

day = int(Path(__file__).name.split('_')[1])
tf = aoc_utils.get_day_input(day)

GRID=[[col for col in row] for row in tf]
MAX_Row = len(GRID)
MAX_Col = len(GRID[0])


# queue with
# distance: The current total distance from the starting point to the current position (row, col). 
#       This is initially set to 0 for the starting position.
# row: The current row index in the grid.
# col: The current column index in the grid.
# direction: The index of the current direction in the N list. The N list contains four pairs 
#       of coordinates, each representing a direction (up, right, down, left). This is initially 
#       set to -1, which means no direction has been taken yet.
# cons_dir: The number of consecutive steps taken in the current direction. This is initially set to 0.
QUEUE=[(0,0,0,-1,0)]

# this is archive with all already evaluated queue items
# since the heapq heapop get alwasy the best distance first
# we can skip all already evaluated items
D = dict()

while QUEUE:
    distance, row, col, direction, cons_dir = heapq.heappop(QUEUE)
    # direcction and cons_dir are used to implement the constraint, hence 
    #  even though we already have evaulated this position, we can't skip it
    #  if the direction and cons_dir are different
    if (row, col, direction, cons_dir) in D:
        continue
    D[(row, col, direction, cons_dir)] = distance
    for i,[dir_col, dir_row] in enumerate(N):
        # next position
        new_row = row + dir_row
        new_col = col + dir_col
        # new direction
        new_dir = i
        # evaluate consesutive straight moves
        new_cons_dir = 1 if direction != new_dir else cons_dir + 1
        # checking is we are inside the grid and if we are not going straight 3 times in a row
        # and if we are not going back (that we cannot!)
        if all([
            0<=new_row<MAX_Row,
            0<=new_col<MAX_Col,
            new_cons_dir <= 3, # no more than 3 straight moves
            ((new_dir+2)%4) != direction # not going back
        ]):
            value = int(GRID[new_row][new_col])  # new distance
            # add to the queue
            heapq.heappush(QUEUE, (distance + value, new_row, new_col, new_dir, new_cons_dir))

# now in D we have all the possible paths, to all the possible positions
#ic(D)

result = 100000000
end_path = [MAX_Row-1, MAX_Col-1]

possible_paths = [v for k,v in D.items() if k[0:2] == tuple(end_path)]
ic (possible_paths)

print(min(possible_paths))
    