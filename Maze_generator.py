import random
import pygame

# Final code:
# - Generates a perfect maze using DFS + stack backtracking
# - Opens entry and exit on random edges
# - Solves with red mouse, marks dead-end cells in blue
# - Bonus: removes one extra wall to create a cycle

ROWS = 15  # Reduced from 20
COLS = 15  # Reduced from 20
CELL_SIZE = 25  # Reduced from 30
MARGIN = 30  # Reduced from 40
FPS = 60

# Calculate new dimensions
WIDTH = COLS * CELL_SIZE + MARGIN * 2
HEIGHT = ROWS * CELL_SIZE + MARGIN * 2 + 100  # Slightly smaller control panel area

BG = (250, 250, 250)
WALL = (32, 32, 32)
VISITED = (235, 245, 255)
PATH_HINT = (255, 221, 170)
RED = (224, 40, 40)
BLUE = (40, 110, 235)
GREEN = (0, 155, 0)
TEXT = (55, 55, 55)
YELLOW = (255, 255, 100)


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


def add_wall(north_wall, east_wall, a, b):
    ar, ac = a
    br, bc = b
    if br == ar - 1 and bc == ac:
        north_wall[ar][ac] = 1
    elif br == ar + 1 and bc == ac:
        north_wall[br][bc] = 1
    elif br == ar and bc == ac + 1:
        east_wall[ar][ac] = 1
    elif br == ar and bc == ac - 1:
        east_wall[br][bc] = 1


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


def random_edge_cell():
    edge = random.choice(("top", "bottom", "left", "right"))
    if edge == "top":
        return 0, random.randrange(COLS)
    if edge == "bottom":
        return ROWS - 1, random.randrange(COLS)
    if edge == "left":
        return random.randrange(ROWS), 0
    return random.randrange(ROWS), COLS - 1


def carve_opening_on_edge(north_wall, east_wall, cell):
    r, c = cell
    if r == 0:
        north_wall[r][c] = 0
    elif c == COLS - 1:
        east_wall[r][c] = 0
    elif r == ROWS - 1:
        north_wall[r][c] = 0
    elif c == 0:
        # Left boundary not directly represented by arrays; opening is visual/logical marker.
        pass


def add_random_cycle(north_wall, east_wall, tries=120):
    for _ in range(tries):
        r = random.randrange(ROWS)
        c = random.randrange(COLS)
        candidates = []
        if r > 0 and north_wall[r][c] == 1:
            candidates.append((r - 1, c))
        if c < COLS - 1 and east_wall[r][c] == 1:
            candidates.append((r, c + 1))
        if not candidates:
            continue
        remove_wall(north_wall, east_wall, (r, c), random.choice(candidates))
        return True
    return False


def cell_xy(r, c):
    return MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE


def cell_center(r, c):
    x, y = cell_xy(r, c)
    return x + CELL_SIZE // 2, y + CELL_SIZE // 2


def draw_control_panel(screen, font, small_font, sim_speed, paused, eat_dead_ends, solving_phase):
    panel_y = HEIGHT - 90
    panel_height = 85
    pygame.draw.rect(screen, (240, 240, 240), (0, panel_y, WIDTH, panel_height))
    pygame.draw.line(screen, WALL, (0, panel_y), (WIDTH, panel_y), 2)
    
    # Title
    title = small_font.render("CONTROLS:", True, TEXT)
    screen.blit(title, (MARGIN, panel_y + 5))
    
    # Control buttons in a grid
    controls = [
        ("R", "Regenerate", 0),
        ("↑/↓", f"Speed: {sim_speed}x", 1),
        ("E", f"Eat: {'ON' if eat_dead_ends else 'OFF'}", 2),
        ("SPACE", "Pause", 3),
    ]
    
    for key, desc, col in controls:
        x = MARGIN + (col * 150)
        # Draw key button
        key_bg = pygame.Rect(x, panel_y + 22, 45, 20)
        pygame.draw.rect(screen, YELLOW, key_bg)
        pygame.draw.rect(screen, TEXT, key_bg, 1)
        key_text = small_font.render(key, True, TEXT)
        screen.blit(key_text, (x + 12, panel_y + 24))
        
        # Draw description
        desc_text = small_font.render(desc, True, TEXT)
        screen.blit(desc_text, (x + 52, panel_y + 24))
    
    # Status indicators
    status_x = MARGIN
    status_y = panel_y + 50
    phase_text = "SOLVING" if solving_phase else "GENERATING"
    status_text = small_font.render(f"{'⏸ PAUSED' if paused else '▶ RUNNING'}  |  {phase_text}  |  SPEED: {sim_speed}x  |  DEAD-ENDS: {'EATEN' if eat_dead_ends else 'KEPT'}", True, TEXT)
    screen.blit(status_text, (status_x, status_y))


def draw(screen, font, small_font, north_wall, east_wall, generated, start, end, solver, message, sim_speed, paused, eat_dead_ends, generation_done):
    screen.fill(BG)

    for r, c in generated:
        x, y = cell_xy(r, c)
        pygame.draw.rect(screen, VISITED, (x + 2, y + 2, CELL_SIZE - 3, CELL_SIZE - 3))

    if solver is not None:
        for r, c in solver["path_stack"]:
            x, y = cell_xy(r, c)
            pygame.draw.rect(screen, PATH_HINT, (x + 6, y + 6, CELL_SIZE - 12, CELL_SIZE - 12))
        for r, c in solver["dead_ends"]:
            cx, cy = cell_center(r, c)
            pygame.draw.circle(screen, BLUE, (cx, cy), CELL_SIZE // 7)

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
    pygame.draw.circle(screen, GREEN, (sx, sy), CELL_SIZE // 5)
    pygame.draw.circle(screen, GREEN, (ex, ey), CELL_SIZE // 5)

    if solver is not None and solver["current"] is not None:
        mx, my = cell_center(*solver["current"])
        pygame.draw.circle(screen, RED, (mx, my), CELL_SIZE // 5)

    # Message area
    msg_y = MARGIN + ROWS * CELL_SIZE + 8
    text = font.render(message, True, TEXT)
    screen.blit(text, (MARGIN, msg_y))
    
    # Draw control panel
    draw_control_panel(screen, font, small_font, sim_speed, paused, eat_dead_ends, generation_done)
    
    pygame.display.flip()


def init_run_state():
    north_wall, east_wall = create_full_walls(ROWS, COLS)
    cur = (random.randrange(ROWS), random.randrange(COLS))
    generated = {cur}
    backtrack = []
    generation_done = False
    start = random_edge_cell()
    end = random_edge_cell()
    while end == start:
        end = random_edge_cell()
    solver = None
    info = "GENERATING maze... (Press SPACE to pause)"
    return north_wall, east_wall, cur, generated, backtrack, generation_done, start, end, solver, info


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Generator + Solver with Controls")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)  # Slightly smaller font
    small_font = pygame.font.SysFont(None, 18)

    (
        north_wall,
        east_wall,
        cur,
        generated,
        backtrack,
        generation_done,
        start,
        end,
        solver,
        info,
    ) = init_run_state()

    sim_speed = 1  # Slow default speed
    paused = False
    eat_dead_ends = True
    
    # Add a frame counter to slow down solving even more
    frame_counter = 0
    solve_step_delay = 0  # 0 = no extra delay

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    (
                        north_wall,
                        east_wall,
                        cur,
                        generated,
                        backtrack,
                        generation_done,
                        start,
                        end,
                        solver,
                        info,
                    ) = init_run_state()
                    frame_counter = 0
                elif event.key == pygame.K_UP:
                    sim_speed = min(8, sim_speed + 1)  # Max speed 8x
                elif event.key == pygame.K_DOWN:
                    sim_speed = max(1, sim_speed - 1)
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_e:
                    eat_dead_ends = not eat_dead_ends

        if not paused:
            # For solving phase, we want slower movement - using frame-based delay
            if generation_done and solver and not solver["finished"]:
                # Slower solving: only move every 2-3 frames for better visibility
                frame_counter += 1
                if frame_counter >= 3:  # Solve every 3 frames (about 20 moves per second)
                    frame_counter = 0
                    # Only do one solving step per frame cycle
                    solve_step = True
                else:
                    solve_step = False
            else:
                # Generation phase or finished solving - normal speed
                solve_step = True
            
            if solve_step or not generation_done:
                for _ in range(sim_speed):
                    if not generation_done:
                        unvisited = [n for n in neighbors(*cur) if n not in generated]
                        if unvisited:
                            nxt = random.choice(unvisited)
                            backtrack.append(cur)
                            remove_wall(north_wall, east_wall, cur, nxt)
                            generated.add(nxt)
                            cur = nxt
                        elif backtrack:
                            cur = backtrack.pop()
                        else:
                            generation_done = True
                            add_random_cycle(north_wall, east_wall)  # Bonus
                            carve_opening_on_edge(north_wall, east_wall, start)
                            carve_opening_on_edge(north_wall, east_wall, end)
                            solver = {
                                "current": start,
                                "visited": {start},
                                "path_stack": [],
                                "dead_ends": set(),
                                "finished": False,
                                "success": False,
                            }
                            info = "SOLVING maze... (Red mouse is exploring)"
                            frame_counter = 0  # Reset frame counter for solving phase
                    else:
                        if not solver["finished"]:
                            current = solver["current"]
                            if current == end:
                                solver["finished"] = True
                                solver["success"] = True
                                info = "SOLVED! Press R for new maze"
                            else:
                                next_cells = [
                                    n
                                    for n in reachable_neighbors(north_wall, east_wall, *current)
                                    if n not in solver["visited"]
                                ]
                                if next_cells:
                                    nxt = random.choice(next_cells)
                                    solver["path_stack"].append(current)
                                    solver["visited"].add(nxt)
                                    solver["current"] = nxt
                                elif solver["path_stack"]:
                                    solver["dead_ends"].add(current)
                                    parent = solver["path_stack"].pop()
                                    # "Eat dead-end": close the branch so it won't be retried.
                                    if eat_dead_ends:
                                        add_wall(north_wall, east_wall, current, parent)
                                    solver["current"] = parent
                                else:
                                    solver["dead_ends"].add(current)
                                    solver["finished"] = True
                                    solver["success"] = False
                                    info = "✗ No path found! Press R for new maze"

        state_prefix = "⏸ " if paused else "▶ "
        draw(
            screen,
            font,
            small_font,
            north_wall,
            east_wall,
            generated,
            start,
            end,
            solver,
            state_prefix + info,
            sim_speed,
            paused,
            eat_dead_ends,
            generation_done,
        )
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()