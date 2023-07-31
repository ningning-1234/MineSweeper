import pygame
from settings import *

cover_img = pygame.image.load('assets/cover.png')

class MSGame:
    def __init__(self):
        self.tile_grp = pygame.sprite.Group()
        self.grid_surface = pygame.Surface((TILE_SIZE*GRID_WIDTH, TILE_SIZE*GRID_HEIGHT))
        self.grid_pos = (0, 0)
        tile_lst = []
        for tiles_x in range(GRID_WIDTH):
            tile_lst.append([])
            for tiles_y in range(GRID_HEIGHT):
                t=Tile(self, (tiles_x, tiles_y))
                tile_lst[tiles_x].append(t)
                self.tile_grp.add(t)

    def update(self):
        self.tile_grp.update()

    def draw(self, surface):
        self.tile_grp.draw(self.grid_surface)
        surface.blit(self.grid_surface, self.grid_pos)

# control everything game related

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, grid_pos, color = (250,75,75)):
        super().__init__()
        self.game = game
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.rect = self.image.get_rect()
        # self.rect.x = 0
        # self.rect.y = 0
        self.rect.x = grid_pos[0]*TILE_SIZE
        self.rect.y = grid_pos[1]*TILE_SIZE
        self.color = color

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mx = mouse_pos[0] - self.game.grid_pos[0]
        my = mouse_pos[1] - self.game.grid_pos[1]
        self.image.fill(self.color)
        self.image.blit(cover_img, (0, 0))
        if(self.rect.collidepoint((mx,my))):
            pygame.draw.rect(self.image, (200, 200, 200), (0, 0, TILE_SIZE, TILE_SIZE), 3)
        else:
            pygame.draw.rect(self.image, (0, 0, 0), (0, 0, TILE_SIZE, TILE_SIZE), 1)

        # print('tile update')


