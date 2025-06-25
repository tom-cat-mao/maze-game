def solve_puzzle(password, constraints):
    """
    Inputs: password: list of three digits representing the password. (Used for verification in tests).
            constraints: List of constraints for the puzzle.
                e.g. [[-1, -1], [pos, 0], [pos, 1], [digit, -1, -1], [-1, digit, -1], [-1, -1, digit]]
    Outputs: solution: List representing the solution to the puzzle.
             tries: int representing the number of tries taken to find the solution.
    Solves a puzzle with given constraints using backtracking with pruning.
    """
    primes = [2, 3, 5, 7]
    evens = [0, 2, 4, 6, 8]
    odds = [1, 3, 5, 7, 9]

    solution = []
    # Use a list for 'tries' to make it mutable across recursive calls
    tries_count = [0]

    def is_consistent(p, cons):
        """Checks if a partial password 'p' is consistent with the given constraints 'cons'."""
        for c in cons:
            # Constraint: All digits are prime and unique
            if c == [-1, -1]:
                seen = set() 
                for digit in p:
                    if digit is not None:
                        if digit not in primes:
                            return False
                        if digit in seen:
                            return False
                        seen.add(digit)

            # Constraint: Digit at a position is even (0) or odd (1)
            elif len(c) == 2 and c[1] in [0, 1]:
                pos, val = c
                if p[pos] is not None:
                    is_even = p[pos] in evens
                    if val == 0 and not is_even: return False
                    if val == 1 and is_even: return False
            # Constraint: A specific digit is at a specific position (mask)
            elif len(c) == 3:
                for i in range(3):
                    if c[i] != -1 and p[i] is not None and p[i] != c[i]:
                        return False
        return True

    def backtrack(position, current_password):
        """Recursively builds the password, backtracking when a constraint is violated."""
        # Pruning step: if the current path is already invalid, stop.
        if not is_consistent(current_password, constraints):
            return False

        # Base case: a full, valid password has been constructed.
        if position == 3:
            tries_count[0] += 1
            # Check if the found password is the one we are looking for.
            if current_password == password:
                nonlocal solution
                solution = list(current_password)
                return True  # Correct solution found, stop searching.
            else:
                return False # A valid password, but not the target. Continue searching.

        # Recursive step: try all possible digits for the current position.
        for digit in range(10):
            current_password[position] = digit
            if backtrack(position + 1, current_password):
                return True  # Propagate the "found" signal up the call stack.
        
        # Backtrack by allowing the loop to try the next digit.
        current_password[position] = None
        return False

    backtrack(0, [None, None, None])
    
    return solution, tries_count[0]

if __name__ == "__main__":
    # Example 1: All digits are prime, first digit is 2.
    true_password_1 = [2, 5, 7] 
    constraints_1 = [[-1, -1], [2, -1, -1]]
    solution_1, tries_1 = solve_puzzle(true_password_1, constraints_1)
    print(f"--- Puzzle 1 ---")
    print(f"Constraints: {constraints_1}")
    print(f"Found solution: {solution_1} in {tries_1} tries.")
    print(f"Correct password was: {true_password_1}")
    print(f"Solution is correct: {solution_1 == true_password_1}\n")

    # Example 2: First digit is odd, second is even, third is 9.
    true_password_2 = [3, 2, 9]
    constraints_2 = [[0, 1], [1, 0], [-1, -1, 9]]
    solution_2, tries_2 = solve_puzzle(true_password_2, constraints_2)
    print(f"--- Puzzle 2 ---")
    print(f"Constraints: {constraints_2}")
    print(f"Found solution: {solution_2} in {tries_2} tries.")
    print(f"Correct password was: {true_password_2}")
    print(f"Solution is correct: {solution_2 == true_password_2}\n")

    # Example 3: No solution possible (digit 1 is both even and odd)
    # true_password_3 = None
    # constraints_3 = [[1, 0], [1, 1]]
    # solution_3, tries_3 = solve_puzzle(true_password_3, constraints_3)
    # print(f"--- Puzzle 3 (No Solution) ---")
    # print(f"Constraints: {constraints_3}")
    # print(f"Found solution: {solution_3} in {tries_3} tries.")
    # print(f"Correctly found no solution: {solution_3 == []}\n")