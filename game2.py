import pygame
import numpy as np
import sys

# Set globals
SCREEN_W, SCREEN_H = 800, 600
WALL_COLOR = (50, 50, 50)
GRID_COLOR = (0, 0, 0)
FLOOR_COLOR = (255, 255, 255)
FLOOR_NEXT_COL = (0, 0, 255)
FLOOR_PROB = 0.7
WALL_PROB = 0.3
ACCELERATION = 0.2
FRICTION = 0.1
MAX_SPEED = 5
mapgen_count = 0

# Player attributes
player_width = 20
player_height = 10
player_pos = pygame.Vector2(SCREEN_W // 2, SCREEN_H // 2)
velocity = pygame.Vector2(0, 0)

# Set the frame rate
clock = pygame.time.Clock()

def generate_map(screen, cells, size, with_progress=False):
    temp = np.zeros((cells.shape[0], cells.shape[1]))
    temp_w, temp_h = len(temp[0]), len(temp)

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

    # Set borders to walls
    temp[:, 0] = 1
    temp[0, :] = 1
    temp[:, temp_w - 1] = 1
    temp[temp_h - 1, :] = 1

    # Create 5-cell wide exit points
    mid_row, mid_col = len(temp) // 2, len(temp[0]) // 2
    temp[mid_row - 5:mid_row + 6, 0] = 0
    temp[mid_row - 5:mid_row + 6, temp_w - 1] = 0
    temp[0, mid_col - 5:mid_col + 6] = 0
    temp[temp_h - 1, mid_col - 5:mid_col + 6] = 0

    return temp

def drawPlayer(screen):
    pygame.draw.rect(screen, (0, 175, 255), (int(player_pos.x), int(player_pos.y), player_width, player_height))

def is_wall(x, y, cells, size):
    grid_x, grid_y = int(x / size), int(y / size)
    return cells[grid_y, grid_x] == 1

def main():
    global velocity, player_pos  # Ensure these persist across frames
    pygame.init()
    size = 10
    cells_w, cells_h = SCREEN_W // size, SCREEN_H // size

    # Initialize the map
    cells = np.random.choice(2, size=(cells_h, cells_w), p=[FLOOR_PROB, WALL_PROB])
    cells[0:cells_h, 0] = 1
    cells[0, 0:cells_w] = 1
    cells[0:cells_h, cells_w - 1] = 1
    cells[cells_h - 1, 0:cells_w] = 1

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    screen.fill(GRID_COLOR)

    mapgen_count = 0

    # Game loop
    while True:
        screen.fill(GRID_COLOR)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                mapgen_count = 0
                generate_map(screen, cells, size)
                print("Space!")

        # Map generation
        if mapgen_count < 2:
            cells = generate_map(screen, cells, size, with_progress=True)
            mapgen_count += 1
        else:
            # Player Movement Handling
            acceleration = pygame.Vector2(0, 0)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                acceleration.x = -ACCELERATION
            if keys[pygame.K_RIGHT]:
                acceleration.x = ACCELERATION
            if keys[pygame.K_UP]:
                acceleration.y = -ACCELERATION
            if keys[pygame.K_DOWN]:
                acceleration.y = ACCELERATION

            # Apply acceleration to velocity
            velocity += acceleration

            # Apply friction when no keys are pressed
            if acceleration.length() == 0:
                velocity *= (1 - FRICTION)

            # Cap velocity to MAX_SPEED
            if velocity.length() > MAX_SPEED:
                velocity = velocity.normalize() * MAX_SPEED

            # Calculate new position
            new_pos = player_pos + velocity

            # Collision checking (prevent moving into walls)
            if not is_wall(new_pos.x, player_pos.y, cells, size):
                player_pos.x = new_pos.x
            if not is_wall(player_pos.x, new_pos.y, cells, size):
                player_pos.y = new_pos.y

            # Draw the map
            for row, col in np.ndindex(cells.shape):
                color = FLOOR_COLOR if cells[row, col] == 0 else WALL_COLOR
                pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

            drawPlayer(screen)

        pygame.display.flip()
        clock.tick(60)  # Cap FPS to 60

if __name__ == "__main__":
    main()
