
                color = FLOOR_COLOR if cells[row, col] == 0 else WALL_COLOR
                pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))