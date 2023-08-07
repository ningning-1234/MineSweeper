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
#  generate mines after first click
#  reveal empty patch at once
#  add game over

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
