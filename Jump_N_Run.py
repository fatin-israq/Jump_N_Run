import random
import sys
import pygame
from random import randint, choice


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
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
        self.player_walk = [player_walk1, player_walk2, player_walk3, player_walk4, player_walk5,
                            player_walk6, player_walk7, player_walk8, player_walk9, player_walk10,
                            player_walk11]
        self.player_index = 0
        self.player_jump = pygame.image.load('art/player/p1_jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(200, 650))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.bottom >= 650:
            self.gravity = -20
            self.jump_sound.play()


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 650:
            self.rect.bottom = 650

    def animation_state(self):
        if self.rect.bottom < 650:
            self.image = self.player_jump
        else:
            self.player_index += 0.35
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_frame_01 = pygame.image.load('art/enemies/flyFly1.png').convert_alpha()
            fly_frame_02 = pygame.image.load('art/enemies/flyFly2.png').convert_alpha()
            self.frames = [fly_frame_01, fly_frame_02]
            y_pos = 550
        elif type == 'snail':
            snail_frame_01 = pygame.image.load('art/enemies/snailWalk1.png').convert_alpha()
            snail_frame_02 = pygame.image.load('art/enemies/snailWalk2.png').convert_alpha()
            self.frames = [snail_frame_01, snail_frame_02]
            y_pos = 650
        elif type == 'slime':
            slime_frame_01 = pygame.image.load('art/enemies/slimeWalk1.png')
            slime_frame_02 = pygame.image.load('art/enemies/slimeWalk2.png')
            self.frames = [slime_frame_01, slime_frame_02]
            y_pos = 652
        else:
            # in case of adding any other obstacles
            y_pos = 0

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(1300, 1500), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        if display_score() < 30:
            self.rect.x -= 5
        elif display_score() < 70:
            self.rect.x -= 7
        else:
            self.rect.x -= 10
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    current_time = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = test_font.render(f'{current_time} ', True, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(600, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        death_audio = pygame.mixer.Sound('audio/death.wav')
        death_audio.play()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('JUMP N RUN')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/fun3.otf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/background_music.ogg')
bg_music.set_volume(0.5)
bg_music.play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surf = pygame.image.load('art/environment/sky.png').convert()
ground_surf = pygame.image.load('art/environment/ground.png').convert()

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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'slime', 'snail'])))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 650))
        score = display_score()

        # player
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        # collision
        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand_scaled, player_stand_rect)

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
