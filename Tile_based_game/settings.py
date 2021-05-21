import pygame as pg
import random as r
import math
from os import path


# Game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
FONT_NAME = 'arial'
TITLE = "Mega Maze Game"


#colors (r,g,b)
BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHT_GRAY = (128, 128, 128)
DARK_GRAY = (40, 40, 40)
BROWN = (139, 69, 19)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
PURPLE = (153,0,153)
ORANGE = (255,155,0)
PINK = (255,51,153)

BGCOLOR = BROWN

TILESIZE = 50
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tileGreen_39.png'

# Player settings
PLAYER_SPEED = 250
PLAYER_ROT_SPEED = 250
PLAYER_IMG = 'survivor1_stand.png'
PLAYER_WALK = 'survivor1_hold.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)

# Coin settings
TOKEN_IMG = 'coin 2_0.png'
TOTAL_LEVELS = 3