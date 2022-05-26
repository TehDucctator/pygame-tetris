import pygame
from tetrominoes import *

board = [["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""],
         ["","","","","","","","","",""]]

# for row in board:
#   print(row)

# screen
pygame.init()

def draw_grid():
    screen.fill(GREY)
    # grid
    pygame.draw.rect(screen, BLACK, [30, 30, 300, 600])

    for i in range(11): # vertical lines
        offset = i * 30
        pygame.draw.line(screen, GREY, (30+offset, 30), (30+offset, 630))

    for i in range(21):
        offset = i * 30
        pygame.draw.line(screen, GREY, (30, 30+offset), (330, 30+offset))


SCRN_W, SCRN_H = 390, 660
screen = pygame.display.set_mode((SCRN_W, SCRN_H))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

draw_grid()

pygame.display.flip()

pygame.display.set_caption('Pygame Tetris')

q = []

def draw(tetromino: str, x=120, y=30, rotation=0):
  piece = eval(tetromino)
  color = piece_colors[tetromino]
  origin_x, origin_y = x, y

  for row in piece[rotation]:
    for c in row:
      if c == 'X':
        pygame.draw.rect(screen, color, [x+1, y+1, 29, 29])
      
      x += 30
    x = origin_x
    y += 30

  pygame.display.flip()

class current_piece:
  def __init__(self, shape, x=120, y=30, rotation=0):
    self.shape = shape
    self.x = x
    self.y = y
    self.rotation = rotation
  

def main():
    q.extend(generate_bag())
    current = current_piece(q[0])
    draw(current.shape, current.x, current.y, current.rotation)

    running = True
    while running: # main game loop
        if len(q) <= 7:
          q.extend(generate_bag())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    draw_grid()
                    current.x += 30
                    draw(current.shape, current.x, current.y, current.rotation)
                elif event.key == pygame.K_DOWN:
                    draw_grid()
                    current.y += 30
                    draw(current.shape, current.x, current.y, current.rotation)
                elif event.key == pygame.K_LEFT:
                    draw_grid()
                    current.x -= 30
                    draw(current.shape, current.x, current.y, current.rotation)
                elif event.key == pygame.K_UP:
                    draw_grid()
                    current.rotation += 1 if current.rotation < 3 else -3
                    draw(current.shape, current.x, current.y, current.rotation)
                elif event.key == pygame.K_SPACE:
                    draw_grid()
                    q.pop(0)
                    current = current_piece(q[0])
                    draw(current.shape, current.x, current.y, current.rotation)
                elif event.key == pygame.K_z:
                    draw_grid()
                    current.rotation -= 1 if current.rotation > 0 else -3
                    draw(current.shape, current.x, current.y, current.rotation)
                elif event.key == pygame.K_c:
                    draw_grid()

if __name__ == "__main__":
  main()