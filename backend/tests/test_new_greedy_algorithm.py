import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.algorithms.pathfinder_greedy import solve_with_greedy

def test_new_greedy_algorithm_with_vision_and_cost_benefit():
    """
    Tests the new greedy algorithm with 3x3 vision and cost-benefit analysis.
    The test maze is designed to verify the core logic:
    1. The agent should initially move towards a high-value treasure ('G').
    2. After collecting the treasure, it should ignore a trap ('T') because its
       cost-benefit ratio is negative.
    3. With no other valuable targets, it should proceed directly to the end ('E').
    """
    maze = [
        "S.G..",
        ".#.#.",
        "..T#.",
        ".....",
        "....E"
    ]

    # Manually traced expected path and value based on the algorithm's logic:
    # 1. Start at (0,0), move towards E -> (0,1).
    # 2. At (0,1), best target is G at (0,2). Move there. Path: [(0,0),(0,1),(0,2)]. Score: 10.
    # 3. At (0,2), no valuable targets. Move towards E -> (0,3).
    # 4. At (0,3), no valuable targets. Move towards E. A* finds two paths with equal f-score.
    #    Due to tie-breaking (comparing tuples), (0,4) is chosen over (1,3). Move to (0,4).
    # 5. From (0,4), continue moving towards E until the end is reached.
    expected_path = [
        (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), 
        (1, 4), (2, 4), (3, 4), (4, 4)
    ]
    expected_value = 10  # 10 for the treasure, the trap is avoided.

    # The solve_with_greedy function now calls the new navigator
    path, value = solve_with_greedy(maze)

    # Convert path tuples to lists for comparison if necessary, but tuple comparison is fine
    assert path == expected_path
    assert value == expected_value

def test_new_greedy_avoids_trap_for_direct_path():
    """
    Tests that the agent will move through a trap if it's on the direct
    path to the only valuable item.
    """
    maze = [
        "S.T.G",
        "....."
    ]
    # 1. Start at (0,0). Vision sees 'T' at (0,2). Ratio is -5/2 = -2.5. Not valuable.
    #    Vision also sees 'G' at (0,4). Ratio is 10/4 = 2.5. Best target.
    # 2. A* to (0,4) is [(0,0),(0,1),(0,2),(0,3),(0,4)].
    # 3. Agent moves along this path.
    #    - Moves to (0,1). Path: [(0,0),(0,1)]. Score: 0.
    #    - Moves to (0,2). Path: [...,(0,2)]. Triggers trap. Score: -5.
    #    - Moves to (0,3). Path: [...,(0,3)]. Score: -5.
    #    - Moves to (0,4). Path: [...,(0,4)]. Collects treasure. Score: -5 + 10 = 5.
    # 4. At (0,4), which is 'G', but we need an 'E'. Let's adjust the maze.
    
    maze_with_end = [
        "S.T.G",
        "....E"
    ]

    # Recalculating the trace for the new maze
    # 1. Start at (0,0). Vision sees 'T' at (0,2) (ratio -2.5) and 'G' at (0,4) (ratio 2.5).
    #    Best target is 'G' at (0,4).
    # 2. A* path to (0,4) is [(0,0),(0,1),(0,2),(0,3),(0,4)].
    # 3. Agent moves along this path, triggering the trap and collecting the gold.
    #    Score becomes 5. Current position is (0,4).
    # 4. At (0,4), no valuable targets. Move towards E at (1,4).
    # 5. A* path to (1,4) is [(0,4),(1,4)]. Agent moves to (1,4).
    expected_path_2 = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4)]
    expected_value_2 = 5 # -5 for trap, +10 for gold

    path, value = solve_with_greedy(maze_with_end)

    assert path == expected_path_2
    assert value == expected_value_2
