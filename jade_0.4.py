import pygame
import random
from os import path

WIDTH = 480
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.display.init()
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jade")
clock = pygame.time.Clock()

img_dir = path.join(path.dirname(__file__), 'img')
player_img = pygame.image.load(path.join(img_dir, "spaceship.png")).convert()
meteor_img = pygame.image.load(path.join(img_dir, "asteroid.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "bullet.png")).convert()
background = pygame.image.load(path.join(img_dir, 'bg.png')).convert()
star_img = pygame.image.load(path.join(img_dir, 'star.png')).convert()
background_rect = background.get_rect()

class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image = pygame.transform.scale(player_img, (21, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 12
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        pressedkeys = pygame.key.get_pressed()
        if pressedkeys[pygame.K_a]:
            self.speedx = -5
        if pressedkeys[pygame.K_d]:
            self.speedx = 5
        if pressedkeys[pygame.K_s]:
            self.speedy = 5
        if pressedkeys[pygame.K_w]:
            self.speedy = -5
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Stars(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = star_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.width3 = random.randrange(1, 10)
        self.image = pygame.transform.scale(star_img, (self.width3, self.width3))
        self.image.set_colorkey(BLACK)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < - 25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Mob(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.width2 = random.randrange(20, 50)
        self.image = pygame.transform.scale(meteor_img, (self.width2, self.width2))
        self.image.set_colorkey(BLACK)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < - 25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        self.image = pygame.transform.scale(bullet_img, (10, 50))
        self.image.set_colorkey(BLACK)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
stars = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for i in range(10):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

for i in range(20):
    m = Stars()
    all_sprites.add(m)
    stars.add(m)

# main loop
running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_j:
                player.shoot()


    # update all sprites
    all_sprites.update()
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)

    # collision
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    hits = pygame.sprite.spritecollide(player, mobs, False, )
    if hits:
        running = False

    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
