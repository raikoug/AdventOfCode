from icecream import ic


class Brick:
    x_1: int
    y_1: int
    z_1: int
    x_2: int
    y_2: int
    z_2: int
    hashing: int

    def __init__(self, x_1, y_1, z_1, x_2, y_2, z_2, hashing):
        self.x_1 = x_1  # x_1 < x_2
        self.y_1 = y_1  # y_1 < y_2
        self.z_1 = z_1  # z_1 < z_2
        self.x_2 = x_2  # x_1 < x_2
        self.y_2 = y_2  # y_1 < y_2
        self.z_2 = z_2  # z_1 < z_2
        self.hashing = hashing

    def __hash__(self) -> int:
        return self.hashing
    
    def __eq__(self, o: object) -> bool:
        return all([self.x_1 == o.x_1, self.y_1 == o.y_1, self.z_1 == o.z_1, self.x_2 == o.x_2, self.y_2 == o.y_2, self.z_2 == o.z_2])
    
    def __lt__(self, o: object) -> bool:
        """
            a brick in a z positione lower than another brick is less than the other brick
            at same height, use hashing to compare     
        """
        return self.z_1 < o.z_1 or (self.z_1 == o.z_1 and self.hashing < o.hashing)
    
    def __le__(self, o: object) -> bool:
        return self.z_1 <= o.z_1 or (self.z_1 == o.z_1 and self.hashing <= o.hashing)
    
    def __gt__(self, o: object) -> bool:
        return self.z_1 > o.z_1 or (self.z_1 == o.z_1 and self.hashing > o.hashing)
    
    def __ge__(self, o: object) -> bool:
        return self.z_1 >= o.z_1 or (self.z_1 == o.z_1 and self.hashing >= o.hashing)
    
    def __repr__(self) -> str:
        return f"Brick - ({self.x_1}, {self.y_1}, {self.z_1}, {self.x_2}, {self.y_2}, {self.z_2}, {self.hashing})"
    
    def __str__(self) -> str:
        return self.__repr__()


class Tower:
    bricks: list
    current_hash: int
    max_x: int
    max_y: int
    max_z: int
    z_dict: dict

    def __init__(self, tf):
        self.bricks = list()
        self.current_hash = 0
        self.max_x = 0
        self.max_y = 0
        self.max_z = 0
        self.z_dict = dict()
        self.part_1_init_bricks(tf)
        
    def __str__(self) -> str:
        res = ""
        for brick in self.bricks:
            res += f"{brick}\n"
        return res
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def part_1_init_bricks(self, tf) -> list:
        self.bricks = list()
        i = 0
        for line in tf:
            # each line is 2 set of coordinate x,y,z separate by ~
            # 5,5,156~5,7,156
            parts = line.split('~')
            x_1,y_1,z_1 = [int(el) for el in parts[0].split(',')]
            x_2,y_2,z_2 = [int(el) for el in parts[1].split(',')]
            # x_1 < x_2  y_1 < y_2 z_1 < z_2  x_1 < x_2 y_1 < y_2  z_1 < z_2
            if x_1 != x_2: 
                if x_1 < x_2: 
                    brick = Brick(x_1, y_1, z_1, x_2, y_2, z_2, i)
                    self.bricks.append(brick)
                    if x_2 > self.max_x: self.max_x = x_2
                else:
                    brick = Brick(x_2, y_2, z_2, x_1, y_1, z_1, i)
                    self.bricks.append(brick)
                    if x_1 > self.max_x: self.max_x = x_1
            if y_1 != y_2: 
                if y_1 < y_2: 
                    brick = Brick(x_1, y_1, z_1, x_2, y_2, z_2, i)
                    self.bricks.append(brick)
                    if y_2 > self.max_y: self.max_y = y_2
                else:
                    brick = Brick(x_2, y_2, z_2, x_1, y_1, z_1, i)
                    self.bricks.append(brick)
                    if y_1 > self.max_y: self.max_y = y_1
            if z_1 != z_2: 
                if z_1 < z_2: 
                    brick = Brick(x_1, y_1, z_1, x_2, y_2, z_2, i)
                    self.bricks.append(brick)
                    if z_2 > self.max_z: self.max_z = z_2
                else:
                    brick = Brick(x_2, y_2, z_2, x_1, y_1, z_1, i)
                    self.bricks.append(brick)
                    if z_1 > self.max_z: self.max_z = z_1
            self.z_dict[min(z_1,z_2)] = brick
            i+=1

        # for the purpose I will create a brick to make the ground platform, ti will be insert(0,)
        #self.bricks.insert(0, Brick(0, 0, 0, self.max_x, self.max_y, 0, i))

        self.current_hash = i

    def gravity(self):
        # apply gravity, each brick is solid and won't split, just move down until it find another brick
        #  bricks are sorted by z position, so I can just iterate over the list, if x or y overlaps with something below
        #  it won't move.
        #   ground id 0, no brick can have z < 1
        
        for brick in self.bricks:
            if brick.z_1 == 0: continue
            current_z = min(brick.z_1, brick.z_2)
            for zbrick in self.z_dict[current_z-1]:
                # this brick is below, check if it overlaps
                pass




if __name__ == "__main__":
    import aoc_utils
    from pathlib import Path

    day = int(Path(__file__).name.split('_')[1])
    test = False
    tf = aoc_utils.get_day_input(day, test)
    t = Tower(tf)
    print(t)
    ic(t.max_x, t.max_y, t.max_z)