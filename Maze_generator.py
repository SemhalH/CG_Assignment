import pygame

# Initial grid setup
# Displays a rectangular maze grid with all walls intact.

ROWS = 20
COLS = 20
CELL_SIZE = 30
MARGIN = 40

WIDTH = COLS * CELL_SIZE + MARGIN * 2
HEIGHT = ROWS * CELL_SIZE + MARGIN * 2

BG = (250, 250, 250)
WALL = (20, 20, 20)


def create_full_walls(rows: int, cols: int):
    # north_wall[r][c] == 1 means top wall of cell (r, c) exists.
    # east_wall[r][c] == 1 means right wall of cell (r, c) exists.
    north_wall = [[1 for _ in range(cols)] for _ in range(rows)]
    east_wall = [[1 for _ in range(cols)] for _ in range(rows)]
    return north_wall, east_wall


def draw_maze(screen, north_wall, east_wall):
    screen.fill(BG)

    # Draw top and right walls per cell from the required data structure.
    for r in range(ROWS):
        for c in range(COLS):
            x = MARGIN + c * CELL_SIZE
            y = MARGIN + r * CELL_SIZE

            if north_wall[r][c]:
                pygame.draw.line(screen, WALL, (x, y), (x + CELL_SIZE, y), 2)
            if east_wall[r][c]:
                pygame.draw.line(
                    screen,
                    WALL,
                    (x + CELL_SIZE, y),
                    (x + CELL_SIZE, y + CELL_SIZE),
                    2,
                )

    # Draw left and bottom boundary to close the grid.
    pygame.draw.line(screen, WALL, (MARGIN, MARGIN), (MARGIN, MARGIN + ROWS * CELL_SIZE), 2)
    pygame.draw.line(
        screen,
        WALL,
        (MARGIN, MARGIN + ROWS * CELL_SIZE),
        (MARGIN + COLS * CELL_SIZE, MARGIN + ROWS * CELL_SIZE),
        2,
    )

    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Step 1 - Initial grid setup")
    clock = pygame.time.Clock()

    north_wall, east_wall = create_full_walls(ROWS, COLS)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_maze(screen, north_wall, east_wall)
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
