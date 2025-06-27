import random
import math
from typing import List, Dict, Any

from app.algorithms.puzzle_solver import solve_puzzle
from app.algorithms.boss_battle import solve_boss_battle
from app.algorithms.maze_generator import PasswordLock

def prepare_and_solve_puzzle(password_hash: str, constraints: List[Any]) -> tuple[List[int], int]:
    """
    Directly calls the puzzle solver with the provided hash and constraints.
    """
    # The logic for generating passwords and constraints has been moved to maze_generator.
    # This helper now simply acts as a pass-through to the core solver.
    solution, tries = solve_puzzle(password_hash, constraints)

    if not solution:
        # If the solver fails, return an empty solution and the number of tries.
        return [], tries

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
