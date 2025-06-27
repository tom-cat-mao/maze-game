import sys
import os

# Add the 'backend' directory to the Python path to allow for absolute imports
# from within the application's modules.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend')))

from app.algorithms.maze_generator import Maze
from app.algorithms.puzzle_solver import solve_puzzle

def main():
    """
    Main function to generate a maze, extract a puzzle, solve it, and display results.
    """
    print("--- Step 1: Generating a new maze with a puzzle ---")
    
    # 1. Create a Maze object instance
    maze_obj = Maze(width=15, height=15)

    # 2. Generate the maze structure and ensure it has a unique path
    maze_obj.generate_maze()
    while not maze_obj.unique_path_checker():
        maze_obj.generate_maze()

    # 3. Place elements, including 'L' for Lockers (puzzles)
    maze_obj.place_elements()
    
    print("Maze generated successfully.")
    print("-" * 20)

    # --- Step 2: Extract puzzle data from the generated maze ---
    print("--- Step 2: Extracting puzzle data ---")
    
    if not maze_obj.lockers:
        print("Error: No puzzles (lockers) were found in the generated maze.")
        return

    # Get the first puzzle from the lockers dictionary
    first_locker_position = next(iter(maze_obj.lockers))
    locker_puzzle = maze_obj.lockers[first_locker_position]

    # Extract the necessary information for the solver
    original_password_list = locker_puzzle.password
    password_hash_to_solve = locker_puzzle.password_hash
    constraints = locker_puzzle.get_tips()

    print(f"Puzzle extracted from locker at position {first_locker_position}.")
    print(f"  - Original Password (for verification): {''.join(map(str, original_password_list))}")
    # print(f"  - Password Hash (for solver): {password_hash_to_solve}")
    print(f"  - Constraints/Tips: {constraints}")
    print("-" * 20)

    # --- Step 3: Call the puzzle solver and display the results ---
    print("--- Step 3: Solving the puzzle ---")
    
    # Call the solve_puzzle function with the hash and constraints
    solution, tries = solve_puzzle(password_hash_to_solve, constraints)

    print("\n--- FINAL RESULTS ---")
    print(f"The original password was: {''.join(map(str, original_password_list))}")
    
    if solution:
        solution_str = ''.join(map(str, solution))
        print(f"The solver found the solution: {solution_str}")
        print(f"Number of tries: {tries}")
        
        # Final verification
        if solution == original_password_list:
            print("Verification successful: The solution matches the original password!")
        else:
            print("Verification FAILED: The solution does not match the original password.")
    else:
        print("Solver failed: No solution was found for the given constraints.")
    print("-" * 20)

if __name__ == "__main__":
    main()
