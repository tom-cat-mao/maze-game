import pytest
from app.algorithms.pathfinder_dp import solve_with_dp
from app.algorithms.maze_generator import generate_maze as maze_gen_algo

def test_simple_main_path():
    """Test a maze with only a direct path from S to E, with zero move cost."""
    maze = [
        "S.E",
    ]
    # Score: 0(S) + 0(.) + 0(E) = 0
    path, score = solve_with_dp(maze)
    assert score == 0
    assert path == [(0, 0), (0, 1), (0, 2)]

def test_profitable_side_branch():
    """Test a maze where exploring a side branch is profitable."""
    maze = [
        "S.E",
        "# #",
        "#G#",
    ]
    # Main path score: S(0) + .(0) + E(0) = 0.
    # Side branch at (0,1) is .(0,1) -> .(1,1) -> G(2,1).
    # Branch total score: .(0) + G(10) = 10.
    # Since 10 > 0, branch is taken.
    # Total score = 0 (main path) + 10 (branch profit) = 10.
    path, score = solve_with_dp(maze)
    assert score == 10
    # Path should be S -> . -> [excursion to G] -> E
    # Excursion: .(0,1) -> .(1,1) -> G(2,1) -> .(1,1) -> .(0,1)
    expected_path = [(0, 0), (0, 1), (1, 1), (2, 1), (1, 1), (0, 1), (0, 2)]
    assert path == expected_path


def test_unprofitable_side_branch():
    """Test a maze where exploring a side branch is not profitable."""
    maze = [
        "S.E",
        "# #",
        "#T#",
    ]
    # Main path score: S(0) + .(0) + E(0) = 0.
    # Side branch at (0,1) is .(0,1) -> .(1,1) -> T(2,1).
    # Branch total score: .(0) + T(-5) = -5.
    # Since -5 < 0, branch is not taken.
    # Total score = 0.
    path, score = solve_with_dp(maze)
    assert score == 0
    assert path == [(0, 0), (0, 1), (0, 2)]

def test_complex_maze_with_nested_branches():
    """Test a maze with nested profitable and unprofitable branches."""
    maze = [
        "#######",
        "#S.E.G#",
        "# # # #",
        "# #T# #",
        "#######"
    ]
    # Main path: S(1,1) -> .(1,2) -> E(1,3). Score = 0.
    # Branch at E(1,3): -> G(1,5). Profit = 10.
    # Branch at .(1,2): -> T(3,3). Profit = -5.
    # dp_away[G(1,5)] = 10.
    # dp_away[T(3,3)] = -5.
    # dp_to_e[E(1,3)] = score(E) + profit(G) = 0 + 10 = 10.
    # dp_to_e[.(1,2)] = score(.) + dp_to_e[E] = 0 + 10 = 10. (T branch ignored)
    # dp_to_e[S(1,1)] = score(S) + dp_to_e[.] = 0 + 10 = 10.
    path, score = solve_with_dp(maze)
    assert score == 10
    
    path_set = set(path)
    assert (1, 5) in path_set  # Should visit G
    assert (3, 3) not in path_set # Should not visit T

def test_large_generated_maze():
    """Test with a larger generated maze for robustness."""
    maze_generator = maze_gen_algo(15, 15)
    maze = None
    for maze_state in maze_generator:
        maze = maze_state
    
    assert maze is not None
    path, score = solve_with_dp(maze)

    # We can't know the exact score, but we can do logical checks.
    assert path is not None
    assert score is not None
    
    # 1. Path must be valid
    assert path[0] == (1,1) # Start position
    assert path[-1] == (13,13) # End position
    
    # 2. Path must be contiguous
    for i in range(len(path) - 1):
        r1, c1 = path[i]
        r2, c2 = path[i+1]
        assert abs(r1 - r2) + abs(c1 - c2) == 1
        
    # 3. Path should not contain walls
    for r, c in path:
        assert maze[r][c] != '#'
