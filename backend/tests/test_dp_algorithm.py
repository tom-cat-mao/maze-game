import pytest
from app.algorithms.pathfinder_dp import solve_with_dp

def test_no_special_nodes():
    """
    Tests a simple maze with no special nodes. The algorithm should
    fall back to a simple BFS and find a valid path.
    """
    maze = [
        "S.E",
    ]
    path, value = solve_with_dp(maze)
    assert path is not None
    assert len(path) > 0
    assert value == 0

def test_single_gem_path():
    """
    Tests if the algorithm correctly finds the path through the only gem.
    """
    maze = [
        "S.G.E",
    ]
    # S(0) -> G(10) -> E(0) = 10. Note: End value is not part of DP calc.
    expected_reward = 10
    path, value = solve_with_dp(maze)
    # The final value includes the end-point value if defined in the map.
    # The DP part calculates the value *up to* the final step towards E.
    # Let's adjust the test to check the core DP value.
    # The path value from S to G is 10. The path from G to E is 0. Total = 10.
    assert value == expected_reward

def test_state_compression_dp_chooses_optimal_order():
    """
    Tests if the State Compression DP algorithm correctly finds the
    optimal ORDER of visiting special nodes (Gems and Traps) to
    maximize the final reward. This is the core test for this algorithm.
    """
    # G1 at (0,2), T at (2,2), G2 at (4,2)
    # Path S->G1->G2->E should be optimal.
    # It avoids the trap 'T'.
    test_maze = [
        "S.G..", # G1
        ".#.#.",
        "..T..", # T
        ".#.#.",
        "..G.E"  # G2
    ]
    
    # Expected reward calculation:
    # Value(G1) = 10
    # Value(G2) = 10
    # Total = 20.
    # The path segments themselves have 0 value.
    expected_highest_reward = 20

    found_path, found_reward = solve_with_dp(test_maze)

    # Assert that the calculated reward is the maximum possible reward.
    assert found_reward == expected_highest_reward, \
        f"Expected reward {expected_highest_reward}, but got {found_reward}"

    # Assert that the path contains the gems and avoids the trap.
    gem1_pos = (0, 2)
    gem2_pos = (4, 2)
    trap_pos = (2, 2)
    
    found_path_tuples = {tuple(p) for p in found_path}
    assert gem1_pos in found_path_tuples, "Optimal path should visit G1"
    assert gem2_pos in found_path_tuples, "Optimal path should visit G2"
    assert trap_pos not in found_path_tuples, "Optimal path should avoid the Trap"

def test_no_path_found():
    """
    Tests if the algorithm correctly returns an empty path and zero value
    when no path from 'S' to 'E' exists.
    """
    test_maze = [
        "S#G",
        "#E#",
        "###",
    ]
    
    found_path, found_reward = solve_with_dp(test_maze)
    
    assert found_path == [], "Path should be empty when no solution exists."
    assert found_reward == 0, "Reward should be 0 when no solution exists."
