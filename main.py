import pygame
import tetrominoes
from draw_screen import draw_grid, draw

board = [[""]*10 for _ in range(24)]

# pygame set up
pygame.init()

SCRN_W, SCRN_H = 420, 690
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

screen = pygame.display.set_mode((SCRN_W, SCRN_H))
pygame.display.set_caption('Pygame Tetris')

clock = pygame.time.Clock()

screen.fill(WHITE)

pygame.display.flip()

q = []

class current_piece:
    def __init__(self, shape: str, x=150, y=30, rotation=0):
        self.shape = shape
        self.x = x
        self.y = y
        self.rotation = rotation
        self.coords = []

    # updates grid coords of each box in the tetromino
    def get_coords(self):
        piece_states = "tetrominoes." + self.shape
        piece = eval(piece_states)

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

            pygame.draw.rect(screen, WHITE, [coord[0]*30+60, (coord[1]-4)*30+30, 29, 29])

        pygame.display.flip()
        pygame.time.delay(2)

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

            pygame.draw.rect(screen, WHITE, [60, 30+30*(i-4), 300, 30]) # white flash

    pygame.display.flip()
    pygame.time.delay(100)


# returns if piece can't be spawned after moving up twice
def check_lose(current):
    if not current.move_check(0,0): # moves up one if can't place
        current.y -= 30
    
        if not current.move_check(0,0): # moves up again if can't place
            current.y -= 30
      
            if not current.move_check(0,0): # lose if can't spawn after moving up twice
                return True
    
    return False


# main game function
def main():
    q.extend(tetrominoes.generate_bag())
    current = current_piece(q[0])
    draw(screen, board, current.shape, current.x, current.y, current.rotation)

    pygame.key.set_repeat(200, 30)

    hold = ""
    used_hold = False # tracks if used hold
    space_held = False # prevents holding space

    frame = 0
    running = True
    while running: # main game loop
        if len(q) <= 7:
          q.extend(tetrominoes.generate_bag())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.KEYDOWN:
                # move right
                if event.key == pygame.K_RIGHT:
                    if current.move_check(1, 0):
                        draw_grid(screen, board, hold, q)
                        current.x += 30
                        draw(screen, board, current.shape, current.x, current.y, current.rotation)

                # soft drop
                if event.key == pygame.K_DOWN:
                    if current.move_check(0, 1):
                        draw_grid(screen, board, hold, q)
                        current.y += 30
                        draw(screen, board, current.shape, current.x, current.y, current.rotation)

                # move left
                if event.key == pygame.K_LEFT:
                    if current.move_check(-1, 0):
                        draw_grid(screen, board, hold, q)
                        current.x -= 30
                        draw(screen, board, current.shape, current.x, current.y, current.rotation)

                # rotate right
                if event.key == pygame.K_UP:
                    current.SRS(0)
                    draw_grid(screen, board, hold, q)
                    draw(screen, board, current.shape, current.x, current.y, current.rotation)

                # hard drop
                if not space_held: # prevent holding space 
                    if event.key == pygame.K_SPACE:
                        used_hold = False
                        space_held = True

                        while current.move_check(0, 1):
                            current.y += 30

                        current.place()
                        q.pop(0)
                        current = current_piece(q[0], 150, 30)
                        if check_lose(current): # check if lost
                            running = False
                        
                        clear_lines()
                        draw_grid(screen, board, hold, q)
                        draw(screen, board, current.shape, current.x, current.y, current.rotation)

                # rotate left
                if event.key == pygame.K_z:
                    current.SRS(-1)
                    draw_grid(screen, board, hold, q)
                    draw(screen, board, current.shape, current.x, current.y, current.rotation)

                # hold
                if event.key == pygame.K_c:
                    if not used_hold:
                        used_hold = True
                        if hold == "":
                            hold = q.pop(0)
                        else:
                            q.insert(0, hold)
                            hold = q.pop(1)
                        
                        draw_grid(screen, board, hold, q)
                        current = current_piece(q[0], 150, 30)
                        draw(screen, board, current.shape, current.x, current.y, current.rotation)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_held = False # allows space to be pressed again after release

        # gravity
        if frame % 30 == 0:
            if current.move_check(0, 1): 
                draw_grid(screen, board, hold, q)
                current.y += 30
                draw(screen, board, current.shape, current.x, current.y, current.rotation)
                ground_time = 0
                
            elif ground_time == 2: # place from gravity
                used_hold = False

                current.place()
                q.pop(0)
                current = current_piece(q[0], 150, 30)
                ground_time = 0
                if check_lose(current): # check if lost
                    running = False
                
                clear_lines()
                draw_grid(screen, board, hold, q)
                draw(screen, board, current.shape, current.x, current.y, current.rotation)
                
            else: # delay before placing from gravity
                ground_time += 1

                # flash
                for coord in current.coords:
                    pygame.draw.rect(screen, WHITE, [coord[0]*30+61, (coord[1]-4)*30+31, 29, 29])
                
                pygame.display.flip()
                pygame.time.delay(15)

                for coord in current.coords:
                    pygame.draw.rect(screen, tetrominoes.piece_colors[current.shape], [coord[0]*30+61, (coord[1]-4)*30+31, 29, 29])

                pygame.display.flip()
                pygame.time.delay(15)


        # update frame var
        frame += 1 
        clock.tick(60)

if __name__ == "__main__":
  main()