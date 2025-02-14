import numpy as np
import pygame
import time
import sys

# Set colors
WALL_COLOR = (50, 50, 50)
GRID_COLOR = (0, 0, 0)
FLOOR_COLOR = (255, 255, 255)
FLOOR_NEXT_COL = (0, 0, 255)
FLOOR_PROB = 0.7
WALL_PROB = 0.3

def update(screen, cells, size, with_progress=False):
    # Create temporary matrix of zeros
    temp = np.zeros((cells.shape[0], cells.shape[1]))
    
    for row, col in np.ndindex(cells.shape):
        walls = np.sum(cells[row - 1:row + 2, col-1:col+2]) - cells[row, col]      
        color = FLOOR_COLOR if cells[row, col] == 0 else WALL_COLOR
        
        #Apply rules (if more than 4 walls create a wall, else a floor)
        if walls > 4:
            temp[row, col] = 1
            if with_progress:
                color = WALL_COLOR  
        else:
            if cells[row, col] == 1:
                if with_progress:
                    color = FLOOR_NEXT_COL
        
        # Draw rectangles, using as background the screen value.
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))
    
    # Set borders to walls
    temp[0:60, 0] = 1
    temp[0, 0:80] = 1
    temp[0:60, 79] = 1
    temp[59, 0:80] = 1  
        
    return temp

def main():
    # Initialise pygame
    pygame.init()

    # Set size of cells
    size = 10

    # Set screen size
    SCREEN_W = 800
    SCREEN_H = 600

    # Set dimension of cells and their initial configuration
    cells = np.random.choice(2, size=(60, 80), p=[FLOOR_PROB, WALL_PROB])

    cells[0:60, 0] = 1
    cells[0, 0:80] = 1
    cells[0:60, 79] = 1
    cells[59, 0:80] = 1

    # Init screen
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    
    # Fill screen with grid
    screen.fill(GRID_COLOR)

    update(screen, cells, size)

    # Update full screen
    pygame.display.flip()

    # Update only portions of the screen
    pygame.display.update()

    # Init running as false, so it won't immediately start the game
    running = False

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, size)
                    pygame.display.update()
        
        if running:
            cells = update(screen, cells, size, with_progress=True)
            pygame.display.update()
        time.sleep(2)

if __name__ == '__main__':
    main()
    