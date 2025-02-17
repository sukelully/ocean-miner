import pygame
import numpy as np
import sys

# Set globals
SCREEN_W, SCREEN_H = 800, 600
WALL_COLOR = (50, 50, 50)
GRID_COLOR = (0, 0, 0)
FLOOR_COLOR = (255, 255, 255)
TEST_COLOR = (255, 0, 0)
FLOOR_PROB = 0.7
WALL_PROB = 0.3
ACCELERATION = 0.1
FRICTION = 0.05
MAX_SPEED = 3
mapgen_iterations = 4

# Player attributes
player_width = 20
player_height = 10
player_pos = pygame.Vector2(SCREEN_W // 2 - player_width / 2, SCREEN_H // 2 - player_height / 2)
velocity = pygame.Vector2(0, 0)

# Set the frame rate
clock = pygame.time.Clock()

# Draw player at specified position
def drawPlayer(screen):
    pygame.draw.rect(screen, (0, 175, 255), (int(player_pos.x), int(player_pos.y), player_width, player_height))

# Return true if cell is a wall
def is_wall(x, y, cells, size):
    grid_x, grid_y = int(x / size), int(y / size)
    return cells[grid_y, grid_x] == 1

# Collision checking
def detect_collision(rect1, cells, size):
    collision_detected = False
    for row, col in np.ndindex(cells.shape):
        if cells[row, col] == 1:  # If the cell is a wall
            wall_rect = pygame.Rect(col * size, row * size, size, size)
            if rect1.colliderect(wall_rect):
                collision_detected = True
                break

    return collision_detected

# Initialise a cell grid with random values to seed map generation
def initialise_map(cells_w, cells_h):
    cells = np.random.choice(2, size=(cells_h, cells_w), p=[FLOOR_PROB, WALL_PROB])
    cells[0:cells_h, 0] = 1
    cells[0, 0:cells_w] = 1
    cells[0:cells_h, cells_w - 1] = 1
    cells[cells_h - 1, 0:cells_w] = 1

    # Blank area for player spawn
    mid_row, mid_col = len(cells) // 2, len(cells[0]) // 2
    cells[mid_row-5:mid_row+5, mid_col-5:mid_col+5] = 0

    return cells

# Generates a random map given a random seed
def generate_map(screen, cells, size):
    temp = np.zeros((cells.shape[0], cells.shape[1]))
    temp_w, temp_h = len(temp[0]), len(temp)

    for row, col in np.ndindex(cells.shape):
        walls = np.sum(cells[row - 1:row + 2, col - 1:col + 2]) - cells[row, col]   # Change values for different maps
        # color = FLOOR_COLOR if cells[row, col] == 0 else WALL_COLOR
        match cells[row, col]:
            case 0:
                color = FLOOR_COLOR
            case 1:
                color = WALL_COLOR
            case 2:
                color = TEST_COLOR

        # Rules governing wall creation
        if walls > 3:
            temp[row, col] = 1

        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    # Set borders to walls
    temp[:, 0] = 1
    temp[0, :] = 1
    temp[:, temp_w - 1] = 1
    temp[temp_h - 1, :] = 1

    # Create 5-cell wide exit points
    mid_row, mid_col = len(temp) // 2, len(temp[0]) // 2
    temp[mid_row-5:mid_row+5, 0:2] = 0
    temp[mid_row-5:mid_row+5, temp_w - 2:temp_w] = 0
    temp[0:2, mid_col-5:mid_col+5] = 0
    temp[temp_h - 2:temp_h, mid_col-5:mid_col+5] = 0

    return temp

def generate_flora(screen, cells, size):
    for row, col in np.ndindex(cells.shape):
        walls = np.sum(cells[row - 1:row + 2, col - 1:col + 2]) - cells[row, col]   # Change values for different maps

def main():
    global velocity, player_pos  # Ensure these persist across frames
    pygame.init()
    size = 10
    cells_w, cells_h = SCREEN_W // size, SCREEN_H // size

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    screen.fill(GRID_COLOR)
    cells = initialise_map(cells_w, cells_h)

    mapgen_count = 0

    # Game loop
    while True:
        screen.fill(GRID_COLOR)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                mapgen_count = 0
                cells = initialise_map(cells_w, cells_h)

        # Map generation
        if mapgen_count < mapgen_iterations:
            cells = generate_map(screen, cells, size)
            mapgen_count += 1
        else:
            # Player Movement Handling
            acceleration = pygame.Vector2(0, 0)
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                acceleration.x = -ACCELERATION
            if keys[pygame.K_d]:
                acceleration.x = ACCELERATION
            if keys[pygame.K_w]:
                acceleration.y = -ACCELERATION
            if keys[pygame.K_s]:
                acceleration.y = ACCELERATION

            # Apply acceleration to velocity
            velocity += acceleration

            # Apply friction when no keys are pressed
            if acceleration.length() == 0:
                velocity *= (1 - FRICTION)

            # Cap velocity to MAX_SPEED
            if velocity.length() > MAX_SPEED:
                velocity = velocity.normalize() * MAX_SPEED

            # Calculate new position and detect collisions
            new_pos = player_pos + velocity
            player_rect = pygame.Rect(new_pos.x, new_pos.y, player_width, player_height)
            collision_detected = detect_collision(player_rect, cells, size)

            # Bounce player off walls
            if collision_detected:
                velocity *= -0.5
            else:
                player_pos = new_pos

            # Wrap window
            if player_pos.x > SCREEN_W:
                new_pos.x = 0
                mapgen_count = 0
                cells = initialise_map(cells_w, cells_h)
            elif player_pos.x < 0:
                new_pos.x = SCREEN_W
                mapgen_count = 0
                cells = initialise_map(cells_w, cells_h)
            elif player_pos.y > SCREEN_H:
                new_pos.y = 0
                mapgen_count = 0
                cells = initialise_map(cells_w, cells_h)
            elif player_pos.y < 0:
                new_pos.y = SCREEN_H
                mapgen_count = 0
                cells = initialise_map(cells_w, cells_h)

            # Draw the map
            for row, col in np.ndindex(cells.shape):
                color = FLOOR_COLOR if cells[row, col] == 0 else WALL_COLOR
                pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

            drawPlayer(screen)

        pygame.display.flip()
        clock.tick(60)  # Cap FPS to 60

if __name__ == "__main__":
    main()
