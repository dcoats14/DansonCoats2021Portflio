import pygame as pg
import random as r
import math
from os import path
from settings import *
from sprites import *
from tilemap import *
import sys

class Game:
    def __init__(self):
        self.running = True
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.font_name = pg.font.match_font(FONT_NAME)
        pg.key.set_repeat(500, 100)
        self.score = 0

        self.level_num = 1


    def load_data(self):
        map = str.format("map{}.txt", self.level_num)
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'imgs')
        self.map = Map(path.join(game_folder, map))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.token = pg.image.load(path.join(img_folder, TOKEN_IMG)).convert_alpha()
        self.exit = pg.image.load(path.join(img_folder, 'castledoors.png')).convert_alpha()
        #self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()


    def new(self):
        self.total_coin_Count = 0
        self.coin_count = 0
        self.load_data()
        # Initialize al variables and do all setup for new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.token_group = pg.sprite.Group()
        self.exit_group = pg.sprite.Group()
        for row, tile in enumerate(self.map.data):
            for col, tile in enumerate(tile):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'C':
                    Token(self, col, row)
                    self.total_coin_Count += 1
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'E':
                    Exit(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

        self.run()

    def run(self):
        # Game loop - set self.playing = False to end game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GRAY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GRAY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        #self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        self.draw_text(str(self.coin_count)+"/"+str(self.total_coin_Count), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()


    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

        hits = pg.sprite.spritecollide(self.player, self.token_group, True)
        for hit in hits:
            self.add_score()
        hits = pg.sprite.spritecollide(self.player, self.exit_group, False)
        if hits and self.coin_count == self.total_coin_Count:
            self.new_level()

    def new_level(self):
        self.level_num += 1
        print(self.level_num)
        if self.level_num  > TOTAL_LEVELS:
            self.playing = False
            return
        else:
            self.new()


    def add_score(self):
        self.score += 100
        self.coin_count += 1
        print(self.coin_count, self.total_coin_Count)
        print(self.score)


    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE, 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Find all the coins and find the exit to win", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def show_go_screen(self):
        self.level_num = 1
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("You collected all the coins!",22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again", 22, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pg.display.flip()
        self.wait_for_key()

#create game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.show_go_screen()