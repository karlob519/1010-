# Imports
import pygame
import random
import sys

# Display
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
board = pygame.Surface((400, 400))
pygame.display.set_caption('1010!')
score_font = pygame.font.SysFont('Calibri', 50)
score_pos = (30, 100)
ariel = pygame.font.SysFont('Ariel', 50)

# Clock
clock = pygame.time.Clock()
FPS = 30

# Colours
black = (0, 0, 0)
white = (255, 255, 255)
orange = (255, 128, 10)
light_grey = (200, 200, 200)
dark_grey = (50, 50, 50)
light_blue = (20, 150, 250)
dark_blue = (1, 47, 200)
bright_green = (10, 250, 50)
dark_green = (2, 120, 30)
red = (250, 0, 30)
dark_brown = (142, 92, 71)
light_brown = (240, 217, 181)
yellow = (250, 250, 5)
purple = (160, 50, 120)
bg_colour = black

# Setting up the initial state and some constants like the size of the squares and starting 
# positions of the board and three random shapes
screen.fill(bg_colour)
sqr_size = 40

start_x, start_y = 200, 20
start_pos = (start_x, start_y)

pos_1 = (100, 550)
pos_2 = (350, 550)
pos_3 = (600, 550)
positions = [pos_1, pos_2, pos_3]
buttons = []

# Dictionary containing instructions on how to build different shapes
shape_dict = {'2_square' : [(1, 0), (0, 1), (1, 1)], 'L_shape' : [(1, 0), (2, 0), (2, 1), (2, 2)],
              '2_line' : [(1, 0)], '5_line' : [(1, 0), (2, 0), (3, 0), (4, 0)], 
              '3_square' : [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (2, 2)],
              'r_shape' : [(1, 0), (0, 1)], '3_line' : [(1, 0), (2, 0)], 
              '4_line' :  [(1, 0), (2, 0), (3, 0)],'dot' : []}

colour_dict = {'2_square' : bright_green, 'L_shape' : dark_blue, '2_line' : yellow, '5_line' : red,
               '3_square' : light_blue, 'r_shape' : orange, '3_line' : purple, 'dot' : white,
               '4_line' : dark_green}


class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.colour = dark_grey
        self.occ = False
        self.num = 0
    
    def draw(self):
        pygame.draw.rect(board, self.colour, (self.x, self.y, sqr_size, sqr_size))
        

class Block:
    def __init__(self, start: tuple, name: str, num=0, pattern=None):
        self.start = start
        self.name = name[:-1]
        self.num = num
        self.pattern = pattern

        self.colour = colour_dict[self.name]
        self.coords = [start]
        start_x, start_y = start
        coord_list = shape_dict[self.name]

        for el in coord_list:
            tup = (start_x + el[0] * sqr_size, start_y + el[1] * sqr_size)
            self.coords.append(tup)

        self.value = len(self.coords)

        self.min_x = min([coord[0] for coord in self.coords])
        self.max_x = max([coord[0] for coord in self.coords])
        self.min_y = min([coord[1] for coord in self.coords])
        self.max_y = max([coord[1] for coord in self.coords])


    def update_coords(self, pattern=None):
        start_x, start_y = self.start
        self.coords = [self.start]
        if pattern is None:
            coord_list = shape_dict[self.name]
        else:
            coord_list = pattern
        for el in coord_list:
            tup = (start_x + el[0] * sqr_size, start_y + el[1] * sqr_size)
            self.coords.append(tup)
        self.min_x = min([coord[0] for coord in self.coords])
        self.max_x = max([coord[0] for coord in self.coords])
        self.min_y = min([coord[1] for coord in self.coords])
        self.max_y = max([coord[1] for coord in self.coords])


    def draw_block(self):
        if 'line' not in self.name and 'square' not in self.name: 
            for coords in self.coords:
                surface = pygame.Surface((sqr_size, sqr_size))
                x_surf, y_surf = 0, 0 
                sqr = Square(x_surf, y_surf)
                pygame.draw.rect(surface, self.colour, (x_surf, y_surf, sqr_size, sqr_size))
                draw_rect(bg_colour, sqr, surface)
                screen.blit(surface, coords)
        else:
            width = self.max_x - self.min_x + sqr_size
            height = self. max_y - self.min_y + sqr_size
            surface = pygame.Surface((width, height))
            start_coords = self.coords[0]
            x1, y1 = start_coords
            for coords in self.coords:
                x, y = coords
                x_surf, y_surf = x - x1, y - y1 
                sqr = Square(x_surf, y_surf)
                pygame.draw.rect(surface, self.colour, (x_surf, y_surf, sqr_size, sqr_size))
                draw_rect(bg_colour, sqr, surface)

            screen.blit(surface, start_coords)

        pygame.display.update()
    

    def erase(self):
        for coords in self.coords:
            surface = pygame.Surface((sqr_size, sqr_size))
            surface.fill(bg_colour)
            screen.blit(surface, coords)


class Button:
    """Create a button"""
    def __init__(self, text: str, colour: tuple, pos: tuple, font: int, func):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.change_text(text, colour)
        self.func = func
 

    def change_text(self, text: str, colour: tuple):
        """Change the text when you click"""
        self.text = self.font.render(text, 1, black)
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(colour)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
 

    def show(self, surface: pygame.Surface):
        surface.blit(self.surface, (self.x, self.y))
 

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    print('pressed')
                    self.func()
                else:
                    None

        
def draw_rect(colour: tuple, sqr: Square, canvas: pygame.Surface):
    for i in range(4):
        pygame.draw.rect(canvas, colour, (sqr.x+i,sqr.y+i,sqr_size+2,sqr_size+2), 1)
    return 


def setup():
    for i in range(10):
        for j in range(10):
            sqr = Square(i * sqr_size, j * sqr_size)
            sqr.num = i * 10 + j 
            dict_key = string(sqr.x, sqr.y)
            board_dict[dict_key] = sqr
            sqr.draw()
            draw_rect(bg_colour, sqr, board)
    screen.blit(board, start_pos)
    pygame.display.update()


def block_choice(coords: tuple, list_of_blocks: list) -> Block:
    '''
    Function which finds what block we are picking to place on the board
    '''
    x, y = coords
    choice = None

    for block in list_of_blocks:
        if x <= block.max_x + sqr_size and x >= block.min_x and y <= block.max_y + sqr_size and y >= block.min_y:
            choice = block
            break

    return choice


def sqrs_choice(block: Block) -> list:
    '''
    Function which returns the squares we have chosen based on where we drop a block
    '''
    sqrs_list = []

    for pos in block.coords:
        x, y = pos
        x, y = x - start_x, y - start_y
        x, y = round(x / 40) * 40, round(y / 40) * 40
        key = string(x, y)
        sqr = board_dict[key]
        sqrs_list.append(sqr)

    return sqrs_list


def stick_block(block: Block, sqrs: list):
    '''
    Drawing in the block on the board and removing the block from the game
    '''
    global active_blocks

    colour = colour_dict[block.name]

    for sqr in sqrs:
        sqr.colour = colour
        sqr.occ = True
        sqr.draw()
        draw_rect(bg_colour, sqr, board)
    
    block.erase()
    block.start = (1500, 1500)
    block.update_coords(pattern=block.pattern)
    active_blocks.remove(block)
    
    screen.blit(board, start_pos)
    pygame.display.update()


def string(x: int, y: int) -> str:
    return str(x) + '.' + str(y) 


def return_block(block: Block):
    global drag

    start_point = pos_dict[block.num]
    block.erase()
    block.start = start_point
    block.update_coords(pattern=block.pattern)
    screen.blit(board, start_pos)
    block.draw_block()
    drag = False
    return

    
def turn():
    global active_blocks, positions

    active_blocks = random.sample(blocks, k=3)

    for i in range(3):
        block, pos = active_blocks[i], positions[i]
        block.num = i + 1
        block.start = pos
        block.pattern = rotate_block(block)
        block.update_coords(pattern=block.pattern)

    recentre()
    for block in active_blocks:    
        block.draw_block()

    return 


def clear_animation(lines: list, delay_time: int):
    '''
    We animate clearings from the middle, with delay_time in milisecunds
    '''
    queue = {i : [] for i in range(5)}
    for line in lines:
        first_half, second_half = line[:5][::-1], line[5:]
        for i in range(5):
            if first_half[i] not in queue[i]:
                queue[i].append(first_half[i])
            else:
                None
            if second_half[i] not in queue[i]:
                queue[i].append(second_half[i])
            else:
                None
                
    for sqrs in queue.values():
        for sqr in sqrs:
            sqr.occ = False
            sqr.colour = dark_grey
            sqr.draw()
            draw_rect(bg_colour, sqr, board)
        screen.blit(board, start_pos)
        pygame.display.update()
        pygame.time.wait(delay_time)

    return


def hit():
    '''
    Function which checkes if we have filled a row or a column
    '''
    global board_dict, score
    
    clean_up = []   
 
    for row in rows:
        if sum([sqr.occ for sqr in row]) == 10:
            clean_up.append(row)
    for column in columns:    
        if sum([sqr.occ for sqr in column]) == 10:
            clean_up.append(column)
    
    if len(clean_up) != 0:
        score += len(clean_up) * 10
        clear_animation(clean_up, 45)
    else:
        None
    
    return


def draw_active_blocks(num: int):
    global active_blocks

    for block in active_blocks:
        if block.num != num:
            block.draw_block()

    return
    

def recentre():
    '''
    Recenters the blocks so they are evenly spaced
    '''
    global active_blocks, positions
    
    # Centers of mass for blocks
    for block in active_blocks:
        x_centre = sum(coords[0] for coords in block.coords) / block.value
        y_centre = sum(coords[1] for coords in block.coords) / block.value
        pos = positions[active_blocks.index(block)]
        pos_x, pos_y = pos
        new_x = block.start[0] + (pos_x - x_centre)
        new_y = block.start[1] + (pos_y - y_centre)
        block.start = (new_x, new_y)
        pos_dict[block.num] = block.start
        block.update_coords(pattern=block.pattern)
        
    return

def show_score():
    global score

    score_value = score_font.render(str(score), 1, red)
    surface = pygame.Surface((170, 60))
    surface.fill(bg_colour)
    screen.blit(surface, score_pos)
    screen.blit(score_value, score_pos)
    pygame.display.update()


# Rotations
def line_rotation(coord_list: list) -> list:
    '''
    Rotates a straight line by 90 degrees
    '''
    return_list = []
    for coords in coord_list:
        x, y = coords
        return_list.append((y, x))
    
    return return_list


def vertical_rotation(coord_list: list) -> list:
    return_list = []
    for coords in coord_list:
        x, y = coords
        return_list.append((x, -y))
    
    return return_list


def horizontal_rotation(coord_list: list) -> list:
    return_list = []
    for coords in coord_list:
        x, y = coords
        return_list.append((-x, y))
    
    return return_list


def rotate_block(block: Block) -> list:
    random_number = random.randint(1, 4)
    old_pattern = shape_dict[block.name]

    if 'line' in block.name:
        if random_number % 2 == 1:
            return line_rotation(old_pattern)
        else:
            return old_pattern

    elif 'shape' in block.name:
        if random_number == 1:
            return horizontal_rotation(old_pattern)
        elif random_number == 2:
            return vertical_rotation(old_pattern)
        elif random_number == 3:
            return vertical_rotation(horizontal_rotation(old_pattern))
        else:
            return old_pattern

    else:
        return old_pattern


# Defining what a loss is
def pattern_to_digit(coords: tuple, start_num: int) -> int:
    '''
    Converts a set of coordinates into a number which we will use to find the squares
    if the game is lost
    '''
    x, y = coords
    number = start_num + x + y * 10
    return number


def shape_to_list(block: Block, sqr_num: int) -> list:
    '''
    Returns a list of squares needed if the shape would fit
    '''
    out_list = [sqr_num]
    for coords in block.pattern:
        number = pattern_to_digit(coords, sqr_num)
        out_list.append(number)
    
    return set(out_list)


def can_fit(block: Block) -> bool:
    '''
    Returns True if a given block can fit on the board, False otherwise
    '''
    count = 0
    free_sqr_nums = set([sqr.num for sqr in board_dict.values() if sqr.occ is False])
    for number in list(free_sqr_nums):
        sqrs_recc = shape_to_list(block, number)
        if sqrs_recc.issubset(free_sqr_nums):
            count = 1
            break
        else:
            None

    return count == 1
        

def loss():
    '''
    Returns True if the game is lost, meaning we cannot place any of the remaining blocks
    '''
    count = 0
    for block in active_blocks:
        try:
            if not can_fit(block):
                count += 1
            else:
                None
        except ValueError:
            count += 1
    return count == len(active_blocks) and len(active_blocks) != 0


def start_again():
    global score, buttons

    score = 0
    buttons = []
    screen.fill(bg_colour)
    score_str = score_font.render('Score :', 1, red)
    screen.blit(score_str, (20, 30))

    setup()
    turn()
    show_score()


# Game over menu
def game_over():
    # Buttons
    yes_button = Button('PLAY AGAIN', bright_green, (610, 180), 30, start_again)
    no_button = Button('QUIT', red, (650, 260), 30, sys.exit)
    yes_button.show(screen)
    no_button.show(screen)
    buttons.append(yes_button)
    buttons.append(no_button)

    # 'Game Over' text
    text = ariel.render('Game Over', 1, white)
    screen.blit(text, (610, 100))

    pygame.display.update()
    

# Dictionary containing the positions of squares on the board as the keys 
# and the squares themselves as values
board_dict = dict()

# Positional dictionary
pos_dict = {1 : pos_1, 2 : pos_2, 3 : pos_3}

# List of all possible block shapes
block_names = ['2_square1', 'L_shape1', '2_line1', '5_line1', '3_square1', 'r_shape1', '3_line1', 'dot1', '4_line1',
               '2_square2', 'L_shape2', '2_line2', '5_line2', '3_square2', 'r_shape2', '3_line2', 'dot2', '4_line2',
               '2_square3', 'L_shape3', '2_line3', '5_line3', '3_square3', 'r_shape3', '3_line3', 'dot3', '4_line3']

blocks = [Block((100 * k, 1500), block_names[k]) for k in range(18)]

# Keeping track of active blocks that need to be placed on the board
active_blocks = []

setup()
turn()

# Creating the rows and columns lists
sqrs_list = list(board_dict.values())
rows, columns = [], []
for n in range(10):
    row_n, column_n = [], []
    for sqr in sqrs_list:
        # Sorting the squares into rows and columns
        if sqr.num % 10 == n:
            column_n.append(sqr)
        if sqr.num // 10 == n:
            row_n.append(sqr)

    rows.append(row_n)
    columns.append(column_n)

score = 0
score_str = score_font.render('Score :', 1, red)
screen.blit(score_str, (20, 30))
show_score()
drag = False

# Main game loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            block_picked = block_choice((x, y), active_blocks)
            if block_picked is not None:
                block_x, block_y = block_picked.start
                x_offset = x - block_x
                y_offset = y - block_y
                drag = True

        elif event.type == pygame.MOUSEMOTION and drag is True:
            x, y = pygame.mouse.get_pos()
            if block_choice((x, y), active_blocks) != block_picked:
                draw_active_blocks(block_picked.num)
            block_picked.erase()
            block_picked.start = (x - x_offset, y - y_offset)
            block_picked.update_coords(pattern=block_picked.pattern)
            block_picked.draw_block()
            screen.blit(board, start_pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if block_picked is not None:
                try:
                    sqrs = sqrs_choice(block_picked)
                    if sum(sqr.occ for sqr in sqrs) == 0:
                        stick_block(block_picked, sqrs)
                        score += block_picked.value
                        hit()
                        show_score()
                        drag = False
                    else:
                        return_block(block_picked)
                except KeyError:
                    return_block(block_picked)
            if len(active_blocks) == 0:
                turn()
            if loss() is True:
                game_over()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_0:
                print(loss(), can_fit(block_picked), len(active_blocks))
        for button in buttons:
            button.click(event)
            
    clock.tick(FPS)

pygame.QUIT
sys.exit()