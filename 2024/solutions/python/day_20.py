from starter import AOC, CURRENT_YEAR
from pathlib import Path
import heapq
from collections import deque, defaultdict


CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

def solve_1(test_string=None):
    saving_max = 20 if test_string else 100
    inp = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    grid = [list(r) for r in inp.splitlines()]
    H, W = len(grid), len(grid[0])
    start = end = None
    for i in range(H):
        for j in range(W):
            if grid[i][j]=='S':
                start=(i,j)
            if grid[i][j]=='E':
                end=(i,j)

    def neighbors(r,c):
        for nr,nc in [(r+1,c),(r-1,c),(r,c+1),(r,c-1)]:
            if 0<=nr<H and 0<=nc<W:
                yield nr,nc

    def dijkstra(startpos, block_walls=True):
        dist = [[999999]*W for _ in range(H)]
        sr,sc=startpos
        dist[sr][sc]=0
        pq=[(0,sr,sc)]
        while pq:
            d,r,c=heapq.heappop(pq)
            if d>dist[r][c]: continue
            for nr,nc in neighbors(r,c):
                if not block_walls or grid[nr][nc]!='#':
                    nd=d+1
                    if nd<dist[nr][nc]:
                        dist[nr][nc]=nd
                        heapq.heappush(pq,(nd,nr,nc))
        return dist

    base_dist = dijkstra(start)[end[0]][end[1]]
    dist_from_start = dijkstra(start, True)
    dist_from_end = dijkstra(end, True)
    
    # ABOMINATION!!!
    res=0
    for r in range(H):
        for c in range(W):
            if dist_from_start[r][c]<999999:
                # first cheat step
                for nr1,nc1 in neighbors(r,c):
                    # can go through walls
                    for nr2,nc2 in neighbors(nr1,nc1):
                        # can go through walls again
                        if 0<=nr2<H and 0<=nc2<W and grid[nr2][nc2]!='#':
                            if dist_from_end[nr2][nc2]<999999:
                                saving = base_dist-(dist_from_start[r][c]+2+dist_from_end[nr2][nc2])
                                if saving>=saving_max:
                                    res+=1
    return res

def solve_2(test_string=None):
    saving_max = 70 if test_string else 100
    inp = aoc.get_input(CURRENT_DAY,1) if not test_string else test_string

    input_grid = inp.splitlines()
    threshold = saving_max  

    R = len(input_grid)
    C = len(input_grid[0])
    grid = [list(row) for row in input_grid]

    # Trova S e E
    start = None
    end = None
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 'S':
                start = (r,c)
            elif grid[r][c] == 'E':
                end = (r,c)

    dirs = [(-1,0),(1,0),(0,-1),(0,1)]
    def in_bounds(x,y):
        return 0 <= x < R and 0 <= y < C

    # BFS per trovare distanze no-cheat da S
    def bfs_no_cheat(start):
        dist = [[-1]*C for _ in range(R)]
        sr,sc = start
        dist[sr][sc]=0
        q=deque([start])
        while q:
            x,y = q.popleft()
            d = dist[x][y]
            for dx,dy in dirs:
                nx,ny = x+dx,y+dy
                if in_bounds(nx,ny) and grid[nx][ny] != '#' and dist[nx][ny]<0:
                    dist[nx][ny]=d+1
                    q.append((nx,ny))
        return dist

    dist_from_S = bfs_no_cheat(start)
    dist_to_E = bfs_no_cheat(end)
    dist_base = dist_from_S[end[0]][end[1]]

    if dist_base < 0:
        return 0

    found_cheats = set()

    start_cells = []
    for r in range(R):
        for c in range(C):
            if dist_from_S[r][c]>=0:
                if grid[r][c] != '#': 
                    start_cells.append((r,c))

    max_cheat_len = 20

    for (sr,sc) in start_cells:
        base_dist = dist_from_S[sr][sc]
        dist_cheat = [[-1]*C for _ in range(R)]
        dist_cheat[sr][sc]=0
        q = deque([(sr,sc)])
        while q:
            x,y = q.popleft()
            d = dist_cheat[x][y]
            if d == max_cheat_len:
                continue
            for dx,dy in dirs:
                nx,ny = x+dx,y+dy
                if in_bounds(nx,ny):
                    if dist_cheat[nx][ny]<0:
                        dist_cheat[nx][ny]=d+1
                        q.append((nx,ny))

        for r2 in range(R):
            for c2 in range(C):
                cheat_len = dist_cheat[r2][c2]
                if cheat_len>0 and cheat_len<=max_cheat_len: 
                    if grid[r2][c2] != '#' and dist_to_E[r2][c2]>=0:
                        total_time_cheat = base_dist  
                        total_time_cheat = base_dist - dist_from_S[end[0]][end[1]] + (dist_from_S[sr][sc] + cheat_len + dist_to_E[r2][c2])
                        saving = dist_base - (dist_from_S[sr][sc] + cheat_len + dist_to_E[r2][c2])

                        if saving>=threshold:
                            cheat_id = ((sr,sc),(r2,c2))
                            found_cheats.add(cheat_id)

    return len(found_cheats)


if __name__ == "__main__":

    test = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""
    print(f"Part 1: {solve_1(test)}")
    print(f"Part 2: {solve_2(test)}")
