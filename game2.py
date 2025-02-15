import pygame
import numpy as np
import sys

# Set globals
WALL_COLOR = (50, 50, 50)
GRID_COLOR = (0, 0, 0)
FLOOR_COLOR = (255, 255, 255)
FLOOR_NEXT_COL = (0, 0, 255)
FLOOR_PROB = 0.7
WALL_PROB = 0.3
SCREEN_W = 800
SCREEN_H = 600
mapgen_count = 0

player_width = 20
player_height = 10
player_max_speed = 5

# Generate map with four exits
def generate_map(screen, cells, size, with_progress=False):
    temp = np.zeros((cells.shape[0], cells.shape[1]))
    temp_w = len(temp[0])
    temp_h = len(temp)
    
    for row, col in np.ndindex(cells.shape):
        walls = np.sum(cells[row - 1:row + 2, col - 1:col + 2]) - cells[row, col]
        color = FLOOR_COLOR if cells[row, col] == 0 else WALL_COLOR
        
        if walls > 4:
            temp[row, col] = 1
            if with_progress:
                color = WALL_COLOR
        elif cells[row, col] == 1 and with_progress:
            color = FLOOR_NEXT_COL
        
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))
    
    # Set window borders to walls
    temp[:, 0] = 1           # Left
    temp[0, :] = 1           # Top
    temp[:, temp_w - 1] = 1  # Right
    temp[temp_h - 1, :] = 1  # Bottom

    mid_row = findArrayMid(temp[:, 0])
    mid_col = findArrayMid(temp[0, :])

    # Set the five rows/columns on either side of the middle to zero
    temp[mid_row-5:mid_row+6, 0] = 0
    temp[mid_row-5:mid_row+6, temp_w - 1] = 0
    temp[0, mid_col-5:mid_col+6] = 0
    temp[temp_h - 1, mid_col-5:mid_col+6] = 0
    
    return temp

def findArrayMid(array):
    mid = len(array) // 2
    return mid

def drawPlayer(screen, player_x, player_y):
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, player_width, player_height))

def main():
    pygame.init()
    size = 10
    player_speed = 0
    cells_w = int(round(SCREEN_W / size))
    cells_h = int(round(SCREEN_H / size))

    # Set dimension of cells and their initial configuration
    cells = np.random.choice(2, size=(cells_h, cells_w), p=[FLOOR_PROB, WALL_PROB])

    # Set borders to walls
    cells[0:cells_h, 0] = 1
    cells[0, 0:cells_w] = 1
    cells[0:cells_h, cells_w-1] = 1
    cells[cells_h-1, 0:cells_w] = 1

    # Init screen
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    
    # Fill screen with grid
    screen.fill(GRID_COLOR)

    player_x = SCREEN_W // 2
    player_y = SCREEN_H // 2

    mapgen_count = 0

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mapgen_count = 0
                    generate_map(screen, cells, size)
                    print("Space!")

        if mapgen_count < 2:
            cells = generate_map(screen, cells, size, with_progress=True)
            mapgen_count += 1
        else:
            keys = pygame.key.get_pressed()
            player_speed += 0.02
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < SCREEN_W - player_width:
                player_x += player_speed
            if keys[pygame.K_UP] and player_y > 0:
                player_y -= player_speed
            if keys[pygame.K_DOWN] and player_y < SCREEN_H - player_height:
                player_y += player_speed
            
            screen.fill(GRID_COLOR)

            for row, col in np.ndindex(cells.shape):
                color = FLOOR_COLOR if cells[row, col] == 0 else WALL_COLOR
                pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))
                
            drawPlayer(screen, player_x, player_y)

        pygame.display.flip()

if __name__ == "__main__":
    main()