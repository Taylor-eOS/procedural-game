import tkinter as tk

GRID_SIZE = 12
CELL_SIZE = 50

def create_canvas():
    root = tk.Tk()
    root.title("Procedural Color Grid")
    canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE, bg="white")
    canvas.pack()
    return root, canvas

def draw_tile(canvas, x, y, color):
    x1 = x * CELL_SIZE
    y1 = y * CELL_SIZE
    x2 = x1 + CELL_SIZE
    y2 = y1 + CELL_SIZE
    canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

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

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

