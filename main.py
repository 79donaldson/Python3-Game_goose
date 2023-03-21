import random
import pygame
from os import listdir
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

screen = width, heigth = 1200, 800

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0

font =pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen)

img_path = 'goose'
# player = pygame.Surface((20, 20))
# player.fill(WHITE)
DEFAULT_IMAGE_SIZE = (80, 40)
player_imgs = [pygame.transform.scale(pygame.image.load(img_path + '/' + file).convert_alpha(), DEFAULT_IMAGE_SIZE) for file in listdir(img_path)]
player = player_imgs[0]
#player = pygame.transform.scale(pygame.image.load('player.png').convert_alpha(), DEFAULT_IMAGE_SIZE)
player_rect = player.get_rect()
player_speed = 5



def create_enemy():
    # enemy = pygame.Surface((20, 20))
    # enemy.fill(RED)
    DEFAULT_IMAGE_SIZE = (60, 30)
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), DEFAULT_IMAGE_SIZE)
    enemy_rect = pygame.Rect(width, random.randint(0, heigth), *enemy.get_size())
    enemy_speed = random.randint(1, 5)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    # bonus = pygame.Surface((20, 20))
    # bonus.fill(GREEN)
    DEFAULT_IMAGE_SIZE = (80, 110)
    bonus = pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), DEFAULT_IMAGE_SIZE)
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonus_speed = random.randint(1, 5)
    return [bonus, bonus_rect, bonus_speed]

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen )
bgx = 0
bgx2 = bg.get_width()
bg_speed = 3

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_bonus = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_bonus, 2500)

CHANGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMG, 125)



scores = 0
scores_enemy = 0

enemies = []
bonuses = []

img_index = 0

is_working = True

while is_working:
    FPS.tick(90)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False
            
        if event.type == CREATE_ENEMY:            
            enemies.append(create_enemy())
        
        if event.type == CREATE_bonus:
            bonuses.append(create_bonus())
            
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]
                  
    
    pressed_keys = pygame.key.get_pressed()            
           
    # main_surface.fill(BLACK)
    
    #main_surface.blit(bg, (0, 0))
    
    bgx -= bg_speed
    bgx2 -= bg_speed
    
    if bgx < -bg.get_width():
        bgx = bg.get_width()        
    
    if bgx2 < -bg.get_width():
        bgx2 = bg.get_width()
        
    main_surface.blit(bg, (bgx, 0))
    main_surface.blit(bg, (bgx2, 0))
    
    main_surface.blit (player, player_rect)
    
    main_surface.blit(font.render("Score_Bonus", True, BLACK), (width -250, 0))
    main_surface.blit(font.render(str(scores), True, BLACK), (width -60, 0))
    main_surface.blit(font.render("Score_ENEMY", True, BLACK), (width -250, 30))
    main_surface.blit(font.render(str(scores_enemy), True, BLACK), (width -60, 30))
    
    for enemy in enemies: 
        enemy[1] = enemy[1].move(-enemy[2], 0) 
        main_surface.blit (enemy[0], enemy[1])    
      
        
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
            scores_enemy += 1
        if player_rect.colliderect(enemy[1]):                      
           
           is_working = False
            
              
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])
        
        if bonus[1].bottom >= heigth:
            bonuses.pop(bonuses.index(bonus))
        
        if player_rect.colliderect(bonus[1]):            
            bonuses.pop(bonuses.index(bonus))
            scores += 1
        
                        
    if pressed_keys[K_DOWN] and not player_rect.bottom >= heigth:
        player_rect = player_rect.move(0, player_speed) 
        
    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, - player_speed)        
    
    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0) 
        
    if pressed_keys[K_LEFT] and not player_rect.left <=0:        
        player_rect = player_rect.move(- player_speed, 0)
        
    pygame.display.flip()