import pytest
from app.algorithms.puzzle_solver import solve_puzzle

def test_solve_puzzle_unique_primes():
    """
    Tests the puzzle solver with constraints for a 3-digit password
    using unique prime digits (2, 3, 5, 7).
    """
    constraints = {
        "length": 3,
        "unique": True,
        "type": "prime"
    }
    # The first solution found by backtracking should be [2, 3, 5]
    expected_solution = [2, 3, 5]
    
    solution = solve_puzzle(constraints)
    
    assert solution is not None, "Solver should find a solution."
    assert solution == expected_solution

def test_solve_puzzle_unique_evens():
    """
    Tests for a 3-digit password with unique even digits.
    """
    constraints = {
        "length": 3,
        "unique": True,
        "type": "even"
    }
    # Evens are 0, 2, 4, 6, 8. First solution should be [0, 2, 4]
    expected_solution = [0, 2, 4]
    solution = solve_puzzle(constraints)
    assert solution == expected_solution

def test_solve_puzzle_no_solution():
    """
    Tests a scenario where no solution is possible.
    """
    # Primes are 2, 3, 5, 7. It's impossible to make a 5-digit password
    # with unique primes.
    constraints = {
        "length": 5,
        "unique": True,
        "type": "prime"
    }
    
    solution = solve_puzzle(constraints)
    
    assert solution is None, "Solver should return None when no solution exists."
