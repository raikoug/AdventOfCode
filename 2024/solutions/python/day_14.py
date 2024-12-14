from starter import AOC, CURRENT_YEAR
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass, field
from math import prod
import pygame 

CURRENT_DAY = int(Path(__file__).stem.replace('day_',''))
aoc = AOC(CURRENT_YEAR)

@dataclass
class Grid(list):
    @dataclass
    class Robot:
        row: int
        col: int
        row_speed: int
        col_speed: int
        grid: 'Grid'
        
        def tick(self, times: int = 1):
            # a tick is a 1s moveent
            self.row = (self.row +(self.row_speed * times)) % self.grid.max_row
            self.col = (self.col + (self.col_speed * times)) % self.grid.max_col
    
    max_row: int
    max_col: int
    robots: List[Robot] = field(default_factory=list)
    
    def add_robot(self, row: int, col: int, row_speed: int, col_speed: int):
        self.robots.append(Grid.Robot(row,col,row_speed,col_speed,self))
    
    def tick(self, times: int = 1):
        for robot in self.robots:
            robot.tick(times)

    def step_back(self):
        # Un passo indietro significa tick(-1)
        self.tick(-1)

    def where_are_robots(self) -> List[List[int]]:
        res : List[List[int]] = list()
        for robot in self.robots:
            res.append([robot.row,robot.col])
        return res    
    
    def stampa(self):
        def count_robot(robot,robot_list:list) -> str:
            if robot not in robot_list:
                return " "
            count = robot_list.count(robot)
            if count == 1: return "①"
            if count == 2: return "②"
            if count == 3: return "③"
            if count == 4: return "④"
            if count == 5: return "⑤"
            if count == 6: return "⑥"
            if count == 7: return "⑦"
            
        # caratteri per la griglia:
        # ┌ ─ │ ┐ └ ┘ ├ ┤ ┬ ┘ ┼ 
        robot_positions: List[List[int]] = self.where_are_robots()
        res = '┌' + '──┬'.join('' for _ in range(self.max_col)) + '──┐'
        s,m,e = "├", "┼", "┤"
        for row in range(self.max_row):
            res +=  ('\n│' + ' │'.join([count_robot([row,col],robot_positions) for col in range(self.max_col)]) + ' │')
            if row == self.max_row-1:
                s,m,e = "└", "┴", "┘"
            res +=  (f'\n{s}' + f'──{m}'.join('' for _ in range(self.max_col)) + f'──{e}')
        
        print(res)

    def stampa_2(self):
        def count_robot(robot,robot_list:list) -> str:
            if robot not in robot_list:
                return " "
            count = robot_list.count(robot)
            return "▇"
            
        # caratteri per la griglia:
        # ┌ ─ │ ┐ └ ┘ ├ ┤ ┬ ┘ ┼ 
        robot_positions: List[List[int]] = self.where_are_robots()
        res = ""
        for row in range(self.max_row):
            res +=  ('\n' + ''.join([count_robot([row,col],robot_positions) for col in range(self.max_col)]))
            
        
        print(res)
        
    
    def quadrants(self) -> List[List[int]]:
        half_row = self.max_row // 2
        half_col = self.max_col // 2
        q1 = [[robot.row,robot.col] for robot in self.robots if (robot.row < half_row and robot.col < half_col)]
        q2 = [[robot.row,robot.col] for robot in self.robots if (robot.row < half_row and robot.col > half_col)]
        q3 = [[robot.row,robot.col] for robot in self.robots if (robot.row > half_row and robot.col < half_col)]
        q4 = [[robot.row,robot.col] for robot in self.robots if (robot.row > half_row and robot.col > half_col)]
        
        return [q1,q2,q3,q4]
    
    
def solve_1(test_string = None) -> int:
    max_row = 7 if test_string else 103
    max_col = 11 if test_string else 101
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    g = Grid(max_row,max_col)
    for line in inputs_1.splitlines():
        position,speed = line.split(" ")
        position = position.replace("p=", "")
        speed = speed.replace("v=", "")
        col,row = position.split(",")
        row = int(row)
        col = int(col)
        col_speed,row_speed = speed.split(",")
        col_speed = int(col_speed)
        row_speed = int(row_speed)
        g.add_robot(row,col,row_speed,col_speed)
    g.tick(100)
    quadrants = g.quadrants()
    
    return prod([len(q) for q in quadrants])
    
def solve_2(test_string = None) -> int:
    max_row = 7 if test_string else 103
    max_col = 11 if test_string else 101
    inputs_1 = aoc.get_input(CURRENT_DAY, 1) if not test_string else test_string
    g = Grid(max_row,max_col)
    for line in inputs_1.splitlines():
        position,speed = line.split(" ")
        position = position.replace("p=", "")
        speed = speed.replace("v=", "")
        col,row = position.split(",")
        row = int(row)
        col = int(col)
        col_speed,row_speed = speed.split(",")
        col_speed = int(col_speed)
        row_speed = int(row_speed)
        g.add_robot(row,col,row_speed,col_speed)
    
    def get_input():
        res = input(" Inserisci un numero di step o [q|0] per uscire: ")
        if res.isdigit():
            return int(res)
        else:
            return 0
    
    # Inizializzazione Pygame
    pygame.init()
    cell_size = 10
    text_area_height = 50
    control_area_width = 240  # aumentiamo per avere spazio per i pulsanti

    screen_width = g.max_col * cell_size + control_area_width
    screen_height = g.max_row * cell_size + text_area_height

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Robots Simulation")

    # Inizializziamo il font
    pygame.font.init()
    font = pygame.font.SysFont(None, 24)

    running = True
    i = 0
    paused = False  
    clock = pygame.time.Clock()

    # Input box states
    go_to_tick_str = ""
    jump_size_str = "1"  # Default jump size
    active_box = 0  # 0 = none, 1 = go_to_tick, 2 = jump_size
    jump_size = 1

    # Posizioni input box
    box_width = 100
    box_height = 30
    box_left = g.max_col * cell_size + 20

    go_to_tick_box_top = 20
    jump_size_box_top = go_to_tick_box_top + box_height + 20

    # Pulsanti "Apply"
    button_width = 60
    button_height = 30
    go_to_tick_button_rect = pygame.Rect(box_left + box_width + 10, go_to_tick_box_top, button_width, button_height)
    jump_size_button_rect = pygame.Rect(box_left + box_width + 10, jump_size_box_top, button_width, button_height)

    def draw_input_box(x, y, w, h, text, active, label):
        color = (255,255,255) if active else (200,200,200)
        pygame.draw.rect(screen, color, (x, y, w, h))
        pygame.draw.rect(screen, (0,0,0), (x, y, w, h), 2)
        txt_surf = font.render(text, True, (0,0,0))
        screen.blit(txt_surf, (x+5, y+(h-txt_surf.get_height())//2))
        lbl_surf = font.render(label, True, (255,255,255))
        screen.blit(lbl_surf, (x, y - 20))

    def draw_button(rect: pygame.Rect, text: str):
        pygame.draw.rect(screen, (100,100,100), rect)
        pygame.draw.rect(screen, (0,0,0), rect, 2)
        txt_surf = font.render(text, True, (255,255,255))
        screen.blit(txt_surf, (rect.x + (rect.width - txt_surf.get_width())//2,
                               rect.y + (rect.height - txt_surf.get_height())//2))

    def apply_go_to_tick():
        nonlocal go_to_tick_str, i
        if go_to_tick_str.isdigit():
            target_tick = int(go_to_tick_str)
            diff = target_tick - i
            if diff != 0:
                g.tick(diff)  # avanza o indietreggia di diff
                i = target_tick

    def apply_jump_size():
        nonlocal jump_size_str, jump_size
        if jump_size_str.isdigit():
            jump_size = int(jump_size_str)
        else:
            jump_size_str = str(jump_size)
        print(jump_size)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_RIGHT:
                    if paused:
                        g.tick(jump_size)
                        i += jump_size
                elif event.key == pygame.K_LEFT:
                    if paused:
                        g.tick(-jump_size)
                        i -= jump_size
                elif event.key == pygame.K_ESCAPE:
                    running = False
                    print("Number of ticks:", i)
                elif event.key == pygame.K_TAB:
                    if active_box == 1:
                        active_box = 2
                    elif active_box == 2:
                        active_box = 1
                    else:
                        active_box = 1
                elif event.key == pygame.K_RETURN:
                    if active_box == 1:
                        apply_go_to_tick()
                    elif active_box == 2:
                        apply_jump_size()
                elif active_box != 0:
                    if event.key == pygame.K_BACKSPACE:
                        if active_box == 1:
                            go_to_tick_str = go_to_tick_str[:-1]
                        else:
                            jump_size_str = jump_size_str[:-1]
                    else:
                        if event.unicode.isdigit():
                            if active_box == 1:
                                go_to_tick_str += event.unicode
                            else:
                                jump_size_str += event.unicode
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                # Controllo input box
                if (box_left <= mx <= box_left+box_width) and (go_to_tick_box_top <= my <= go_to_tick_box_top+box_height):
                    active_box = 1
                elif (box_left <= mx <= box_left+box_width) and (jump_size_box_top <= my <= jump_size_box_top+box_height):
                    active_box = 2
                # Controllo pulsanti
                elif go_to_tick_button_rect.collidepoint(mx, my):
                    apply_go_to_tick()
                elif jump_size_button_rect.collidepoint(mx, my):
                    apply_jump_size()
                else:
                    # Clic fuori dalle box
                    active_box = 0

        if not paused:
            g.tick(jump_size)
            i += jump_size

        screen.fill((0,0,0))  
        # Disegno robots
        robot_positions = g.where_are_robots()
        for (r,c) in robot_positions:
            rect = pygame.Rect(c*cell_size, r*cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (0,255,0), rect)

        # Testo sotto
        ticks_text = f"Ticks: {i}"
        commands_text = "Space: Pause/Play | Right: +N Ticks | Left: -N Ticks | ESC: Quit | Tab: Switch box"
        
        ticks_surf = font.render(ticks_text, True, (255,255,255))
        commands_surf = font.render(commands_text, True, (255,255,255))
        
        text_start_y = g.max_row * cell_size
        screen.blit(ticks_surf, (10, text_start_y + 5))
        screen.blit(commands_surf, (10, text_start_y + 25))

        # Box e pulsanti a destra
        draw_input_box(box_left, go_to_tick_box_top, box_width, box_height, go_to_tick_str, active_box==1, "Go To Tick")
        draw_button(go_to_tick_button_rect, "Apply")

        draw_input_box(box_left, jump_size_box_top, box_width, box_height, jump_size_str, active_box==2, "Jump Size")
        draw_button(jump_size_button_rect, "Apply")

        pygame.display.flip()
        pygame.time.delay(100)

    pygame.quit()
    return i


if __name__ == "__main__":
    test = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""
    test_singolo = "p=2,4 v=2,-3"
    print(f"Part 1: {solve_1()}")
    print(f"Part 2: {solve_2()}")