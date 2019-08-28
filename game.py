#1. import library
import math
import pygame
from pygame.locals import *
from random import randint

#2. inisialisasi game
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

# key mapping
keys = {
    "top": False,
    "bottom": False,
    "left": False,
    "right": False
}

running = True
playerpos = [150, 240] #inisialisasi posisi pemain

# exit code for game over and win condition
exitcode = 0
EXIT_CODE_GAME_OVER = 0
EXIT_CODE_WIN = 1

score = 0
health_point = 194
countdown_timer = 90000 # 90 detik
arrows = [] #list ofarrows

enemy_timer = 100 # waktu muncul
enemies = [[width, 100]] # list yg menampung kordinat musuh

#3. memanggil aset game
#3.1 load gambar
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
enemy_img = pygame.image.load("resources/images/badguy.png")
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
youwin = pygame.image.load("resources/images/youwin.png")

# 3.1 - Load audio
pygame.mixer.init()
hit_sound = pygame.mixer.Sound("resources/audio/explode.wav")
enemy_hit_sound = pygame.mixer.Sound("resources/audio/enemy.wav")
shoot_sound = pygame.mixer.Sound("resources/audio/shoot.wav")
hit_sound.set_volume(0.05)
enemy_hit_sound.set_volume(0.05)
shoot_sound.set_volume(0.05)

# background music
pygame.mixer.music.load("resources/audio/moonlight.wav")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

#4. game loop
while(running):
    
    #5. membersihkan tampilan
    screen.fill(0)

    #6. membuat objek game
    # membuat rumput
    for x in range(int(width/grass.get_width()+1)):
        for y in range(int(height/grass.get_height()+1)):
            screen.blit(grass, (x*100,y*100))

    # membuat kastil
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))

    # draw the player
    mouse_position = pygame.mouse.get_pos()
    angle = math.atan2(mouse_position[1] - (playerpos[1]+32), mouse_position[0] - (playerpos[0]+26))
    player_rotation = pygame.transform.rotate(player, 360 - angle * 57.29)
    new_playerpos = (playerpos[0] - player_rotation.get_rect().width / 2, playerpos[1] - player_rotation.get_rect().height / 2)
    screen.blit(player_rotation, new_playerpos)

    #6.1 draw arrows
    for bullet in arrows:
        arrow_index = 0
        velx=math.cos(bullet[0])*10
        vely=math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1] < -64 or bullet[1] > width or bullet[2] < -64 or bullet[2] > height:
            arrows.pop(arrow_index)
        arrow_index += 1
        # draw the arrow
        for projectile in arrows:
            new_arrow = pygame.transform.rotate(arrow, 360-projectile[0]*57.29)
            screen.blit(new_arrow, (projectile[1], projectile[2]))

    #6.2 draw enemy
    # waktu musuh akan muncul
    enemy_timer -= 1
    if enemy_timer == 0:
        #buat musuh baru
        enemies.append([width, randint(50, height-32)])
        #reset enemy timer to rando time
        enemy_timer = randint(1, 100)
    
    index = 0
    for enemy in enemies:
        # musuh bergerak dengan kecepatan 5 pixel ke kiri
        enemy[0] -= 5
        # hapus musuh saat mencapai batas layar sebelah kiri
        if enemy[0] < -64:
            enemies.pop(index)

    #6.2.1 collision between enemies and castle
    enemy_rect = pygame.Rect(enemy_img.get_rect())
    enemy_rect.top = enemy[1] #ambil titik y
    enemy_rect.left = enemy[0] #ambil titik x
    # benturan musuh dengan markas kelinci
    if enemy_rect.left < 64:
        enemies.pop(index)
        health_point -= randint(5, 20)
        hit_sound.play()
        print("oh tidak, kita diserang!!!!!!!")

    #6.2.2 check for collision between eneies and arrows
    index_arrow = 0
    for bullet in arrows:
        bullet_rect = pygame.Rect(arrow.get_rect())
        bullet_rect.left = bullet[1]
        bullet_rect.top = bullet[2]
        #benturan anak panah dengan musuh
        if enemy_rect.colliderect(bullet_rect):
            score += 1
            enemies.pop(index)
            arrows.pop(index_arrow)
            enemy_hit_sound.play()
            print("MATI KAU!!!")
            print("Score: {}".format(score))
        index_arrow += 1
    index += 1

    # gambar musuh ke layar
    for enemy in enemies:
        screen.blit(enemy_img, enemy)
        
    #6.3 Draw health bar
    screen.blit(healthbar, (5,5))
    for hp in range(health_point):
        screen.blit(health, (hp+8, 8))
    
    #6.4 draw clock
    font = pygame.font.Font(None, 24)
    minutes = int((countdown_timer-pygame.time.get_ticks())/60000) #60000 = 60 detik
    seconds = int((countdown_timer-pygame.time.get_ticks())/10000%60)
    time_text = "{:02}:{:02}".format(minutes, seconds)
    clock = font.render(time_text, True, (255,255,255))
    textRect = clock.get_rect()
    textRect.topright = [635, 5]
    screen.blit(clock, textRect)

    #7. memperbaharui tampilan
    pygame.display.flip()

    #8. event loop
    for event in pygame.event.get():
        # event saat tombol exit di klik
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

        # tembak
        if event.type == pygame.MOUSEBUTTONDOWN:
            arrows.append([angle, new_playerpos[0]+32, new_playerpos[1]+32])
            shoot_sound.play()

        # check keydown dan keyup
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys["top"] = True
            elif event.key == K_a:
                keys["left"] = True
            elif event.key == K_s:
                keys["bottom"] = True
            elif event.key == K_d:
                keys["right"] = True
        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys["top"] = False
            elif event.key == K_a:
                keys["left"] = False
            elif event.key == K_s:
                keys["bottom"] = False
            elif event.key == K_d:
                keys["right"] = False
    # end of event loop

    #9. perpindahan pemain
    if keys["top"]:
        playerpos[1] -= 5 # kurangi nilai y
    elif keys["bottom"]:
        playerpos[1] += 5 # tambah nilai y
    if keys["left"]:
        playerpos[0] -= 5 # kurangi nilai x
    elif keys["right"]:
        playerpos[0] += 5 # tambah nilai x

    #10. win/lose chexk
    if pygame.time.get_ticks() > countdown_timer:
        running = False
        exitcode = EXIT_CODE_WIN
    if health_point <= 0:
        running = False
        exitcode = EXIT_CODE_GAME_OVER
#End of game loop

#11 win/lose display
if exitcode == EXIT_CODE_GAME_OVER:
    screen.blit(gameover, (0,0))
else:
    screen.blit(youwin, (0,0))

# tampilkan score
text = font.render("Score: {}".format(score), True, (255, 255, 255))
textRect = text.get_rect()
textRect.centerx = screen.get_rect().centerx
textRect.centery = screen.get_rect().centery + 24
screen.blit(text, textRect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
    pygame.display.flip()
