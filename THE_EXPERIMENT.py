import pygame
import random

WIDTH = 1080
HEIGHT = 1080
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DETERMINATION = (255, 0, 0)
JUSTICE = (255, 255, 0)


pygame.init()
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound('snd_heartshot_dr_b.wav')
charge_sound = pygame.mixer.Sound('snd_chargeshot_charge.wav')
charge_shoot = pygame.mixer.Sound('snd_chargeshot_fire.wav')
charge_sound.set_volume(0.3)
charge_shoot.set_volume(0.3)
shoot_sound.set_volume(0.3)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EXPERIMENT")
clock = pygame.time.Clock()
font = pygame.font.SysFont("comicsans", 32)
text = font.render("e", True, WHITE)
screen.fill(BLACK)
bullet_bank = []
bullet_capacity = 8000
enemy_bank = []
class BULLET:
    def __init__(self, x, y, dx, dy, size, color, damage):
        self.index = len(bullet_bank)-1
        self.color = color
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = size
        self.damage = damage
        self.picture = pygame.Rect(self.x-size/2, self.y-size/2, size, size)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.picture.move_ip(self.dx, self.dy)
        if self.y < 0:
            self.destroy()

    def destroy(self):
        bullet_bank.remove(self)
        del self

    def render(self):
        pygame.draw.ellipse(screen, self.color, self.picture)

class DEVICE:
    """
    THE CULMINATION OF YOUR BEING
    """

    def __init__(self):
        self.shot_charge = 0
        self.color = JUSTICE
        self.x = 500
        self.y = 500
        self.speed = 5 * (30/FPS)
        self.picture = pygame.Rect(self.x, self.y, 20, 20)

    def movement_manage(self, keys):
        if keys[pygame.K_LEFT]:
            self.picture.move_ip(-self.speed, 0)
        if keys[pygame.K_RIGHT]:
            self.picture.move_ip(self.speed, 0)
        if keys[pygame.K_UP]:
            self.picture.move_ip(0, -self.speed)
        if keys[pygame.K_DOWN]:
            self.picture.move_ip(0, self.speed)

        self.x = self.picture.x+10
        self.y = self.picture.y+10

    def action_manage(self, keys, events):
        if keys[pygame.K_z]:
           self.shot_charge += 0.1
           charge_sound.play(fade_ms=1000, loops=999)
        else:
            charge_sound.stop()
            if self.shot_charge > 3:
                charge_shoot.play()
                bullet_bank.append(BULLET(self.x, self.y, 0, -7.5, 20, JUSTICE, 20))
            elif self.shot_charge > 0:
                shoot_sound.play()
                bullet_bank.append(BULLET(self.x, self.y, 0, -7.5, 10, JUSTICE, 3))
            self.shot_charge = 0

    def render(self):
        pygame.draw.ellipse(screen, self.color, self.picture)

class ENEMY:
    def __init__(self, health, size, color, spawnX, spawnY, move_speed):
        self.x = spawnX
        self.y = spawnY
        self.health = health
        self.size = size
        self.color = color
        self.speed = move_speed
        self.picture = pygame.Rect(self.x, self.y, size, size)

    def passive_move(self):
        if self.x > 1000 or self.x < 80:
            self.speed = -self.speed

        self.picture.move_ip(self.speed, 0)

    def check_collision(self):
        for bullet in bullet_bank:
            if self.picture.colliderect(bullet.picture):
                self.health -= bullet.damage
                bullet.destroy()
                if self.health < 0:
                    self.destroy()

    def destroy(self):
        enemy_bank.remove(self)
        del self

    def render(self):
        pygame.draw.ellipse(screen, self.color, self.picture)

    def passiveLoop(self):
        self.passive_move()
        self.check_collision()

player = DEVICE()
run = True
enemy_bank.append(ENEMY(20, 40, GREEN, 500, 100, 2))
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()
    player.movement_manage(keys)
    player.action_manage(keys, events)
    player.render()
    for bullet in bullet_bank:
        bullet.update()
        bullet.render()
    for enemy in enemy_bank:
        enemy.passiveLoop()
        enemy.render()
    text = font.render(str(len(bullet_bank)), True, WHITE)
    screen.blit(text, (20, 20))
    pygame.display.flip()
    clock.tick(FPS)
