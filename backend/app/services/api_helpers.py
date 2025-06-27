import random
import math
from typing import List, Dict, Any

from app.algorithms.puzzle_solver import solve_puzzle
from app.algorithms.boss_battle import solve_boss_battle
from app.algorithms.maze_generator import PasswordLock

def prepare_and_solve_puzzle(high_level_constraints: Dict[str, Any]) -> tuple[List[int], int]:
    """
    Generates a target password and low-level constraints based on high-level rules,
    then calls the puzzle solver and returns both the solution and the number of tries.
    """
    puzzle_len = high_level_constraints.get("length", 3)
    puzzle_type = high_level_constraints.get("type")
    is_unique = high_level_constraints.get("unique", False)

    # --- Generate a target password that fits the constraints ---
    password_digits = []
    if puzzle_type == "prime":
        options = [2, 3, 5, 7]
    elif puzzle_type == "even":
        options = [0, 2, 4, 6, 8]
    elif puzzle_type == "odd":
        options = [1, 3, 5, 7, 9]
    else:
        options = list(range(10))

    if is_unique:
        if len(options) < puzzle_len:
            # Not enough unique numbers for the requested length
            raise ValueError("Not enough unique numbers for puzzle length")
        password_digits = random.sample(options, puzzle_len)
    else:
        password_digits = [random.choice(options) for _ in range(puzzle_len)]
    
    password_str = "".join(map(str, password_digits))
    
    # Hash the password before sending it to the solver
    password_locker = PasswordLock()
    password_hash = password_locker.hash_password(password_str)

    # --- Translate high-level constraints to low-level for the algorithm ---
    low_level_constraints = []
    
    # Add constraint for prime numbers
    if puzzle_type == "prime":
        # This implies all digits are unique and prime
        low_level_constraints.append([-1, -1])

    # Add constraints for even/odd properties
    for i, digit in enumerate(password_digits):
        is_even = digit % 2 == 0
        if puzzle_type == "even" and is_even:
            low_level_constraints.append([i + 1, 0]) # pos is 1-based
        elif puzzle_type == "odd" and not is_even:
            low_level_constraints.append([i + 1, 1]) # pos is 1-based

    # Add one random "digit reveal" constraint to make it more interesting
    if password_digits:
        revealed_idx = random.randint(0, len(password_digits) - 1)
        mask = [-1] * len(password_digits)
        mask[revealed_idx] = password_digits[revealed_idx]
        low_level_constraints.append(mask)

    # Call the algorithm with the hashed password
    solution, tries = solve_puzzle(password_hash, low_level_constraints)

    if not solution:
        # Fallback to the generated password if solver fails, with 0 tries
        return password_digits, 0

    return solution, tries

def prepare_and_solve_boss_battle(boss_hps: List[int], skills: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Adapts the request data for the boss battle algorithm, calls the solver,
    and adapts the response data for the frontend.
    """
    # 1. Adapt the input data structure
    skills_list = [[s['damage'], s['cooldown']] for s in skills]
    skill_names = [s['name'] for s in skills]

    # 2. Call the algorithm
    min_time, path = solve_boss_battle(boss_hps, skills_list)

    if not path:
        return None

    # 3. Adapt the output data structure
    sequence = [skill_names[skill_idx] for _, skill_idx in path]
    turns = math.ceil(min_time)

    return {"sequence": sequence, "turns": turns}
