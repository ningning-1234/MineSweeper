from random import randint

import pygame
from settings import *

#images
cover_img = pygame.image.load('assets/cover.png')
pressed_img = pygame.image.load('assets/cover_pressed.png')
flag_img1 = pygame.image.load('assets/flag1.png')
flag_img2 = pygame.image.load('assets/flag2.png')
mine_img = pygame.image.load('assets/mine.png')

#numbers
pygame.font.init()
adj_mines_font = pygame.font.Font('freesansbold.ttf', 40)
adj_mines_text = []
for i in range(1, 9):
    adj_mines_text.append(adj_mines_font.render(str(i), False, (0, 0, 0)))


draw_cover = False

class MSGame:
    def __init__(self):
        self.tile_grp = pygame.sprite.Group()
        self.grid_surface = pygame.Surface((TILE_SIZE*GRID_WIDTH, TILE_SIZE*GRID_HEIGHT))
        self.grid_pos = (0, UI_HEIGHT)
        self.tile_lst = []
        self.total_mines = 0
        self.flag_count = 0

        self.set_up_grid()

        # self.generate()

    def set_up_grid(self):
        for tiles_x in range(GRID_WIDTH):
            self.tile_lst.append([])
            for tiles_y in range(GRID_HEIGHT):
                t=Tile(self, (tiles_x, tiles_y))
                self.tile_lst[tiles_x].append(t)
                self.tile_grp.add(t)

    def generate(self, click_pos = (0,0)):
        self.total_mines = 0
        for tiles in range(0, round(GRID_WIDTH * GRID_HEIGHT /4)):
            x_pos = randint(0, GRID_WIDTH - 1)
            y_pos = randint(0, GRID_WIDTH - 1)
            try_count = 20
            while(self.tile_lst[x_pos][y_pos].mine == True and try_count>0):
                x_pos = randint(0, GRID_WIDTH-1)
                y_pos = randint(0, GRID_WIDTH-1)
                try_count -= 1
            if(try_count>0):
                #generate mine
                mine_tile = self.tile_lst[x_pos][y_pos]
                mine_tile.mine = True
                self.total_mines += 1
                adj = mine_tile.get_adj_tiles()
                for t in adj:
                    t.adj_mines += 1
            print(self.total_mines)

    def update(self, events):
        self.tile_grp.update(events)
        for event in events:
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_d):
                    global draw_cover
                    if(draw_cover==True):
                        draw_cover = False
                    else:
                        draw_cover = True

    def draw(self, surface):
        self.tile_grp.draw(self.grid_surface)
        surface.blit(self.grid_surface, self.grid_pos)
        flag_counter = pygame.font.Font('freesansbold.ttf', 50)
        text = flag_counter.render(str(self.total_mines - self.flag_count), False, (0, 0, 0))
        surface.blit(text, (0, 0))

# control everything game related

class Tile(pygame.sprite.Sprite):
    def __init__(self, game, grid_pos, color = (250,75,75)):
        super().__init__()
        self.game = game
        self.image = pygame.Surface([TILE_SIZE, TILE_SIZE])
        self.rect = self.image.get_rect()
        # self.rect.x = 0
        # self.rect.y = 0
        self.grid_pos = grid_pos
        self.rect.x = grid_pos[0]*TILE_SIZE
        self.rect.y = grid_pos[1]*TILE_SIZE
        self.color = color
        self.cover = True
        self.flagged = False
        self.mine = False
        self.adj_mines = 0

    def get_adj_tiles(self):
        tile_lst = []
        for y in range(self.grid_pos[1] - 1, self.grid_pos[1] + 2, 1):
            for x in range(self.grid_pos[0] - 1, self.grid_pos[0] + 2, 1):
                if (y >= 0 and x >= 0 and y<GRID_HEIGHT and x<GRID_WIDTH):
                    tile_lst.append(self.game.tile_lst[x][y])
        return tile_lst

    def uncover(self):
        if(self.flagged):
            return
        self.cover = False
        if(self.mine):
            print('Gameover')
        elif(self.adj_mines == 0):
            for tile in range(0, len(self.get_adj_tiles())):
                if(self.get_adj_tiles()[tile].cover == True):
                    self.get_adj_tiles()[tile].uncover()

    def force_uncover(self):
        if(self.cover):
            self.uncover()
            return
        if(self.adj_mines != 0):
            adj_flags = 0
            for tile in range(0, len(self.get_adj_tiles())):
                if(self.get_adj_tiles()[tile].flagged == True):
                    adj_flags += 1
            print(adj_flags)
            if(self.adj_mines == adj_flags):
                print('test2')
                for tile in range(0, len(self.get_adj_tiles())):
                    if (self.get_adj_tiles()[tile].cover == True):
                        self.get_adj_tiles()[tile].uncover()
        # check that there are at least one adj mine
        # check that the right amount of adjacent tiles have been flagged



    def flag(self):
        if(self.flagged==False):
            self.flagged = True
            self.game.flag_count += 1
        else:
            self.flagged = False
            self.game.flag_count -= 1

    def update(self, events):
        mouse_pos = pygame.mouse.get_pos()
        mx = mouse_pos[0] - self.game.grid_pos[0]
        my = mouse_pos[1] - self.game.grid_pos[1]
        if (self.rect.collidepoint((mx, my))):
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if(event.button==1):
                        self.uncover()
                    if(event.button==3 and self.cover==True):
                        self.flag()
                    if(event.button==2):
                        self.force_uncover()
        self.draw()

        # print('tile update')

    def draw(self):
        mouse_pos = pygame.mouse.get_pos()
        mx = mouse_pos[0] - self.game.grid_pos[0]
        my = mouse_pos[1] - self.game.grid_pos[1]
        self.image.fill(self.color)
        if (self.mine):
            self.image.blit(mine_img, (0, 0))
        elif(self.adj_mines != 0):
            self.image.blit(adj_mines_text[self.adj_mines-1], (0, 0))
        if (self.cover and draw_cover):
            self.image.blit(cover_img, (0, 0))
        if (self.flagged and draw_cover):
            self.image.blit(flag_img1, (0, 0))
        if (self.rect.collidepoint((mx, my))):
            pygame.draw.rect(self.image, (200, 200, 200), (0, 0, TILE_SIZE, TILE_SIZE), 3)
        else:
            pygame.draw.rect(self.image, (0, 0, 0), (0, 0, TILE_SIZE, TILE_SIZE), 1)
