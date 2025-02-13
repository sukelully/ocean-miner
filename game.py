import pygame
import sys

# Initialise PyGame
pygame.init()

# Set up game window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simple Shooter Game")

# Set frame rate
clock = pygame.time.Clock()

# Player settings
player_width = 50
player_height = 60
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Handle player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
    
    # Fill the screen with a color (black in this case)
    screen.fill((0, 0, 0))
    

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 fps
    clock.tick(60)