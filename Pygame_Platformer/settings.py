import pygame as pg
import random as r
import math
from os import path

TITLE = "Fun Jump Game"

WIDTH = 500
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'
HS_FILE = "highscore.txt"
SPRITESHEET = "spritesheet_jumper.png"

# Player Properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.8
PLAYER_JUMP = 20

# Game Properties
BOOST_POWER = 60
POW_SPAWN_PCT = 7
MOB_FREQ = 5000
PLAYER_LAYER = 2
PLATFORM_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = 0

# Starting platforms
PLATFORM_LIST = [(0, HEIGHT - 60),
                 (WIDTH / 2 - 50, HEIGHT * 3 / 4 - 50),
                 (125, HEIGHT - 350),
                 (350, 200),
                 (175, 100)]
# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 128, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
TURQUOISE = (0, 206, 209)
PURPLE = (153, 0, 153)
ORANGE = (255, 155, 0)
PINK = (255, 51, 153)
BGCOLOR = TURQUOISE

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "imgs")
player_imgs = path.join(img_folder, "player_imgs")
sound_folder = path.join(game_folder, "sounds")
text_data = path.join(game_folder, "text_data")