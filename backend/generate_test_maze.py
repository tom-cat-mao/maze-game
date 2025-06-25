import sys
import os

# Add the project root to the Python path to allow imports from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.algorithms.maze_generator import generate_maze

# Generate a 15x15 maze
maze_generator = generate_maze(15, 15)

# Get the final maze state from the generator
final_maze = None
for maze_state in maze_generator:
    final_maze = maze_state

# Print the maze in a format that can be copied into the test file
print("    large_maze = [")
for row in final_maze:
    print(f'        "{''.join(row)}",')
print("    ]")
