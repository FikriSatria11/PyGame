#1. import library
import pygame
from pygame.locals import *

#2. inisialisasi game
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

running = True

playerpos = [100, 100] #inisialisasi posisi pemain

#3. memanggil aset game
#3.1 load gambar
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")

#4. game loop
while(running):
    
    #5. membersihkan tampilan
    screen.fill(0)

    #6. membuat objek game
    # membuat rumput
    for x in range(int(width/grass.get_width()+1)):
        for y in range(int(height/grass.get_height()+1)):
            screen.blit(grass, (x*100,y*100))

    #ebuat kastil
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))

    screen.blit(player, playerpos)

    #7. memperbaharui tampilan
    pygame.display.flip()

    #8. event loop
    for event in pygame.event.get():
        # event saat tombol exit di klik
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
