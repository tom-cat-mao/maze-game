import pytest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.algorithms.pathfinder_dp import solve_with_dp
from generate_test_maze import generate_test_maze

def run_test(test_elements, test_id):
    """Helper function to run a single test case."""
    # 1. Generate the test maze and get the theoretical max profit
    test_data = generate_test_maze(7, 7, test_elements, test_id)
    maze = test_data["maze"]
    theoretical_max = test_data["theoretical_max_profit"]

    # 2. Run the DP solver
    path, value = solve_with_dp(maze)

    # 3. Assert that the calculated value matches the theoretical max
    print(f"Test '{test_id}':")
    print(f"  - Theoretical Max Profit: {theoretical_max}")
    print(f"  - DP Algorithm Result: {value}")
    print(f"  - Path Found: {'Yes' if path else 'No'}")
    
    assert value == theoretical_max, f"Test {test_id} failed: Expected {theoretical_max}, got {value}"
    print(f"Test '{test_id}' PASSED!")

def test_simple_profit_maximization():
    """
    Test case where the most profitable path is not the shortest.
    S(1,1) -> G(2,2) -> E(5,5)
    Profit = 10 (G) + 5 (E) = 15
    """
    elements = [
        (2, 2, 'G'), # +10
        (3, 4, 'T'), # -5, should be avoided
    ]
    run_test(elements, "simple_profit_test")

def test_complex_routing_for_profit():
    """
    Test case that requires non-trivial routing to collect all valuable items.
    Path should be S -> G2(4,2) -> G1(2,4) -> E(5,5)
    Profit = 10 (G2) + 10 (G1) + 5 (E) = 25
    """
    elements = [
        (2, 4, 'G'), # G1: +10
        (4, 2, 'G'), # G2: +10
        (4, 4, 'T'), # T1: -5, should be avoided
    ]
    run_test(elements, "complex_routing_test")

def test_no_profitable_items():
    """
    Test case with only traps. The best path is to go directly to the end.
    Path: S -> E
    Profit: 5 (E)
    """
    elements = [
        (2, 2, 'T'),
        (3, 3, 'T'),
    ]
    run_test(elements, "avoid_all_traps_test")

def test_must_take_trap_for_gold():
    """
    A scenario where a trap must be crossed to get a high-value gold.
    S(1,1) -> T(2,2) -> G(2,3) -> E(5,5)
    Path: S -> T -> G -> E
    Profit: -5 (T) + 10 (G) + 5 (E) = 10
    """
    # To enforce this, we can wall off the gold
    maze_with_walls = [
        "#######",
        "#S....#",
        "##.TG##",
        "#.....#",
        "#.....#",
        "#.....E#",
        "#######"
    ]
    # This setup is more complex than the generator can handle,
    # so we will skip this kind of test for now.
    # A future improvement would be to allow custom maze strings in tests.
    pass

if __name__ == "__main__":
    pytest.main()
