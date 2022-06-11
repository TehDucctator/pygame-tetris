import pygame
import tetrominoes

pygame.display.init()
pygame.font.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)

def draw_grid(screen, board, hold, q, level, lines):
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
                pygame.draw.rect(screen, tetrominoes.piece_colors[spot], [x+1, y+1, 29, 29])
            x += 30

        y += 30

    # level text
    level_text = font.render(f"LEVEL: {level}", True, BLACK)
    tRect = level_text.get_rect()
    tRect.center = (150, 660)
    screen.blit(level_text, tRect)

    # lines cleared text
    line_text = font.render(F"LINES: {lines}", True, BLACK)
    tRect = line_text.get_rect()
    tRect.center = (270, 660)
    screen.blit(line_text, tRect)

    # next up text
    next_text = font.render("NEXT:", True, BLACK)
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
    hold_text = font.render("HOLD:", True, BLACK)
    tRect = hold_text.get_rect()
    tRect.center = (31, 30)
    screen.blit(hold_text, tRect)
    
    # show held piece
    pygame.draw.rect(screen, BLACK, [10, 45, 40, 30])
    if hold != "":
        held = pygame.image.load("Tetromino Images/" + hold + ".png")
        screen.blit(held, [18, 48])

    pygame.display.flip()


def draw(screen, board, tetromino: str, x=120, y=30, rotation=0):
    tetromino_arr = "tetrominoes." + tetromino

    piece = eval(tetromino_arr)
    color = tetrominoes.piece_colors[tetromino]

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