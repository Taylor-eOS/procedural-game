import random
import time
from tkinter_logic import GRID_SIZE, draw_tile, get_empty_neighbors, get_all_empty_cells

# Rule configuration with clear names
COLOR_RULES = {
    "black": {
        "placement_restriction": {
            "rule_type": "no_neighbors_in_radius",
            "radius": 2,
            "color": "black"
        }
    },
    "blue": {
        "activation_requirement": {"must_be_adjacent_to_blue": True},
        "probability_cases": [
            {
                "condition": {
                    "type": "exact_count", 
                    "color": "blue",
                    "count": 1
                },
                "outcomes": [
                    {"probability": 0.9, "color": "blue"},
                    {"probability": 0.95, "color": "#d3d3d3"},
                    {"color": "black"}
                ]
            },
            {
                "condition": {
                    "type": "exact_count", 
                    "color": "blue",
                    "count": 2
                },
                "outcomes": [
                    {"probability": 0.1, "color": "blue"},
                    {"probability": 0.9, "color": "#d3d3d3"},
                    {"color": "black"}
                ]
            },
            {
                "condition": {
                    "type": "minimum_count", 
                    "color": "blue",
                    "count": 3
                },
                "outcomes": [
                    {"probability": 0.05, "color": "blue"},
                    {"probability": 0.95, "color": "#d3d3d3"},
                    {"color": "black"}
                ]
            }
        ]
    },
    "grey": {
        "probability_cases": [
            {
                "condition": {"type": "always_true"},
                "outcomes": [
                    {"probability": 0.8, "color": "#d3d3d3"},
                    {"color": "black"}
                ]
            }
        ]
    }
}

CONDITION_HANDLERS = {
    "exact_count": lambda grid, x, y, color, count: 
        count_adjacent_colors(grid, x, y, color) == count,
    "minimum_count": lambda grid, x, y, color, count: 
        count_adjacent_colors(grid, x, y, color) >= count,
    "no_neighbors_in_radius": lambda grid, x, y, color, radius: 
        not has_color_in_radius(grid, x, y, color, radius),
    "always_true": lambda *_: True
}

def count_adjacent_colors(grid, x, y, color):
    return sum(
        1 for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]
        if 0 <= x+dx < GRID_SIZE 
        and 0 <= y+dy < GRID_SIZE 
        and grid[x+dx][y+dy] == color
    )

def has_color_in_radius(grid, x, y, color, radius):
    for dx in range(-radius, radius+1):
        for dy in range(-radius, radius+1):
            if (dx != 0 or dy != 0) and 0 <= x+dx < GRID_SIZE and 0 <= y+dy < GRID_SIZE:
                if grid[x+dx][y+dy] == color:
                    return True
    return False

def get_growth_point(grid, last_generated):
    x, y = last_generated
    empty_neighbors = get_empty_neighbors(x, y, grid)
    if empty_neighbors:
        return random.choice(empty_neighbors)
    
    all_empty = get_all_empty_cells(grid)
    if all_empty:
        return random.choice(all_empty)
    
    return (x, y)  # Fallback to current position if all else fails

def determine_color(x, y, grid, context):
    rule_set = "blue" if context["adjacent_to_blue"] else "grey"
    
    for case in COLOR_RULES[rule_set].get("probability_cases", []):
        condition = case["condition"]
        handler = CONDITION_HANDLERS[condition["type"]]
        
        # Extract only the arguments the handler needs
        handler_args = {
            "grid": grid,
            "x": x,
            "y": y,
            "color": condition.get("color"),
            "count": condition.get("count", 0),
            "radius": condition.get("radius", 0)
        }
        
        # Filter arguments to match the handler's expected parameters
        if condition["type"] == "exact_count":
            args = (handler_args["grid"], handler_args["x"], handler_args["y"], 
                    handler_args["color"], handler_args["count"])
        elif condition["type"] == "minimum_count":
            args = (handler_args["grid"], handler_args["x"], handler_args["y"], 
                    handler_args["color"], handler_args["count"])
        elif condition["type"] == "no_neighbors_in_radius":
            args = (handler_args["grid"], handler_args["x"], handler_args["y"], 
                    handler_args["color"], handler_args["radius"])
        elif condition["type"] == "always_true":
            args = ()
        
        if handler(*args):
            return select_outcome(case["outcomes"])
    
    return "#d3d3d3"  # Default fallback

def select_outcome(outcomes):
    rand = random.random()
    threshold = 0
    for outcome in outcomes:
        if "probability" in outcome:
            if rand < (threshold + outcome["probability"]):
                return outcome["color"]
            threshold += outcome["probability"]
        else:
            return outcome["color"]
    return "black"

def generate_population(canvas):
    grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    start_x, start_y = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
    grid[start_x][start_y] = "blue"
    last_generated = (start_x, start_y)
    last_blue = (start_x, start_y)
    
    draw_tile(canvas, start_x, start_y, "blue")
    canvas.update()
    time.sleep(0.05)
    
    total_cells = GRID_SIZE * GRID_SIZE
    placed = 1
    
    while placed < total_cells:
        # Get next growth point using fixed logic
        next_x, next_y = get_growth_point(grid, last_generated)
        
        # Check adjacency to blue cells
        adjacent_to_blue = any(
            0 <= next_x+dx < GRID_SIZE and 0 <= next_y+dy < GRID_SIZE
            and grid[next_x+dx][next_y+dy] == "blue"
            for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]
        )
        
        # Determine color using rules
        context = {"adjacent_to_blue": adjacent_to_blue}
        chosen_color = determine_color(next_x, next_y, grid, context)
        
        # Validate black placement
        if chosen_color == "black":
            restriction = COLOR_RULES["black"]["placement_restriction"]
            handler = CONDITION_HANDLERS[restriction["rule_type"]]
            args = (grid, next_x, next_y, restriction["color"], restriction["radius"])
            if not handler(*args):
                chosen_color = "#d3d3d3"
        
        # Update grid and display
        grid[next_x][next_y] = chosen_color
        draw_tile(canvas, next_x, next_y, chosen_color)
        
        if chosen_color == "blue":
            last_blue = (next_x, next_y)
        
        last_generated = (next_x, next_y)
        placed += 1
        canvas.update()
        time.sleep(0.05)
