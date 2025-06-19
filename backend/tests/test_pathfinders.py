import pytest
from app.algorithms.pathfinder_dp import solve_with_dp
from app.algorithms.pathfinder_greedy import solve_with_greedy

def test_pathfinders_on_cyclic_maze():
    """
    Tests that both algorithms return a valid path on a cyclic maze.
    """
    trap_maze = [
        ['S', '.', '.', '.', 'E'],
        ['#', '#', '#', '.', '#'],
        ['G', '.', '.', '.', '.'],
    ]
    
    greedy_path, greedy_value = solve_with_greedy(trap_maze)
    dp_path, dp_value = solve_with_dp(trap_maze)

    assert len(greedy_path) > 0
    assert len(dp_path) > 0

def test_greedy_can_escape_trap_with_backtracking():
    """
    Tests that the new Greedy algorithm can backtrack out of a dead end.
    """
    trap_maze = [
        ['S', '.', '#', 'E'],
        ['.', '.', '.', '.'],
        ['#', '#', '#', '#'],
    ]
    
    greedy_path, greedy_value = solve_with_greedy(trap_maze)
    
    assert len(greedy_path) > 0, "Greedy algorithm should find a path."
    assert tuple(greedy_path[-1]) == (0, 3), "Greedy algorithm should reach the end."
