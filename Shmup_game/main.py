
########################## Attribution ################################
# tutorial found at kids can code.org and Eric Broadbent
#Code created by: Danson Coats
#Art created by: www.kenny.nl
################## End Attribution ####################################



import pygame as pg
import random as r
from os import *


#explosions class
class Explosion(pg.sprite.Sprite):

    def __init__(self, center, size):
        super(Explosion, self).__init__()
        self.size = size
        self.image = exp_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1
            if self.frame == len(exp_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = exp_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


class NPC(pg.sprite.Sprite):
    def __init__(self):
        super(NPC, self).__init__()
        #pg.sprite.Sprite.__init__(self) does the same as above
        # self.image = pg.Surface((15,15))
        # self.image.fill(RED)
        self.image_orig = r.choice(meteor_imgs)

        #self.image_orig = pg.transform.scale(self.image_orig, (75, 75))
        self.image = self.image_orig.copy()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = self.rect.width *.75 /2
        if debug:
            pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.x = r.randint(80, WIDTH-80)
        self.rect.bottom = 0
        self.rect.centerx = self.x
        self.rx = r.randint(-10,10)
        self.ry = r.randint(1,10)
        self.speedx = self.rx
        self.speedy = self.ry
        self.center_x = self.rect.centerx
        self.center_y = self.rect.centery
        self.rot = 0
        self.rot_speed = r.randint(-8,8)
        self.last_update = pg.time.get_ticks()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 60:
            self.last_update = now
            #rotate sprite
            self.rot = (self.rot + self.rot_speed)%360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center



    def update(self):
        self.rotate()
        #screen wrapping
        # if self.rect.left > WIDTH:
        #     self.kill()
        #     spawn_npc()
        # if self.rect.right < 0:
        #     self.kill()
        #     spawn_npc()
        if self.rect.top > HEIGHT:
            self.kill()
            spawn_npc()

#constant movement
        self.rect.x += self.speedx
        self.rect.y += self.speedy
 # Wall Bouncing
 #        if self.rect.right >= WIDTH:
 #            self.speedx *= -1
 #        if self.rect.left < 0:
 #            self.speedx *= -1




class Player(pg.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.shield = 100
        self.fuel = 100
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        #pg.sprite.Sprite.__init__(self) does the same as above
        # self.image = pg.Surface((50,40))
        # self.image.fill(BLACK)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * .75 / 2
        if debug:
            pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.bottom = HEIGHT - 5
        self.rect.centerx = WIDTH / 2
        #self.rect.bottomright =(0,0)
        self.speedx = 0
        self.speedy = 0
        self.keypressed = False
        self.shoot_delay = 250
        self.last_shot = pg.time.get_ticks()

    def shoot(self):
        now = pg.time.get_ticks()
        if (now - self.last_shot) > self.shoot_delay:
            self.last_shot = now
            b = Bullet(self.rect.centerx, self.rect.top-1)
            all_Sprites.add(b)
            bullet_group.add(b)



    def toggle_pressed(self):
        self.keypressed = False

    def hide(self):
        # hides player temporarily
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT +500)

    def update(self):
        #unhide if hidden
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
         #basic flow movment
        self.speedx = 0
        self.speedy = 0
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.speedx += -8
            self.fuel-=.05
        if keystate[pg.K_RIGHT]:
            self.rect.x += 8
            self.fuel-=.05
        if keystate[pg.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx
        self.rect.y += self.speedy


        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT

class Bullet(pg.sprite.Sprite):
    def __init__(self,x,y):
        super(Bullet,self).__init__()
        # self.image = pg.Surface((5,10))
        # self.image.fill(YELLOW)
        self.image = lazer_img
        self.image.set_colorkey(BLACK)
        self.image = pg.transform.scale(self.image, (10, 40))
        self.rect = self.image.get_rect()
        self.radius = self.rect.width * .75 / 2
        if debug:
            pg.draw.circle(self.image, BLUE, self.rect.center, self.radius)
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y+=self.speedy
        #kill bullet when rect.bottom <=0
        if self.rect.bottom < 0:
            self.kill()
            print("kill")

WIDTH = 360
HEIGHT = 480
FPS = 30
title = "Template"

#colors (r,g,b)
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
PURPLE = (153,0,153)
ORANGE = (255,155,0)
PINK = (255,51,153)

font_name = pg.font.match_font('arial') #move to constants

mouse_bttn_held = False
debug = False

######################################
#folder variables
######################################
game_folder = path.dirname(__file__)
imgs_folder = path.join(game_folder, "imgs")
sounds_folder = path.join(game_folder, "sounds")
scores_folder = path.join(game_folder, "scores")
background_folder = path.join(imgs_folder, "backgrounds")
enemy_imgs_folder = path.join(imgs_folder, "enemy_imgs")
player_imgs_folder = path.join(imgs_folder, "player_imgs")
animation_folder = path.join(imgs_folder, "animations")


######################################
#game Functions
######################################
def spawn_npc():
    newNpc = NPC()
    newNpc.speedx = r.randint(-10, 10)
    newNpc.speedy = r.randint(1, 10)
    npc_group.add(newNpc)
    all_Sprites.add(newNpc)

def draw_text(surf,text,size,x,y,color):
    font = pg.font.Font(font_name, size)
    text_surf = font.render(text, True, color)
    text_rect = text_surf.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surf, text_rect)

def draw_bar(surf,x,y,pct,color):
    if pct < 0:
        pct = 0
    bar_len = 100
    bar_height = 40
    fill = (pct/100)*bar_len
    outline = pg.Rect(x, y, bar_len, bar_height)
    fillrect = pg.Rect(x, y, fill, bar_height)
    pg.draw.rect(surf, color, fillrect)
    pg.draw.rect(surf, WHITE, outline, 3)




pg.init()
pg.mixer.init()

screen=pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption(title)
clock = pg.time.Clock()

########################################
#load in images
########################################
background = pg.image.load(path.join(background_folder, "space.png")).convert()
background = pg.transform.scale(background,(WIDTH, HEIGHT))
background_rect = background.get_rect()
npc_img = pg.image.load(path.join(enemy_imgs_folder, "rock.png")).convert()
player_img = pg.image.load(path.join(player_imgs_folder, "ship.png")).convert()
lazer_img = pg.image.load(path.join(player_imgs_folder, "lazer.png")).convert()
meteor_imgs = []
meteor_list = ["meteorBrown_big1.png","meteorBrown_big2.png", "meteorBrown_big3.png",
               "meteorBrown_med3.png", "meteorBrown_small1.png", "meteorBrown_small2.png"]
for img in meteor_list:
    meteor_imgs.append(pg.image.load(path.join(enemy_imgs_folder,img)))

exp_anim = {}
exp_anim["lg"] = []
exp_anim["sm"] = []
for i in range(9):
    filename = "regularExplosion0{}.png".format(i)
    img=pg.image.load(path.join(animation_folder,filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pg.transform.scale(img,(100,100))
    exp_anim["lg"].append(img_lg)
    img_sm = pg.transform.scale(img, (50, 50))
    exp_anim["sm"].append(img_sm)



############################################
#load sounds
############################################
shoot_sound = pg.mixer.Sound(path.join(sounds_folder,"pew.wav"))
expl_snds = []
for snd in ["expl3.wav", "expl6.wav"]:
    expl_snds.append(pg.mixer.Sound(path.join(sounds_folder, snd)))

pg.mixer.music.load(path.join(sounds_folder,"tgfcoder-FrozenJam-SeamlessLoop.ogg"))


#create sprite groups
all_Sprites = pg.sprite.Group()
players_group = pg.sprite.Group()
npc_group = pg.sprite.Group()
bullet_group = pg.sprite.Group()

#creates game objects
player = Player()
for i in range(50):
    spawn_npc()



#add object to sprite groups
players_group.add(player)
all_Sprites.add(player)

score = 0



#Game Loop
running = True
while running:
    clock.tick(FPS)
    # process input
    #getting a list of events

    for event in pg.event.get():
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                player.toggle_pressed()
            if event.key == pg.K_UP or event.key == pg.K_DOWN:
                player.toggle_pressed()

        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key ==pg.K_ESCAPE:
                running = False
            #player shoot
            # if event.key ==pg.K_SPACE:
            #     player.shoot()
            if event.key == pg.K_F12:
                debug = True

    #make updates
    all_Sprites.update()
    #checking for hit between player and npc
    hits = pg.sprite.spritecollide(player, npc_group, True, pg.sprite.collide_circle)
    if hits:
        exp = Explosion(hits[0].rect.center, "sm")
        all_Sprites.add(exp)
        r.choice(expl_snds).play()
        spawn_npc()
        player.shield-=hits[0].radius*2
        print(player.shield)
        if player.shield <= 0:
            exp = Explosion(player.rect.center, "lg")
            all_Sprites.add(exp)
            player.hide()
            player.lives -= 1
            player.shield = 100
            if player.lives == 0 and not exp.alive():
                running = False

        # running = False
    #bullet hits NPC
    hits = pg.sprite.groupcollide(npc_group, bullet_group, True, True, pg.sprite.collide_circle)
    for hit in hits:
        if hit.radius < 30:
            size = "sm"
        else:
            size = "lg"
        exp = Explosion(hit.rect.center, size)
        all_Sprites.add(exp)
        score += 50 - int(hit.radius)
        npc = NPC()
        npc_group.add(npc)
        all_Sprites.add(npc)


    #render (Draw)
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_Sprites.draw(screen)

    #draw HUD
    draw_text(screen,"Score: "+str(score),18, WIDTH/2, 15,WHITE)
    draw_bar(screen, 5, 15, player.shield, GREEN)
    draw_bar(screen, 5, 55, player.fuel, BLUE)




    #last thing we do in the loop
    pg.display.flip()



pg.quit()