from icecream import ic

""" (my arrows :D →←↑↓)
   symbols in the data represents mirrors. Behaviors of the laser beam are as follows:
        • beam coming from left →
            - '\' : changes direction down
            - '/' : changes direction up
            - '|' : split into two beams going down and up
            - '-' : continue in the same direction
        • beam coming from right ←
            - '\' : changes direction up
            - '/' : changes direction down
            - '|' : split into two beams going down and up
            - '-' : continue in the same direction
        • beam coming from down ↑
            - '\' : changes direction left
            - '/' : changes direction right
            - '|' : continue in the same direction
            - '-' : split into two beams going left and right
        • beam coming from up ↓
            - '\' : changes direction right
            - '/' : changes direction left
            - '|' : continue in the same direction
            - '-' : split into two beams going left and right
    
    Beam will start from 0,0 direction right →
        Beam could end outside the matrix, and would die.
        Beam could end in a loop, as soon I discover it is a loop, kill the beam
    
    When no more beams are present, count the tyles with len(ener) > 0
"""

D ={
    '→' : (0,1),
    '←' : (0,-1),
    '↑' : (-1,0),
    '↓' : (1,0)
}

class Tyle:
    row: int
    col: int
    s: str
    ener = list()  # contains the direction it has been energized with '→←↑↓'

    def __init__(self, row, col, s, ener = list()):
        self.row = row
        self.col = col
        self.s = s
        self.ener = ener

class Beam:
    row: int
    col: int
    dir: str # →←↑↓

    def __init__(self, row: int, col: int, dir: str):
        self.row = row
        self.col = col
        self.dir = dir

class Game:
    tyles: list
    field: list
    beams: list

    def __init__(self, tf):
        self.tyles = list()
        for i,row in enumerate(tf):
            row_t = list()
            for j,col in enumerate(row):
                row_t.append(Tyle(i, j, col, list()))
            self.tyles.append(row_t)
        self.beams = list()
        self.field = tf

        
    
    def play_step(self):
        # for each beam, go to ne next tyle and evaulate it
        for beam in list(self.beams):
            beam.row += D[beam.dir][0]
            beam.col += D[beam.dir][1]

            # if beam is outside the matrix, kill it
            if any(
                [
                    beam.row < 0, 
                    beam.row >= len(self.tyles), 
                    beam.col < 0, 
                    beam.col >= len(self.tyles[0])
                ]):
                self.beams.remove(beam)
                continue

            next_tyle = self.tyles[beam.row][beam.col]
            # if energized with the same direction as the beam, kill the beam
            if beam.dir in next_tyle.ener:
                self.beams.remove(beam)
                continue

            # energize the tyle with the beam direction
            next_tyle.ener.append(beam.dir)

            # evaluate the tyle
            match next_tyle.s: # \ / - |
                case '|':
                    match beam.dir: # → ← ↑ ↓
                        case '→' | '←':  # don't care, result is the same
                            # i kill the beam and create two new beams
                            self.beams.remove(beam)
                            self.beams.append(Beam(beam.row, beam.col, "↑"))
                            self.beams.append(Beam(beam.row, beam.col, "↓"))
                case '-':
                    match beam.dir: # → ← ↑ ↓
                        case '↑' | '↓': # don't care, result is the same
                            # i kill the beam and create two new beams
                            self.beams.remove(beam)
                            self.beams.append(Beam(beam.row, beam.col, "→"))
                            self.beams.append(Beam(beam.row, beam.col, "←"))
                case '\\':
                    match beam.dir: # → ← ↑ ↓  -> in these case the beam doesn't die, jus tchange direction
                        case '→':
                            beam.dir = "↓"
                        case '←':
                            beam.dir = "↑"
                        case '↑':
                            beam.dir = "←"
                        case '↓':
                            beam.dir = "→"
                case '/':
                    match beam.dir:
                        case '→':
                            beam.dir = "↑"
                        case '←':
                            beam.dir = "↓"
                        case '↑':
                            beam.dir = "→"
                        case '↓':
                            beam.dir = "←"

    def print_field(self):
        for row in self.tyles:
            for tyle in row:
                ts = tyle.ener[0] if tyle.ener else tyle.s
                print(ts, end="")
            print()
        print()

    def count_energized_tyles(self):
        return len([t for sub in self.tyles for t in sub if len(t.ener)>0])

def calculate_beams_starts(tf: list)-> list:
    res = list()
    # left side
    c = -1
    r = [i for i in range(len(tf))]
    d = "→"
    res += [(r,c,d) for r in r]

    # right side
    c = len(tf[0])
    # same r
    d = "←"
    res += [(r,c,d) for r in r]

    # top side
    r = -1
    c = [i for i in range(len(tf[0]))]
    d = "↓"
    res += [(r,c,d) for c in c]

    # bottom side
    r = len(tf)
    # same c
    d = "↑"
    res += [(r,c,d) for c in c]

    return res

if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    tf = aoc_utils.get_day_input(day)

    # PART_1
    game = Game(tf)
    # start the beam from outside so the first tyle is accounted too :D
    game.beams.append(Beam(0,-1,"→"))
    while len(game.beams) > 0:
        game.play_step()
        #game.print_field()
    ic("PART_1", game.count_energized_tyles())

    possible_beam_starts = calculate_beams_starts(tf)
    maximum = 0
    for beam_start in possible_beam_starts:
        r,c,d = beam_start
        game = Game(tf)
        game.beams.append(Beam(r,c,d))
        while len(game.beams) > 0:
            game.play_step()
            
        res = game.count_energized_tyles()
        if res > maximum:
            maximum = res
            best_beam = beam_start
        #ic(beam_start, res)
    ic("PART_2", best_beam, maximum)
    