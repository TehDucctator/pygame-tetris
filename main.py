import pygame
from tetrominoes import *

board = [[""]*10 for _ in range(24)]

# pygame set up
pygame.init()

SCRN_W, SCRN_H = 420, 690
screen = pygame.display.set_mode((SCRN_W, SCRN_H))

pygame.display.set_caption('Pygame Tetris')

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

screen.fill(WHITE)

pygame.display.flip()

q = []

def draw_grid(hold):
    font = pygame.font.Font('freesansbold.ttf', 15)
    screen.fill(GREY)
    
    # grid
    pygame.draw.rect(screen, BLACK, [60, 30, 300, 600])

    for i in range(11): # vertical lines
        offset = i * 30
        pygame.draw.line(screen, GREY, (60+offset, 30), (60+offset, 630))

    for i in range(21): # horizontal lines
        offset = i * 30
        pygame.draw.line(screen, GREY, (60, 30+offset), (390, 30+offset))

    # draw placed pieces
    y = 30
    for row in board[4:]:
        x = 60
        for spot in row:
            if spot != '':
                pygame.draw.rect(screen, piece_colors[spot], [x+1, y+1, 29, 29])
            x += 30

        y += 30

    # next up text
    next_text = font.render("NEXT:", True, (0, 0, 0))
    tRect = next_text.get_rect()
    tRect.center = (390, 30)
    screen.blit(next_text, tRect)
    
    # show next pieces
    pygame.draw.rect(screen, BLACK, [370, 45, 40, 175])
    next_piece_y = 50
    for shape in q[1:6]:
        first_piece = pygame.image.load("Tetromino Images/" + shape + ".png")
        screen.blit(first_piece, [378, next_piece_y])
        next_piece_y += 35

    # hold text
    hold_text = font.render("HOLD:", True, (0, 0, 0))
    tRect = hold_text.get_rect()
    tRect.center = (31, 30)
    screen.blit(hold_text, tRect)
    
    # show held piece
    pygame.draw.rect(screen, BLACK, [10, 45, 40, 30])
    if hold != "":
        held = pygame.image.load("Tetromino Images/" + hold + ".png")
        screen.blit(held, [18, 48])

    pygame.display.flip()

def draw(tetromino: str, x=120, y=30, rotation=0):
    piece = eval(tetromino)
    color = piece_colors[tetromino]

    x_spawn = x # initial line where each box is drawn relative to
    outline_coords = [] # used for coords for outline of where piece will land

    for row in piece[rotation]:
        for c in row: # goes through list to draw shape one box at a time
            if c == 'X':
                pygame.draw.rect(screen, color, [x+1, y+1, 29, 29]) # boxes of tetromino
                outline_coords.append([(x-60)//30, (y-30)//30+4]) # adds coords of each box
            
            x += 30

        # resets drawing "cursor" on next row
        x = x_spawn 
        y += 30

    # outline
    can_go_down = True
    while can_go_down: # moves outline coords down as much as possible
        for coord in outline_coords: # checks if can move down 1
            if coord[1]+1 > 23: # bottom of board
                can_go_down = False
                break
                
            elif board[coord[1]+1][coord[0]] != "": # another piece
                can_go_down = False
                break

        if can_go_down: # moves down one if can move down
            for coord in outline_coords:
                coord[1] += 1

    for coord in outline_coords: # draws outline
        outline_x = coord[0] * 30 + 60
        outline_y = (coord[1]-3) * 30

        pygame.draw.rect(screen, color, [outline_x+1, outline_y+1, 29, 29], 1)
    
    pygame.display.flip()

class current_piece:
    def __init__(self, shape: str, x=150, y=30, rotation=0):
        self.shape = shape
        self.x = x
        self.y = y
        self.rotation = rotation
        self.coords = []

    # updates grid coords of each box in the tetromino
    def get_coords(self):
        piece = eval(self.shape)

        temp_x = self.x
        temp_y = self.y
        
        x_spawn = self.x
    
        for row in piece[self.rotation]:
            for c in row:
                if c == 'X': # turns pygame screen coords into grid coords
                    new_x = int((temp_x-60)/30) 
                    new_y = int((temp_y-30)/30)
                    self.coords.append((new_x, new_y+4)) # top left is (0, 4)
                    if len(self.coords) > 4:
                        self.coords.pop(0)
                
                temp_x += 30
                
            temp_x = x_spawn
            temp_y += 30

    # returns if piece can move in a certain direction
    def move_check(self, x_change: int, y_change: int):
        self.get_coords()
        
        can_move = True
        for coord in self.coords:
            new_x = coord[0]+x_change # horizontal
            if new_x < 0 or new_x > 9: # checks for left and right wall
                can_move = False

            elif board[coord[1]][new_x] != "": # checks for piece
                can_move = False

            # vertical
            new_y = coord[1] + y_change

            if new_y > 23: # checks for bottom
                can_move = False

            elif board[new_y][coord[0]] != "": # checks for piece
                can_move = False

        return can_move

    # updates board to place piece
    def place(self):
        for coord in self.coords:
            board[coord[1]][coord[0]] = self.shape

    # rotation system (wall kicks)
    def SRS(self, direction):
        wall_kick_tests = [[[(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)], # 0 to 1 (r)
                            [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)]], # 0 to 3 (l)
                            
                            [[(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)], # 1 to 2
                            [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)]], # 1 to 0
                            
                            [[(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)], # 2 to 3
                            [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1,2)]], # 2 to 1
                            
                            [[(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)], # 3 to 0
                            [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]]] # 3 to 2

        I_wall_kick_tests = [[[(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)], # 0 to 1 (r)
                            [(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)]], # 0 to 3 (l)
                            
                            [[(0, 0), (-1, 0), (2, 0), (-1, -2), (2, 1)], # 1 to 2
                            [(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)]], # 1 to 0
                            
                            [[(0, 0), (2, 0), (-1, 0), (2, -1), (-1, 2)], # 2 to 3
                            [(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)]], # 2 to 1
                            
                            [[(0, 0), (1, 0), (-2, 0), (1, 2), (-2, -1)], # 3 to 0
                            [(0, 0), (-2, 0), (1, 0), (-2, 1), (1, -2)]]] # 3 to 2

        def test(start_rotation, shape_name):
            self.get_coords() # get orientation for placement

            if shape_name != "I" or shape_name != "O": # choose between 2 wall kick tests
                kick_tests = wall_kick_tests
            else:
                kick_tests = I_wall_kick_tests
            
            for test in kick_tests[start_rotation][direction]:
                acceptable = True # stores if a rotation test fits
                new_coords = [] # store where new coords will be
                
                for coord in self.coords:
                    new_x = coord[0] + test[0] # changes coords according to test data
                    new_y = coord[1] + test[1]

                    new_coords.append((new_x, new_y)) # stores new coords

                for n_coord in new_coords: # checks if coords are valid
                    if n_coord[0] < 0 or n_coord[0] > 9: # past left + right walls
                        acceptable = False
                        break

                    elif n_coord[1] > 23: # below bottom
                        acceptable = False
                        break
                        
                    elif board[n_coord[1]][n_coord[0]] != "": # in placed piece
                        acceptable = False
                        break

                if acceptable: # updates to the one that fits
                    self.x += test[0]*30
                    self.y += test[1]*30
                    self.get_coords()
                    break

            else: # if no suitable spot found, undo rotation 
                self.rotation = start_rotation

            
        if direction == 0: # rotate right
            start_rotation = self.rotation
            self.rotation += 1 if self.rotation < 3 else -3
            test(start_rotation, self.shape)
            
        else: # rotate left
            start_rotation = self.rotation
            self.rotation -= 1 if self.rotation >= 1 else -3
            test(start_rotation, self.shape)
  
# clears full lines in board
def clear_lines():
    for i, line in enumerate(board):
        if not "" in line:
            board.pop(i)
            board.insert(0, [""]*10)

# main game function
def main():
    # draw_grid(hold)
    q.extend(generate_bag())
    current = current_piece(q[0])
    draw(current.shape, current.x, current.y, current.rotation)

    pygame.key.set_repeat(200, 30)

    hold = ""
    used_hold_flag = False

    frame = 0
    running = True
    while running: # main game loop
        if len(q) <= 7:
          q.extend(generate_bag())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.KEYDOWN:
                # move right
                if event.key == pygame.K_RIGHT:
                    if current.move_check(1, 0):
                        draw_grid(hold)
                        current.x += 30
                        draw(current.shape, current.x, current.y, current.rotation)

                # soft drop
                if event.key == pygame.K_DOWN:
                    if current.move_check(0, 1):
                        draw_grid(hold)
                        current.y += 30
                        draw(current.shape, current.x, current.y, current.rotation)

                # move left
                if event.key == pygame.K_LEFT:
                    if current.move_check(-1, 0):
                        draw_grid(hold)
                        current.x -= 30
                        draw(current.shape, current.x, current.y, current.rotation)

                # rotate right
                if event.key == pygame.K_UP:
                    current.SRS(0)
                    draw_grid(hold)
                    draw(current.shape, current.x, current.y, current.rotation)

                # hard drop
                if event.key == pygame.K_SPACE:
                    used_hold_flag = False
                    while current.move_check(0, 1):
                        current.y += 30

                    current.place()
                    q.pop(0)
                    current = current_piece(q[0], 150, 30)
                    
                    clear_lines()
                    draw_grid(hold)
                    draw(current.shape, current.x, current.y, current.rotation)

                # rotate left
                if event.key == pygame.K_z:
                    current.SRS(-1)
                    draw_grid(hold)
                    draw(current.shape, current.x, current.y, current.rotation)

                # hold
                if event.key == pygame.K_c:
                    if not used_hold_flag:
                        used_hold_flag = True
                        if hold == "":
                            hold = q.pop(0)
                        else:
                            q.insert(0, hold)
                            hold = q.pop(1)
                        
                        draw_grid(hold)
                        current = current_piece(q[0], 150, 30)
                        draw(current.shape, current.x, current.y, current.rotation)

        # gravity
        if frame % 30 == 0:
            if current.move_check(0, 1): 
                draw_grid(hold)
                current.y += 30
                draw(current.shape, current.x, current.y, current.rotation)
                ground_time = 0
                
            elif ground_time == 3: # place from gravity
                used_hold_flag = False
                current.place()
                q.pop(0)
                current = current_piece(q[0], 150, 30)
                ground_time = 0
                
                clear_lines()
                draw_grid(hold)
                draw(current.shape, current.x, current.y, current.rotation)
                
            else: # delay before placing from gravity
                ground_time += 1

        # update frame var
        frame += 1 
        clock.tick(60)

if __name__ == "__main__":
  main()