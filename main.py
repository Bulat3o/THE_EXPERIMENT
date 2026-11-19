import pygame
import random

WIDTH = 1080
HEIGHT = 1080
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EXPERIMENT")
clock = pygame.time.Clock()
screen.fill(BLACK)
spr_gaster = pygame.image.load("Wrenche.png")
FONT_PATH = 'font_fish.ttf'
font = pygame.font.SysFont(FONT_PATH, 32)
text = font.render("продолжай", True, WHITE)
screen.blit(text, (180, 240))
#screen.blit(spr_gaster, (20, 20))
pygame.display.flip()
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            screen.blit(spr_gaster, (10, 10))

    pygame.display.flip()