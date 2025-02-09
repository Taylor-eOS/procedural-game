import random
import time
from tkinter_logic import GRID_SIZE, draw_tile

def get_empty_neighbors(x, y, grid):
    neighbors = []
    if x > 0 and grid[x-1][y] is None:
        neighbors.append((x-1, y))
    if x < GRID_SIZE - 1 and grid[x+1][y] is None:
        neighbors.append((x+1, y))
    if y > 0 and grid[x][y-1] is None:
        neighbors.append((x, y-1))
    if y < GRID_SIZE - 1 and grid[x][y+1] is None:
        neighbors.append((x, y+1))
    return neighbors

def get_all_empty_cells(grid):
    empty = []
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if grid[x][y] is None:
                empty.append((x, y))
    return empty

def is_valid_black(x, y, grid):
    if x > 0 and grid[x-1][y] == "black":
        return False
    if x < GRID_SIZE - 1 and grid[x+1][y] == "black":
        return False
    if y > 0 and grid[x][y-1] == "black":
        return False
    if y < GRID_SIZE - 1 and grid[x][y+1] == "black":
        return False
    return True

def choose_color(adjacent_to_blue):
    r = random.random()
    if adjacent_to_blue:
        if r < 0.9:
            return "blue"
        elif r < 0.95:
            return "#d3d3d3"  # light grey
        else:
            return "black"
    else:
        if r < 0.8:
            return "#d3d3d3"
        else:
            return "black"

def generate_population(canvas):
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    start_x = random.randint(0, GRID_SIZE - 1)
    start_y = random.randint(0, GRID_SIZE - 1)
    grid[start_x][start_y] = "blue"
    last_generated = (start_x, start_y)
    last_blue = (start_x, start_y)
    draw_tile(canvas, start_x, start_y, "blue")
    canvas.update()
    time.sleep(0.1)
    total_cells = GRID_SIZE * GRID_SIZE
    placed = 1
    while placed < total_cells:
        x, y = last_generated
        empty_neighbors = get_empty_neighbors(x, y, grid)
        if empty_neighbors:
            next_cell = random.choice(empty_neighbors)
        else:
            all_empty = get_all_empty_cells(grid)
            if not all_empty:
                break
            next_cell = random.choice(all_empty)
        nx, ny = next_cell
        adjacent_to_blue = False
        bx, by = last_blue
        if abs(nx - bx) + abs(ny - by) == 1:
            adjacent_to_blue = True
        chosen = choose_color(adjacent_to_blue)
        if chosen == "black" and not is_valid_black(nx, ny, grid):
            chosen = "#d3d3d3"
        grid[nx][ny] = chosen
        draw_tile(canvas, nx, ny, chosen)
        canvas.update()
        time.sleep(0.05)
        placed += 1
        last_generated = (nx, ny)
        if chosen == "blue":
            last_blue = (nx, ny)

