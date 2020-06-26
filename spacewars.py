
import pygame
import time
import random
from os import path

#img_dir=path.join(path.dirname(__file__),'img')


WIDTH = 1000
HEIGHT = 800
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Wars!")
clock = pygame.time.Clock()


mob_shields=100



def draw_pshields():
    pygame.draw.rect(screen, WHITE, (10, 10, 200, 10), 2) #draw outline of pshield bar
    if player.player_shields<30:
        pygame.draw.rect(screen, YELLOW, (10, 10, player.player_shields * 2, 10), 0)  # draw fill of pshield bar
    else:
        pygame.draw.rect(screen, BLUE, (10, 10, player.player_shields*2, 10),0)  # draw fill of pshield bar
    myfont = pygame.font.SysFont("Linux Libertine O", 15)
    label = myfont.render("Player Shields", 1, (WHITE))
    screen.blit(label, (55, 25))

    pygame.draw.rect(screen, WHITE, (10, 40, 200, 10), 2)  # draw outline of total power bar
    pygame.draw.rect(screen, BLUE, (10, 40, player.total_power * 1.33, 10), 0) #draw fill of power bar
    myfont = pygame.font.SysFont("Linux Libertine O", 15)
    label = myfont.render("Total System Reserve", 1, (WHITE))
    screen.blit(label, (55, 55))

    if player.total_power<30:
        pygame.draw.rect(screen, WHITE, (10, 40, 200, 10), 2)  # draw outline of total power bar
        pygame.draw.rect(screen, RED, (10, 40, player.total_power * 1.33, 10), 0)  # draw fill of power bar
        myfont = pygame.font.SysFont("Linux Libertine O", 25)
        label = myfont.render("WARNING: Low reserve power - You will be unable to fire weapons if depleted!", 1, (YELLOW))
        screen.blit(label, (255, 55))


    pygame.draw.rect(screen, WHITE, (10, 70, 200, 10), 2)  # draw outline of heat bar
    pygame.draw.rect(screen, BLUE, (11, 71, player.heat*2, 9), 0)  # draw fill of heat bar


    myfont = pygame.font.SysFont("Linux Libertine O", 15)
    label = myfont.render("Core temperature", 1, (WHITE))
    screen.blit(label, (55, 85))
    if player.heat>80:
        pygame.draw.rect(screen, WHITE, (10, 70, 200, 10), 2)  # draw outline of heat bar
        pygame.draw.rect(screen, RED, (11, 71, player.heat * 2, 9), 0)  # draw fill of heat bar
        myfont = pygame.font.SysFont("Linux Libertine O", 25)
        label = myfont.render("WARNING: Core temperature critical - firing rate will be reduced", 1,(RED))
        screen.blit(label, (275, 75))


def draw_mshields():
    pygame.draw.rect(screen, WHITE, (790, 10, 200, 10), 2)  # draw outline of pshield bar
    if mob_shields<30:
        pygame.draw.rect(screen, YELLOW, (790, 10, mob_shields * 2, 10), 0)  # draw fill of pshield bar
    else:
        pygame.draw.rect(screen, RED, (790, 10, mob_shields * 2, 10), 0)
    myfont = pygame.font.SysFont("Linux Libertine O", 15)
    label = myfont.render("Invader Shields", 1, (WHITE))
    screen.blit(label, (850, 25))



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((15, 15))
        #self.image.fill(GREEN)

        self.angle = 0
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.original=self.image

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.rect.top=HEIGHT
        self.speedx = 0
        self.xthrust=0
        self.ythrust=0
        self.fuel=500
        self.rect.x=10
        self.rect.y=400
        self.last_facing='R'
        self.total_power=150
        self.player_shields=100
        self.facing='D'
        self.heat=0


    def update(self):

        self.speedx = 0
        up=False
        down=True
        left=False
        right=False
        if self.heat>0:
            self.heat-=0.1



        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] and self.fuel>0:
            self.xthrust -=0.02
            self.fuel-=0.02
            if self.facing!='L':
                self.angle=270
                self.facing = 'L'  # pphasers store last ship position to fire in the correct direction
        if keystate[pygame.K_RIGHT]and self.fuel>0:
            self.angle = 90
            self.xthrust +=0.02
            self.facing='R'
        if keystate[pygame.K_UP]and self.fuel>0:
            self.angle = 180
            self.ythrust-=0.02
            self.facing='U'
        if keystate[pygame.K_DOWN]and self.fuel>0:
            self.angle = 0
            self.ythrust+=0.02
            self.fuel -= 0.02
            self.facing='D'
        if keystate[pygame.K_s] and self.total_power>0 and self.player_shields<100 and self.heat<100:
            self.total_power-=1
            self.player_shields+=1

        if keystate[pygame.K_e] and self.player_shields>1 and self.total_power<150: #shields>1 so you don't destroy yourself by making shields=0
            self.total_power+=1
            self.player_shields-=1
          

        if self.rect.right > WIDTH: #if player goes off screen will reappear on other end
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = WIDTH
        if self.rect.top<0:
            self.rect.bottom=HEIGHT
        if self.rect.bottom>HEIGHT:
            self.rect.top=0 

        self.rect.x += self.xthrust #where player ship is drawn
        self.rect.y+=self.ythrust
        self.image = pygame.transform.rotate(player.original, self.angle)

    def shoot(self):
        if self.total_power>0 and self.heat<100:
            pphaser=Pphaser(self.rect.centerx,self.rect.top)
            all_sprites.add(pphaser)
            pphasers.add(pphaser)
            self.total_power-=1 #draws from system power when shoot
            self.heat+=5
            pygame.mixer.init()
            effect = pygame.mixer.Sound('playerfire.wav')
            effect.play()
            print(self.heat)



class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.angle = 0
        self.image = pygame.transform.scale(asteroid, (100, 100))
        self.original=self.image
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.y = random.randint(100,HEIGHT-10)
        self.rect.top=HEIGHT
        self.new_coord=0

    def update(self):
        self.angle+=0.1
        self.rect.x+=1
        self.rect.y=self.y+self.new_coord
        self.image = pygame.transform.rotate(asteroid.original, asteroid.angle)
        self.image.set_colorkey(WHITE)
        if self.rect.x>WIDTH:
            self.rect.x=0


class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.angle = 180
        self.image = pygame.transform.scale(enemy_img, (20, 20)) #resizes enemy ship
        self.original = self.image
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(400,800)   #random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randint(200,320)   #start enemy ship at random y position
        self.speedy = 0
        self.speedx = 0
        self.facing = 'D'
        self.angle=90
        self.image = pygame.transform.rotate(self.original, self.angle) #starting position facing player




    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.bottom > HEIGHT + 10: #if go off bottom of screen, reappear from top
            self.rect.bottom=10
        if self.rect.top<0: #if go off top of screen, reappear from bottom
           self.rect.top=HEIGHT-10
        if self.rect.left<0: #if go off left of screen, reappear from right
            self.rect.left=WIDTH-10
        if self.rect.right>WIDTH: #if go off right of screen, reappear from left
            self.rect.right=10

        if self.rect.left>player.rect.right: #and self.rect.left-player.rect.right>200:# if player is to the left
            self.speedx=-1
            self.facing='L'
            self.shoot()
            self.angle=90
        if self.rect.right<player.rect.left: #and player.rect.left-self.rect.right>200:#if player is to the right, turn to face player
            self.speedx=1
            self.facing='R'
            self.shoot()
            self.angle=270
        if self.rect.top>player.rect.bottom: #and self.rect.top-player.rect.bottom>200: #if player is above enemy, turn to face player
            self.speedy=-1
            self.facing='U'
            self.shoot()
            self.angle=0
        if self.rect.bottom<player.rect.top: #and player.rect.top-self.rect.bottom>200: #if player is below enemy, turn to face player
            self.speedy=1
            self.facing='D'
            self.shoot()
            self.angle=180

        self.image = pygame.transform.rotate(m.original, self.angle) #rotate enemy ship to face correct direction



    def shoot(self): #enemy shoot

        x=random.uniform(1,400) #picks a random number and if number under 20, CPU will shoot...
        if x<20:
            mphaser = Mphaser(self.rect.centerx, self.rect.top)
            all_sprites.add(mphaser)
            mphasers.add(mphaser)
            pygame.mixer.init()
            effect = pygame.mixer.Sound('enemyfire.wav') #enemy fire sound effect
            effect.play()



class Pphaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_weapon
        self.image.set_colorkey(BLACK)
        #self.image = pygame.Surface((5, 5))
        #self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.rect.top=y
        self.rect.bottom = y+28 #adjust so bullet leaves at y center of ship
        self.speedy = -10
        self.speedx=-10
        if not player.facing:
            player.facing='D'
        self.pphaserface=player.facing #so bullets fire in direction ship last faced

    def update(self):
        if self.pphaserface=='U':
            self.rect.y+=self.speedy #if last ship pos facing up, fire phaser upwards
        elif self.pphaserface=='D':
            self.rect.y-=self.speedy
        elif self.pphaserface=='L':
            self.rect.x+=self.speedx
        elif self.pphaserface =='R':

            self.rect.x-=self.speedx

        # kill pphaser if goes off the screen
        if self.rect.bottom>WIDTH:
            self.kill()
        elif self.rect.top<0:
            self.kill()
        elif self.rect.left<0:
            self.kill()
        elif self.rect.right>WIDTH:
            self.kill()

class Mphaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.transform.scale(enemy_weapon, (10, 7)) #resizes enemy fire
            #self.image = enemy_weapon
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.rect.top = y
            self.rect.bottom = y + 5
            self.speedy = -10
            self.speedx = -10
            self.mphaserface = m.facing  # bullets fire in direction ship last faced

    def update(self):


        if self.mphaserface=='U':
            self.rect.y+=self.speedy #if last ship pos facing up, fire phaser upwards
        elif self.mphaserface=='D':
            self.rect.y-=self.speedy
        elif self.mphaserface=='L':
            self.rect.x+=self.speedx
        elif self.mphaserface =='R':
            self.rect.x-=self.speedx

        # kill pphaser if goes off the screen
        if self.rect.bottom>WIDTH:
            self.kill()
        elif self.rect.top<0:
            self.kill()
        elif self.rect.left<0:
            self.kill()
        elif self.rect.right>WIDTH:
            self.kill()

#Load all game graphics
background = pygame.image.load("space.jpg").convert()
background_rect = background.get_rect()
player_img = pygame.image.load("player.png").convert()
player_img2 = pygame.image.load("pshield.jpg").convert()
enemy_img = pygame.image.load("enemy.png").convert()
enemy_img2=pygame.image.load("mshield.jpg").convert()
explosion=pygame.image.load("explosion.png").convert()
asteroid=pygame.image.load("asteroid.png").convert()
player_weapon = pygame.image.load("playerfire.jpg").convert()
enemy_weapon=pygame.image.load("enemyfire.png").convert()
player_hit=False
enemy_hit=False

#start music 
#pygame.mixer.init()
#pygame.mixer.music.load("music.mp3")
#pygame.mixer.music.play(-1)
#pygame.mixer.music.set_volume(5)




all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
pphasers=pygame.sprite.Group()
mphasers=pygame.sprite.Group()
asteroid=Asteroid()
all_sprites.add(asteroid)
player = Player()
all_sprites.add(player)

m = Mob()
all_sprites.add(m)
mobs.add(m)

time_hit=0
mtime_hit=0

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                pygame.mixer.init()
                player.shoot()

    # Update
    all_sprites.update()
    all_sprites.draw(screen)

    hits=pygame.sprite.spritecollide(asteroid,pphasers,True,False) 
    hits=pygame.sprite.spritecollide(asteroid,mphasers,True,False)


    #did player fire hit the enemy?

    hits=pygame.sprite.groupcollide(pphasers,mobs,True,False)

    if hits:
        mob_hit=True
        mob_shields-=2
        mtime_hit = pygame.time.get_ticks()   # if player hit set time for duration shield bubble appears on screen
    if mob_shields<=0:
        running=False #If mob loses shields, game is over...

    #did mob fire hit player?
    hits = pygame.sprite.spritecollide(player,mphasers,True)
    if hits:
        player.player_shields -= 2
        time_hit = pygame.time.get_ticks()  #if player hit set time for duration shield bubble appears on screen

        if player.player_shields<=0:
            time_now=pygame.time.get_ticks()
            running = False  # If mob loses shields, game is over...


    if time_hit+100>pygame.time.get_ticks() :
        player.image = pygame.transform.scale(player_img2, (50, 38)) #if hit show player shield bubble
    if mtime_hit+100>pygame.time.get_ticks() :
        m.image = pygame.transform.scale(enemy_img2, (50, 38)) #if hit show enemy shield bubble

    screen.fill(BLACK) #draw screen
    screen.blit(background,background_rect)
    all_sprites.draw(screen) #update all sprite groups
    draw_pshields()
    draw_mshields()
    pygame.display.flip()

pygame.quit()
