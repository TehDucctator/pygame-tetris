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
    screen.fill(WHITE)
    # grid
    pygame.draw.rect(screen, BLACK, [30, 30, 300, 600])

    for i in range(9): # vertical lines
        offset = i * 30
        pygame.draw.line(screen, GREY, (60+offset, 30), (60+offset, 630))

    for i in range(19):
        offset = i * 30
        pygame.draw.line(screen, GREY, (30, 60+offset), (330, 60+offset))


SCRN_W, SCRN_H = 390, 660
screen = pygame.display.set_mode((SCRN_W, SCRN_H))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)

draw_grid()

pygame.display.flip()

pygame.display.set_caption('Pygame Tetris')


def main():
    running = True
    while running: # main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 

if __name__ == "__main__":
  main()