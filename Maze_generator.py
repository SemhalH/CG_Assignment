import random
import pygame

# Implemented mouse movement
# Mouse moves through adjacent cells and eats connecting walls.
# This version focuses on movement + wall removal visualization.

ROWS = 20
COLS = 20
CELL_SIZE = 30
MARGIN = 40

WIDTH = COLS * CELL_SIZE + MARGIN * 2
HEIGHT = ROWS * CELL_SIZE + MARGIN * 2

BG = (248, 248, 248)
WALL = (25, 25, 25)
MOUSE = (220, 40, 40)
VISITED = (210, 230, 255)


def create_full_walls(rows: int, cols: int):
    north_wall = [[1 for _ in range(cols)] for _ in range(rows)]
    east_wall = [[1 for _ in range(cols)] for _ in range(rows)]
    return north_wall, east_wall


def cell_center(r, c):
    x = MARGIN + c * CELL_SIZE + CELL_SIZE // 2
    y = MARGIN + r * CELL_SIZE + CELL_SIZE // 2
    return x, y


def draw_maze(screen, north_wall, east_wall, visited, mouse):
    screen.fill(BG)

    for (r, c) in visited:
        x = MARGIN + c * CELL_SIZE + 2
        y = MARGIN + r * CELL_SIZE + 2
        pygame.draw.rect(screen, VISITED, (x, y, CELL_SIZE - 3, CELL_SIZE - 3))

    for r in range(ROWS):
        for c in range(COLS):
            x = MARGIN + c * CELL_SIZE
            y = MARGIN + r * CELL_SIZE
            if north_wall[r][c]:
                pygame.draw.line(screen, WALL, (x, y), (x + CELL_SIZE, y), 2)
            if east_wall[r][c]:
                pygame.draw.line(screen, WALL, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)

    pygame.draw.line(screen, WALL, (MARGIN, MARGIN), (MARGIN, MARGIN + ROWS * CELL_SIZE), 2)
    pygame.draw.line(
        screen,
        WALL,
        (MARGIN, MARGIN + ROWS * CELL_SIZE),
        (MARGIN + COLS * CELL_SIZE, MARGIN + ROWS * CELL_SIZE),
        2,
    )

    mx, my = cell_center(*mouse)
    pygame.draw.circle(screen, MOUSE, (mx, my), CELL_SIZE // 4)

    pygame.display.flip()


def neighbors(r, c):
    cand = []
    if r > 0:
        cand.append((r - 1, c))
    if r < ROWS - 1:
        cand.append((r + 1, c))
    if c > 0:
        cand.append((r, c - 1))
    if c < COLS - 1:
        cand.append((r, c + 1))
    return cand


def remove_wall(north_wall, east_wall, a, b):
    ar, ac = a
    br, bc = b
    if br == ar - 1 and bc == ac:  # b is above a
        north_wall[ar][ac] = 0
    elif br == ar + 1 and bc == ac:  # b is below a
        north_wall[br][bc] = 0
    elif br == ar and bc == ac + 1:  # b is right of a
        east_wall[ar][ac] = 0
    elif br == ar and bc == ac - 1:  # b is left of a
        east_wall[br][bc] = 0


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Step 2 - Implemented mouse movement")
    clock = pygame.time.Clock()

    north_wall, east_wall = create_full_walls(ROWS, COLS)
    current = (random.randrange(ROWS), random.randrange(COLS))
    visited = {current}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Mouse picks a random unvisited neighbor when possible.
        unvisited = [n for n in neighbors(*current) if n not in visited]
        if unvisited:
            nxt = random.choice(unvisited)
            remove_wall(north_wall, east_wall, current, nxt)
            current = nxt
            visited.add(current)

        draw_maze(screen, north_wall, east_wall, visited, current)
        clock.tick(20)

    pygame.quit()


if __name__ == "__main__":
    main()
