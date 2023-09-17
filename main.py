import pygame
from settings import *
from minesweeper import MSGame

run=True

pygame.init()
pygame.font.init()

window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

game = MSGame()

# todo
#  add game over
#  add second flag type:
#   prevents setting off mines but doesn't decrease mine count or force uncover
#  don't generate mines in corners

while (run):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False

    # t1.update()
    game.update(events)

    #_____Draw_____
    window.fill(BG_COLOR)
    # window.blit(t1.image, (0,0))
    game.draw(window)

    pygame.display.flip()
    clock.tick(FPS)
