#Создай собственный Шутер!

from pygame import *
from random import randint 

font.init()
font1 = font.SysFont("Arial",75)
winNER = font1.render('Win',True,(255,255,255))
Lose = font1.render('LOSE',True,(180,0,0))
font2 = font.SysFont("Arial",30)
WHITE = (255, 255, 255)
win_height = 500
win_widht = 700
win = display.set_mode((win_widht,win_height))
display.set_caption("shooter")
game = True
FPS = 60
score = 0
lost = 0
max_lost = 5
life = 3
finish = False
goal = 10
img_bullet = "bullet.png"
bullet_sum = 10
color_life = 0,255,0   
score_of_astr = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image,player_x,player_y,player_speed,size_x,size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        
    def reset(self):
        win.blit(self.image,(self.rect.x,self.rect.y))
    

#игрок(класс)

bullets = sprite.Group()
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y  > 500:
            self.kill()
class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >5:
            self.rect.x -= 5
        elif keys[K_RIGHT]and self.rect.x < 620:
            self.rect.x += 5
        
    def fire(self):
        bullet = Bullet(img_bullet,self.rect.centerx,self.rect.top,15,20,15)
        bullets.add(bullet)

        

#враг
class ENEMY(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 525:

            self.rect.y -= 525
            self.rect.x = randint(0,500)
            self.speed = randint(1, 3)
            lost = lost + 1
class ASTR(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 525:

            self.rect.y -= 525
            self.rect.x = randint(0,500)
            self.speed = randint(1, 3)
            
        
        
    def reset(self):
        win.blit(self.image,(self.rect.x,self.rect.y))

    

all_sprites = sprite.Group()
        
enemys =sprite.Group()
bullets = sprite.Group()
for i in range(1,6):
    enm = ASTR("asteroid.png",randint(5,695),0,randint(1,3),50,50)
    enemys.add(enm)
vragi = sprite.Group()
for i in range(1,6):
    monstr = ENEMY("ufo.png",randint(5,695),0,randint(1,3),50,50)
    vragi.add(monstr)

background = transform.scale(
    image.load("galaxy.jpg"),
    (win_widht,win_widht)
)


player = Player("rocket.png",0,430,8,50,50)


# Создание группы пуль

# Основной цикл игры
while game == True:
    for e in event.get(): 
        if e.type == QUIT:
            game = False    
            display.update()
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                bullet_sum = bullet_sum - 1
                if bullet_sum == 0:
                    from time import sleep
                    bullet_sum = 10 
                    
    
    if not finish:
        #изображение
        
        win.blit(background,(0,0))
        
        
        
        player.update()
        player.reset()
        enemys.update()
        enemys.draw(win)
        bullets.update()
        bullets.draw(win)
        vragi.update()
        vragi.draw(win)
        cols = sprite.groupcollide(enemys,bullets,True,True)
        collides = sprite.groupcollide(vragi,bullets,True,True)
        col = sprite.spritecollide(player,enemys,True)
        for c in cols:
            score_of_astr = score_of_astr + 1
            enm = ASTR("asteroid.png",randint(5,695),0,randint(1,3),50,50)
            enemys.add(enm)
        for c in collides:
            score = score + 1
            monstr = ENEMY("ufo.png",randint(5,695),0,randint(1,3),50,50)
            vragi.add(monstr)
        for c in col:
            life = life - 1
            monstr = ENEMY("ufo.png",randint(5,695),0,randint(1,3),50,50)
            vragi.add(monstr)
        if life == 2:
            color_life = 255,233,0
        elif life == 1:
            color_life = 255,0,0
        if life <= 0:
            finish = True

            
            win.blit(background,(0,0))
            win.blit(Lose,(300,250))
            win.blit(text_lost,(300,220))
            win.blit(text,(300,190))
        if score >= goal:
            finish = True
            win.blit(background,(0,0))
            win.blit(winNER,(300,250)) 
            win.blit(text_lost,(300,220))
            win.blit(text,(300,190))
            win.blit(score_of,(10,110))
        text = font2.render("Score: "+ str(score), 1 ,(255,255,255))
        text_bull = font2.render("Ammo: "+ str(bullet_sum), 1 ,(255,255,255))
        win.blit(text,(10,20))
        win.blit(text_bull,(10,80 ))
        text_lost = font2.render("Lost: "+ str(lost), 1 ,(255,255,255))
        win.blit(text_lost,(10,50))
        text_LIFE = font2.render("Life: "+ str(life), 1 ,(color_life))
        win.blit(text_LIFE,(600,20))
        score_of = font2.render("Asteroid: "+ str(score_of_astr), 1 ,(255,255,255))
        win.blit(score_of,(10,110))
        display.update()
    time.delay(10)
    
