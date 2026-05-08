# CG_Assignment
# Maze Generator (Python + Pygame)

This project visualizes how a maze is generated and solved step by step using `pygame`.
It implements the full requirements:
- Builds and displays a rectangular maze of `R x C` cells.
- Uses `north_wall[R][C]` and `east_wall[R][C]` as the core wall representation.
- Generates a **proper maze** (every cell reachable with exactly one path between cells).
- Runs a visible maze solver with:
  - a **red dot** (current mouse position),
  - a **blue path** (computed shortest solution path),
  - and animated traversal.
- Includes the **challenge addendum** mode that adds cycles by opening extra walls.

## Features

- Grid-based maze representation using two wall arrays (`north_wall` and `east_wall`)
- Maze generation using randomized DFS with backtracking
- Start/end points placed on random maze edges
- Solver visualization with:
  - Red mouse for current position
  - Blue markers for dead ends
  - Optional dead-end "eating" in final version
- Speed control, pause/resume, and regeneration controls

## Project step by step commits

- `step1 initial grid`: draws the full grid with all walls intact "!["alt text"](<Screenshots/1 initial gride setup.png>)"
- `step2 mouse movement`: moves the mouse through random neighbors while removing walls "![alt text](<Screenshots/2 mouse movement.png>)"
- `step3 backtracking`: adds DFS backtracking to fully carve the maze "![alt text](<Screenshots/3 backtracking.png>)"
- `step4 bonus cycle solver`: adds one extra opening (cycle) and visual solving, This introduces cycles and can break guaranteed shoulder-to-wall success. "![alt text](<Screenshots/4 Bonus.png>)"
- `Maze_generator.py`: polished final version with controls and full flow also a custom control panel layout "![alt text](<Screenshots/5 final maze.png>)"

## Requirements
- Python 3.9+ (recommended)
- `pygame`
Install dependency:
```bash
pip install pygame
```
## Run
Run any stage:
```bash
python Maze_generator.py
```

## Controls (Final Versions)

In `Maze_generator.py`:

- `R`: regenerate a new maze
- `UP / DOWN`: increase or decrease simulation speed
- `SPACE`: pause/resume
- `E`: toggle dead-end eating behavior during solving

## How It Works

### Data Structure
- `north_wall[r][c] == 1` means the top border of cell `(r, c)` exists.
- `east_wall[r][c] == 1` means the right border of cell `(r, c)` exists.
- A passage is created by setting the corresponding wall entry to `0`.

### Generation (Perfect Maze)
- Uses depth-first search with a stack (recursive-backtracker style):
  - Start from a random cell.
  - Repeatedly pick an unvisited neighbor and carve through the wall.
  - Backtrack when stuck.
- This produces a spanning tree over the grid (connected, no cycles).

### Running / Solving
- Chooses random edge start/end cells.
- Solves with DFS + backtracking (stack-based mouse behavior).
- Animates traversal as a red dot and marks backtracked dead ends in blue.
- Draws the final DFS-found route in orange.

### Challenge Mode (Bonus)
- After generating the perfect maze, remove extra random walls.
- This introduces cycles and can break guaranteed shoulder-to-wall success.
### brief steps
1. Start from a random cell in a fully walled grid.
2. Repeatedly move to a random unvisited neighbor and remove the wall between cells.
3. If stuck, backtrack using a stack until a branch is found.
4. After generation, optionally remove one extra wall to create a cycle.
5. Solve from random start edge to random end edge while visualizing path and dead ends.

## Notes

- The maze is randomized each run, so output is different every time.

