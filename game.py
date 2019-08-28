# import library
import pygame
from pygame.locals import *

# inisialisasi game
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

running = True

playerpos = [100, 100] #inisialisasi posisi pemain

# memanggil image game
player = pygame.image.load("resources/images/dude.png")

# game loop
while(running):
    
    # membersihkan tampilan
    screen.fill(0)

    # membuat objek game
    screen.blit(player, playerpos)

    # memperbaharui tampilan
    pygame.display.flip()

    # event loop
    for event in pygame.event.get():
        # event saat tombol exit di klik
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
