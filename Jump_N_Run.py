import sys
import pygame
from random import randint



def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = test_font.render(f'{current_time} ', True, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(600, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 4
            if obstacle_rect.bottom == 650:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []


def collision_checker(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True


def player_animations():
    global player_surf, player_index

    # play walking animation if the player is on floor
    # display the jump surface when the player is not on the floor
    if player_rect.bottom < 650:
        # jump
        player_surf = player_jump
    else:
        # walk
        player_index += 0.35
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]


pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('JUMP N RUN')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/fun.ttf', 50)
game_active = False
start_time = 0
score = 0


sky_surf = pygame.image.load('art/environment/Glowing_City.png').convert()
ground_surf = pygame.image.load('art/environment/ground.png').convert()

# Obstacles / Enemies
# Snail
snail_frame_01 = pygame.image.load('art/enemies/snailWalk1.png').convert_alpha()
snail_frame_02 = pygame.image.load('art/enemies/snailWalk2.png').convert_alpha()
snail_frames = [snail_frame_01, snail_frame_02]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame_01 = pygame.image.load('art/enemies/flyFly1.png').convert_alpha()
fly_frame_02 = pygame.image.load('art/enemies/flyFly2.png').convert_alpha()
fly_frames = [fly_frame_01, fly_frame_02]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

obstacle_rect_list = []

# Player
player_walk1 = pygame.image.load('art/player/p1_walk01.png').convert_alpha()
player_walk2 = pygame.image.load('art/player/p1_walk02.png').convert_alpha()
player_walk3 = pygame.image.load('art/player/p1_walk03.png').convert_alpha()
player_walk4 = pygame.image.load('art/player/p1_walk04.png').convert_alpha()
player_walk5 = pygame.image.load('art/player/p1_walk05.png').convert_alpha()
player_walk6 = pygame.image.load('art/player/p1_walk06.png').convert_alpha()
player_walk7 = pygame.image.load('art/player/p1_walk07.png').convert_alpha()
player_walk8 = pygame.image.load('art/player/p1_walk08.png').convert_alpha()
player_walk9 = pygame.image.load('art/player/p1_walk09.png').convert_alpha()
player_walk10 = pygame.image.load('art/player/p1_walk10.png').convert_alpha()
player_walk11 = pygame.image.load('art/player/p1_walk11.png').convert_alpha()
player_walk = [player_walk1, player_walk2, player_walk3, player_walk4, player_walk5,
               player_walk6, player_walk7, player_walk8, player_walk9, player_walk10,
               player_walk11]
player_index = 0
player_jump = pygame.image.load('art/player/p1_jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom=(100, 650))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('art/player/p1_front.png').convert_alpha()
player_stand_scaled = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand_scaled.get_rect(center=(600, 400))

game_name = test_font.render('Jump N Run', True, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(600, 230))
game_message = test_font.render('Press space to run', True, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(600, 600))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1550)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 400)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 150)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 650:
                    player_gravity = -10

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 650:
                    player_gravity = -20
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

        if game_active:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(1300, 1500), 650)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(1300, 1500), 560)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 650))
        score = display_score()

        # snail_rect.x -= 5
        # if snail_rect.right <= 0: snail_rect.left = 1200
        # screen.blit(snail_surf, snail_rect)

        # player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 650:
            player_rect.bottom = 650
        player_animations()
        screen.blit(player_surf, player_rect)

        # obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collision
        game_active = collision_checker(player_rect, obstacle_rect_list)
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_scaled, player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (100, 650)
        player_gravity = 0

        score_message = test_font.render(f'Your score: {score}', True, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(600, 550))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)
            screen.blit(game_message, game_message_rect)

    pygame.display.update()
    clock.tick(60)
