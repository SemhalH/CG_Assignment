import random
import pygame

# Added backtracking
# Proper maze generation using DFS + stack:
# 1) move to random unvisited neighbor
# 2) push current cell onto stack
# 3) dead-end => pop stack
# 4) done when stack empty and all visited

ROWS = 20
COLS = 20
CELL_SIZE = 30
MARGIN = 40
FPS = 30

WIDTH = COLS * CELL_SIZE + MARGIN * 2
HEIGHT = ROWS * CELL_SIZE + MARGIN * 2

BG = (250, 250, 250)
WALL = (30, 30, 30)
MOUSE = (220, 40, 40)
VISITED = (230, 242, 255)
STACK_CLR = (255, 220, 170)


def create_full_walls(rows: int, cols: int):
    north_wall = [[1 for _ in range(cols)] for _ in range(rows)]
    east_wall = [[1 for _ in range(cols)] for _ in range(rows)]
    return north_wall, east_wall


def neighbors(r, c):
    items = []
    if r > 0:
        items.append((r - 1, c))
    if r < ROWS - 1:
        items.append((r + 1, c))
    if c > 0:
        items.append((r, c - 1))
    if c < COLS - 1:
        items.append((r, c + 1))
    return items


def remove_wall(north_wall, east_wall, a, b):
    ar, ac = a
    br, bc = b
    if br == ar - 1 and bc == ac:
        north_wall[ar][ac] = 0
    elif br == ar + 1 and bc == ac:
        north_wall[br][bc] = 0
    elif br == ar and bc == ac + 1:
        east_wall[ar][ac] = 0
    elif br == ar and bc == ac - 1:
        east_wall[br][bc] = 0


def cell_rect(r, c, pad=2):
    x = MARGIN + c * CELL_SIZE + pad
    y = MARGIN + r * CELL_SIZE + pad
    return x, y, CELL_SIZE - (pad + 1), CELL_SIZE - (pad + 1)


def cell_center(r, c):
    x = MARGIN + c * CELL_SIZE + CELL_SIZE // 2
    y = MARGIN + r * CELL_SIZE + CELL_SIZE // 2
    return x, y


def draw(screen, north_wall, east_wall, visited, stack, current, finished):
    screen.fill(BG)

    for r, c in visited:
        pygame.draw.rect(screen, VISITED, cell_rect(r, c, 2))

    for r, c in stack:
        pygame.draw.rect(screen, STACK_CLR, cell_rect(r, c, 6))

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

    if not finished:
        mx, my = cell_center(*current)
        pygame.draw.circle(screen, MOUSE, (mx, my), CELL_SIZE // 4)

    pygame.display.flip()


def generate_step(north_wall, east_wall, visited, stack, current):
    unvisited = [n for n in neighbors(*current) if n not in visited]
    if unvisited:
        nxt = random.choice(unvisited)
        stack.append(current)
        remove_wall(north_wall, east_wall, current, nxt)
        visited.add(nxt)
        return nxt, False

    if stack:
        return stack.pop(), False

    return current, True


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Step 3 - Added backtracking")
    clock = pygame.time.Clock()

    north_wall, east_wall = create_full_walls(ROWS, COLS)
    current = (random.randrange(ROWS), random.randrange(COLS))
    visited = {current}
    stack = []
    finished = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not finished:
            current, finished = generate_step(north_wall, east_wall, visited, stack, current)

        draw(screen, north_wall, east_wall, visited, stack, current, finished)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
