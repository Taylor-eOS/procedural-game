import tkinter as tk

GRID_SIZE = 10
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

