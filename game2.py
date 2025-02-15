import numpy as np
import pygame
import time
import sys

# Set globals
WALL_COLOR = (50, 50, 50)
GRID_COLOR = (0, 0, 0)
FLOOR_COLOR = (255, 255, 255)
FLOOR_NEXT_COL = (0, 0, 255)
FLOOR_PROB = 0.7
WALL_PROB = 0.3
SCREEN_W = 400
SCREEN_H = 600
mapgen_count = 0


def update(screen, cells, size, with_progress=False):
    # Create temporary matrix of zeros
    temp = np.zeros((cells.shape[0], cells.shape[1]))
    temp_w = len(temp[0])
    temp_h = len(temp)
    
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
    temp[0:temp_h, 0] = 1           # Left
    temp[0, 0:temp_w] = 1           # Top
    temp[0:temp_h, temp_w-1] = 1          # Right
    temp[temp_h-1, 0:temp_w] = 1          # Bottom

    # Set doorways in centre
    temp[30, 0] = 0

    # Set middle of the borders to zero
    mid_row = findArrayMid(temp[:, 0])
    mid_col = findArrayMid(temp[0, :])

    print(mid_row)

    # temp[mid_row, 0] = 0
    # temp[mid_row, 79] = 0
    # temp[0, mid_col] = 0
    # temp[59, mid_col] = 0

    # print(findArrayMid(temp[1]))
    # mapgen_count += 1

    return temp

def findArrayMid(array):
    mid = float(len(array)) / 2
    if mid % 2 == 0:
        return (int(mid), int(mid - 1))
    else:
        return int(mid - 0.5)


def main():
    # Initialise pygame
    pygame.init()

    # Set size of cells
    size = 10
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
    