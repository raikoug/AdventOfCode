from icecream import ic

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
# S is the starting position of the animal; there is a pipe on this


PM = {
    "|": [[1, 0], [-1, 0]],
    "-": [[0, 1], [0, -1]],
    "L": [[-1,0], [0, 1]],
    "J": [[-1,0], [0, -1]],
    "7": [[1,0], [0, -1]],
    "F": [[1,0], [0, 1]]
}

class Worm:
    def __init__(self, row, col):
        # initial position in the matrix
        self.row = row
        self.col = col
        # previous position in the matrix
        self.prev_x = row
        self.prev_y = col
        self.symbol = "S"
        self.all_moves = list()

        
    def move(self, row, col, M):
        # move the worm to the new position
        self.all_moves.append([row,col])
        self.prev_x = self.row
        self.prev_y = self.col
        self.row = row
        self.col = col
        self.symbol = M[self.row][self.col]

        
#
    def first_move(self, M):
        # the possible pipes, theis symbols, and the direction of the worm compatible with the pipe
        #    -  this has to be left or right
        #    |  this has to be up or down
        #    F  this has to be up or left
        #    7  this has to be up or right
        #    J  this has to be down or left
        #    L  this has to be down or right

        # the 4 possible tiles where to move, along with possible pipes 
        tyles =    [[self.row - 1, self.col], [self.row + 1, self.col], [self.row, self.col - 1], [self.row, self.col + 1]]
        ok_pipes = [["|", "F", "7"],           ["|", "L", "J"],           ["-", "L", "F"],           ["-", "J", "7"]]
        #            going up                  going down                  going left                 going right                       
        # remove the previous position to avoid crawling back
        try:
            tyles.remove([self.prev_x, self.prev_y])
        except:
            # probably first moev
            pass

        # remove any impossible move with row or col < 0 or > len(M)
        tyles = [t for t in tyles if t[0] >= 0 and t[1] >= 0 and t[0] < len(M) and t[1] < len(M[0])]

        ic(tyles)

        # check sourrounding tiles, retunr the first correct, at fest there will be 2, ignore
        for i,t in enumerate(tyles):
            try:
                m_tyle = M[t[0]][t[1]]
                if m_tyle in ok_pipes[i]:
                    self.move(t[0], t[1], M)
                    return t
            except Exception as e:
                # normally out of index
                ic(e)
                pass
        ic("no move found")

    def next_move(self, M):
        # give the actual position of the worm, the pipe and the previous position, next move is just 1
        #    based on the actual tile:
        #    -  have to go left or right
        #    |  have to go up or down
        #    F  have to go up or right
        #    7  have to go down or left
        #    J  have to go down or left
        #    L  have to go up or right

        current_tile = M[self.row][self.col]
        #ic(current_tile)
        directions = PM[current_tile]
        #ic(directions)
        possible_moves = [[self.row + d[0], self.col + d[1]] for d in directions]
        #ic(possible_moves)
        previous_pos = [self.prev_x, self.prev_y]
        #ic(previous_pos)

        # remove previous position from possible moves
        possible_moves.remove(previous_pos)
        #ic(possible_moves)
        
        # only 1 move left, take it
        self.move(possible_moves[0][0], possible_moves[0][1], M)

if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)
    
    # istantiate worm on S smbol in the 2d matrix tf

    for row in tf:
        if "S" in row:
            worm = Worm(tf.index(row), row.index("S"))
            break
    total = 0
    ic(worm.row, worm.col)
    ic(worm.first_move(tf))
    total += 1

    while worm.symbol != "S":
        worm.next_move(tf)
        #ic("next move:", worm.row, worm.col)
        total += 1
    ic(total/2)
    
    #ic(worm.all_moves)
   
    # write TF to file, and count points, maybe...
    total_inside_tiles = 0
    with open("TF", "w", encoding="utf8") as f:
        for i,row in enumerate(tf):
            we_are_inside = False   # this will change to true each time we have 
                                    # we have a "vertical" pipe: | or L or J
            for j,col in enumerate(row):
                if [i,j] in worm.all_moves:
                    # replace the worm path with ─ │ ┌ ┐ └ ┘ corresponding to the direction of the worm
                    if col == "J": 
                        f.write("┘")
                        we_are_inside = not we_are_inside
                    elif col == "L": 
                        f.write("└")
                        we_are_inside = not we_are_inside
                    elif col == "7": f.write("┐")
                    elif col == "F": f.write("┌")
                    elif col == "|": 
                        f.write("│")
                        we_are_inside = not we_are_inside
                    elif col == "-": f.write("─")
                    elif col == "S": f.write("S")
                else:
                    if we_are_inside:
                        total_inside_tiles += 1
                        f.write("█")
                    else:
                        f.write(" ")
            f.write("\n")
    ic(total_inside_tiles)

    