import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('JUMP N RUN')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/fun.ttf', 50)
game_active = True

sky_surf = pygame.image.load('art/environment/Glowing_City.png').convert()
ground_surf = pygame.image.load('art/environment/ground.png').convert()

score_surf = test_font.render('Fun N Game', True, (64, 64, 64))
score_rect = score_surf.get_rect(center=(600, 50))

snail_surf = pygame.image.load('art/enemies/snailWalk1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright=(1200, 650))

player_surf = pygame.image.load('art/player/playerWalk1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(100, 650))
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if player_rect.collidepoint(event.pos) and player_rect.bottom >= 650:
                player_gravity = -20

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_rect.bottom >= 650:
                player_gravity = -20

    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, 650))
    pygame.draw.rect(screen, '#997EE4', score_rect)
    pygame.draw.rect(screen, '#997EE4', score_rect, 10)
    screen.blit(score_surf, score_rect)

    snail_rect.x -= 5
    if snail_rect.right <= 0: snail_rect.left = 1200
    screen.blit(snail_surf, snail_rect)

    player_gravity += 1
    player_rect.y += player_gravity
    if player_rect.bottom >= 650:
        player_rect.bottom = 650
    screen.blit(player_surf, player_rect)

    if snail_rect.colliderect(player_rect):
        sys.exit()

    pygame.display.update()
    clock.tick(60)
