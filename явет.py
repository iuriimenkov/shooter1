from pygame import *
from random import randint

window = display.set_mode((900, 600))
display.set_caption('Shooter')

background = image.load('galaxy.jpg')
background = transform.scale(background, (900, 600))

clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
# mixer.music.play()
shoot = mixer.Sound('fire.ogg')

lost = 0
score = 0

class GameSprite(sprite.Sprite):
    def __init__(self, img, x_pos, y_pos, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x_pos
        self.rect.y = y_pos
        self.speed = speed

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        pressed = key.get_pressed()
        if pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if pressed[K_d] and self.rect.x < 840:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 7, self.rect.top, 15, 15, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 600:
            self.rect.x = randint(0, 900-80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()


player = Player('rocket.png', 400, 480, 10, 50, 100)

enemies = sprite.Group()
for i in range(7):
    enemy = Enemy('ufo.png', randint(0, 900-80), 0, randint(1,5), 80, 40)
    enemies.add(enemy)
asteriods = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(0, 900-80), 0, randint(1,3), 80, 40)
    asteriods.add(asteroid)
bullets = sprite.Group()

game = True
finish = False
font.init()
f = font.Font(None, 30)

win = f.render('YOU WIN!', True, (255,255,255))
lose = f.render('YOU LOSE!', True, (255,255,255))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                shoot.play()


    if not finish:
        window.blit(background, (0, 0))

        score_text = f.render(f'Счёт: {str(score)}', True, (255,255,255))
        window.blit(score_text, (10, 10))

        lost_text = f.render(f'Пропущено: {str(lost)}', True, (255,255,255))
        window.blit(lost_text, (10, 50))


        player.draw()
        player.update()

        enemies.draw(window)
        enemies.update()

        asteriods.draw(window)
        asteriods.update()

        bullets.draw(window)
        bullets.update()

        collides = sprite.groupcollide(enemies, bullets, True, True)
        for c in collides:
            score += 1
            enemy = Enemy('ufo.png', randint(0, 900 - 80), 0, randint(1, 5), 80, 40)
            enemies.add(enemy)

        if sprite.spritecollide(player, enemies, True) or lost >= 3:
            finish = True
            window.blit(lose, (400, 275))

        if score >= 10:
            finish = True
            window.blit(win, (400, 275))



    display.update()
    # time.delay(50)
    clock.tick(FPS)