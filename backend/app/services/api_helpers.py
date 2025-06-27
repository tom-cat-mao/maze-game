import random
import math
from typing import List, Dict, Any

from app.algorithms.puzzle_solver import solve_puzzle
from app.algorithms.boss_battle import solve_boss_battle

def prepare_and_solve_puzzle(high_level_constraints: Dict[str, Any]) -> List[int]:
    """
    Generates a target password and low-level constraints based on high-level rules,
    then calls the puzzle solver.
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

    # --- Translate high-level constraints to low-level for the algorithm ---
    low_level_constraints = []
    if is_unique and puzzle_type == "prime":
        low_level_constraints.append([-1, -1])

    # Call the algorithm
    solution, _ = solve_puzzle(password_str, low_level_constraints)

    if not solution:
        # Fallback to the generated password if solver fails
        return password_digits

    return solution

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
