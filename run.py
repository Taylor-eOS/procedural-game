import tkinter as tk
from tkinter_logic import create_canvas
from population_rules import generate_population

def main():
    root, canvas = create_canvas()
    redo_button = tk.Button(root, text="Redo", command=lambda: redo(canvas))
    redo_button.pack()
    generate_population(canvas)
    root.mainloop()

def redo(canvas):
    canvas.delete("all")
    generate_population(canvas)

if __name__ == "__main__":
    main()

