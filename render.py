import pygame
import tetrominoes

pygame.display.init()
pygame.font.init()

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)

# writes text
def write_text(text: str, size: int, x: int, y: int, color: tuple, screen):
    font = pygame.font.Font('freesansbold.ttf', size)
    rendered = font.render(text, True, color)
    tRect = rendered.get_rect()
    tRect.center = (x, y)
    screen.blit(rendered, tRect)


# draws playfield, hold, queue, and placed tetrominoes
def draw_grid(screen, board, hold, q, level, lines):
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
    write_text(f"LEVEL: {level}", 15, 150, 660, BLACK, screen)

    # lines cleared text
    write_text(f"LINES: {lines}", 15, 270, 660, BLACK, screen)

    # next up text
    write_text("NEXT:", 15, 390, 30, BLACK, screen)

    # show next 5 pieces
    pygame.draw.rect(screen, BLACK, [370, 45, 40, 175])
    next_piece_y = 50
    for shape in q[1:6]:
        first_piece = pygame.image.load("Tetromino Images/" + shape + ".png")
        screen.blit(first_piece, [378, next_piece_y])
        next_piece_y += 35

    # hold text
    write_text("HOLD:", 15, 31, 30, BLACK, screen)
    
    # show held piece
    pygame.draw.rect(screen, BLACK, [10, 45, 40, 30])
    if hold != "":
        held = pygame.image.load("Tetromino Images/" + hold + ".png")
        screen.blit(held, [18, 48])

    pygame.display.flip()


# draws tetromino and outline
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


# writes lost text
def write_lose_text(screen):
    text = "You Lose! Press space to play again"
    x = 210
    y = 345

    # outline
    write_text(text, 17, x-1, y+1, BLACK, screen)
    write_text(text, 17, x+1, y+1, BLACK, screen)
    write_text(text, 17, x-1, y-1, BLACK, screen)
    write_text(text, 17, x+1, y-1, BLACK, screen)
    
    # lost text
    write_text(text, 17, x, y, RED, screen)
