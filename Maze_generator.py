import random
import pygame

# (Bonus): add a random extra opening to create a cycle,
# then solve while marking dead ends in blue and active mouse in red.

ROWS = 20
COLS = 20
CELL_SIZE = 30
MARGIN = 40
FPS = 60

WIDTH = COLS * CELL_SIZE + MARGIN * 2
HEIGHT = ROWS * CELL_SIZE + MARGIN * 2 + 40

BG = (250, 250, 250)
WALL = (30, 30, 30)
RED = (230, 30, 30)
BLUE = (30, 100, 240)
VISITED = (233, 244, 255)
TEXT = (50, 50, 50)
START_END = (0, 150, 0)


def create_full_walls(rows: int, cols: int):
    north_wall = [[1 for _ in range(cols)] for _ in range(rows)]
    east_wall = [[1 for _ in range(cols)] for _ in range(rows)]
    return north_wall, east_wall


def neighbors(r, c):
    out = []
    if r > 0:
        out.append((r - 1, c))
    if r < ROWS - 1:
        out.append((r + 1, c))
    if c > 0:
        out.append((r, c - 1))
    if c < COLS - 1:
        out.append((r, c + 1))
    return out


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


def wall_between(north_wall, east_wall, a, b):
    ar, ac = a
    br, bc = b
    if br == ar - 1 and bc == ac:
        return north_wall[ar][ac] == 1
    if br == ar + 1 and bc == ac:
        return north_wall[br][bc] == 1
    if br == ar and bc == ac + 1:
        return east_wall[ar][ac] == 1
    if br == ar and bc == ac - 1:
        return east_wall[br][bc] == 1
    return True


def reachable_neighbors(north_wall, east_wall, r, c):
    out = []
    for nr, nc in neighbors(r, c):
        if not wall_between(north_wall, east_wall, (r, c), (nr, nc)):
            out.append((nr, nc))
    return out


def cell_xy(r, c):
    x = MARGIN + c * CELL_SIZE
    y = MARGIN + r * CELL_SIZE
    return x, y


def cell_center(r, c):
    x = MARGIN + c * CELL_SIZE + CELL_SIZE // 2
    y = MARGIN + r * CELL_SIZE + CELL_SIZE // 2
    return x, y


def draw(screen, font, north_wall, east_wall, gen_visited, start, end, mode, solver_state):
    screen.fill(BG)

    for r, c in gen_visited:
        x, y = cell_xy(r, c)
        pygame.draw.rect(screen, VISITED, (x + 2, y + 2, CELL_SIZE - 3, CELL_SIZE - 3))

    if solver_state is not None:
        dead_ends = solver_state["dead_ends"]
        path_stack = solver_state["path_stack"]
        for r, c in dead_ends:
            x, y = cell_xy(r, c)
            pygame.draw.circle(screen, BLUE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), CELL_SIZE // 6)

        for r, c in path_stack:
            x, y = cell_xy(r, c)
            pygame.draw.rect(screen, (255, 215, 160), (x + 8, y + 8, CELL_SIZE - 15, CELL_SIZE - 15))

    for r in range(ROWS):
        for c in range(COLS):
            x, y = cell_xy(r, c)
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

    sx, sy = cell_center(*start)
    ex, ey = cell_center(*end)
    pygame.draw.circle(screen, START_END, (sx, sy), CELL_SIZE // 5)
    pygame.draw.circle(screen, START_END, (ex, ey), CELL_SIZE // 5)

    if solver_state is not None and solver_state["current"] is not None:
        mx, my = cell_center(*solver_state["current"])
        pygame.draw.circle(screen, RED, (mx, my), CELL_SIZE // 4)

    text = font.render(mode, True, TEXT)
    screen.blit(text, (MARGIN, HEIGHT - 30))
    pygame.display.flip()


def random_edge_cell():
    edge = random.choice(["top", "bottom", "left", "right"])
    if edge == "top":
        return 0, random.randrange(COLS)
    if edge == "bottom":
        return ROWS - 1, random.randrange(COLS)
    if edge == "left":
        return random.randrange(ROWS), 0
    return random.randrange(ROWS), COLS - 1


def add_random_cycle(north_wall, east_wall, tries=100):
    # Remove one extra internal wall to break "shoulder-to-wall" guarantee.
    for _ in range(tries):
        r = random.randrange(ROWS)
        c = random.randrange(COLS)
        options = []
        if r > 0 and north_wall[r][c] == 1:
            options.append((r - 1, c))
        if c < COLS - 1 and east_wall[r][c] == 1:
            options.append((r, c + 1))
        if not options:
            continue
        n = random.choice(options)
        remove_wall(north_wall, east_wall, (r, c), n)
        return True
    return False


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Step 4 - Bonus cycle + solving")
    font = pygame.font.SysFont(None, 26)
    clock = pygame.time.Clock()

    north_wall, east_wall = create_full_walls(ROWS, COLS)

    # Phase 1: generate perfect maze (tree) with DFS + backtracking.
    cur = (random.randrange(ROWS), random.randrange(COLS))
    visited = {cur}
    stack = []
    generating = True

    # Solver state created after generation.
    solver = None
    start = random_edge_cell()
    end = random_edge_cell()
    while end == start:
        end = random_edge_cell()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if generating:
            unvisited = [n for n in neighbors(*cur) if n not in visited]
            if unvisited:
                nxt = random.choice(unvisited)
                stack.append(cur)
                remove_wall(north_wall, east_wall, cur, nxt)
                visited.add(nxt)
                cur = nxt
            elif stack:
                cur = stack.pop()
            else:
                generating = False
                add_random_cycle(north_wall, east_wall)
                solver = {
                    "current": start,
                    "visited": {start},
                    "path_stack": [],
                    "dead_ends": set(),
                    "finished": False,
                    "success": False,
                }

        else:
            if not solver["finished"]:
                cur = solver["current"]
                if cur == end:
                    solver["finished"] = True
                    solver["success"] = True
                else:
                    options = [
                        n
                        for n in reachable_neighbors(north_wall, east_wall, *cur)
                        if n not in solver["visited"]
                    ]
                    if options:
                        nxt = random.choice(options)
                        solver["path_stack"].append(cur)
                        solver["visited"].add(nxt)
                        solver["current"] = nxt
                    elif solver["path_stack"]:
                        solver["dead_ends"].add(cur)
                        solver["current"] = solver["path_stack"].pop()
                    else:
                        solver["dead_ends"].add(cur)
                        solver["finished"] = True
                        solver["success"] = False

        mode = "Generating maze..." if generating else "Solving maze..."
        if solver is not None and solver["finished"]:
            mode = "Solved!" if solver["success"] else "No path found"

        draw(screen, font, north_wall, east_wall, visited, start, end, mode, solver)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
