import random
import time
from tkinter_logic import GRID_SIZE, draw_tile, get_empty_neighbors, get_all_empty_cells

SLEEP = 0.025

def determine_color(x, y, grid, adjacent_to_blue):
    blue_neighbors = count_adjacent_colors(grid, x, y, "blue")
    if adjacent_to_blue:
        if blue_neighbors == 1:
            if r(0.8): return "blue"
            elif r(0.95): return "snow"
            else: return "black"
        elif blue_neighbors == 2:
            if cells_of_color(grid, "blue") < 10:
                if r(0.1): return "blue"
                else: return "snow"
            else:
                if r(0.5): return "snow"
                else: return "blue"
        else: return "snow"
    else:
        if cells_of_color(grid, "yellow") == 0 and blue_neighbors == 0:
            if r(0.8): return "yellow"

        #elif not has_color_in_radius(grid, x, y, "blue", 2) and cells_of_color(grid, "blue") < 6:
        #        if r(0.2): return "blue"

        if has_color_in_radius(grid, x, y, "black", 1):
            if cells_of_color(grid, "black") < 4:
                if r(0.05): return "black"
                else: return "snow"
        elif has_color_in_radius(grid, x, y, "black", 2):
            if r(0.15): return "black"
            else: return "snow"
        else:
            if cells_of_color(grid, "black") > 3:
                if r(0.2): return "black"
                else: return "snow"
            else:
                if r(0.5): return "black"
                else: return "snow"
    return "snow"

def r(value):
    return random.random() < value

def count_adjacent_colors(grid, x, y, color):
    count = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[nx][ny] == color:
            count += 1
    return count

def has_color_in_radius(grid, x, y, color, radius):
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if grid[nx][ny] == color:
                    return True
    return False

def get_growth_point(grid, last_generated, search_radius=4):
    x, y = last_generated
    empty_neighbors = get_empty_neighbors(x, y, grid)
    if empty_neighbors:
        return random.choice(empty_neighbors)
    cells_in_radius = []
    for dx in range(-search_radius, search_radius + 1):
        for dy in range(-search_radius, search_radius + 1):
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                if grid[nx][ny] is None:
                    cells_in_radius.append((nx, ny))
    if cells_in_radius:
        return random.choice(cells_in_radius)
    all_empty = get_all_empty_cells(grid)
    if all_empty:
        return random.choice(all_empty)
    return (x, y)

def generate_population(canvas):
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    start_x = random.randint(0, GRID_SIZE - 1)
    start_y = random.randint(0, GRID_SIZE - 1)
    grid[start_x][start_y] = "blue"
    last_generated = (start_x, start_y)
    draw_tile(canvas, start_x, start_y, "blue")
    canvas.update()
    time.sleep(SLEEP)
    total_cells = GRID_SIZE * GRID_SIZE
    placed = 1
    while placed < total_cells:
        next_x, next_y = get_growth_point(grid, last_generated)
        adjacent_to_blue = False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = next_x + dx, next_y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[nx][ny] == "blue":
                adjacent_to_blue = True
                break
        color_choice = determine_color(next_x, next_y, grid, adjacent_to_blue)
        #print(f"({next_x},{next_y}) {color_choice}")
        #print(f"({grid}")
        grid[next_x][next_y] = color_choice
        draw_tile(canvas, next_x, next_y, color_choice)
        last_generated = (next_x, next_y)
        placed += 1
        canvas.update()
        time.sleep(SLEEP)

def cells_of_color(grid, color):
    return sum(row.count(color) for row in grid)

