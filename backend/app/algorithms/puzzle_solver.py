import json
from maze_generator import PasswordLock

def solve_puzzle(password, constraints):
    """
    Inputs: password: list of three digits representing the password. (Used for verification in tests).
            constraints: List of constraints for the puzzle.
                e.g. [[-1, -1], [pos, 0], [pos, 1], [digit, -1, -1], [-1, digit, -1], [-1, -1, digit]]
    Outputs: solution: List representing the solution to the puzzle.
             tries: int representing the number of tries taken to find the solution.
    Solves a puzzle with given constraints using backtracking with pruning.
    """
    password_locker = PasswordLock()
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
                if p[pos-1] is not None:
                    is_even = p[pos-1] in evens
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
            # Convert the list of digits to a string before verification.
            password_str = "".join(map(str, current_password))
            # Check if the found password is the one we are looking for.
            if password_locker.verify_password(password_str, password):
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

def json_loader(json_file):
    """
    Converts a JSON file to a Python object.
    Args:
        json_file (str): Path to the JSON file to be converted.
    Returns:
        tuple: A tuple containing the constraints and the password.
    Example: password = "hash", constraints = [[-1, -1], [0, 0], [1, 1], [2, -1, -1], [-1, 2, -1], [-1, -1, 5]]
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
        constraints = data.get("C", [])
        password = data.get("L", "")
        password = str(password)
        return constraints, password


if __name__ == "__main__":
    json_file = 'file_path'  # Replace with your JSON file path
    constraints, password = json_loader(json_file)
    # print(f"password: {password}")
    # print(f"password type: {type(password)}")
    solution, tries = solve_puzzle(password, constraints)
    
    print(f"Solution: {solution}")
    print(f"Tries: {tries}")

# Example usage:
# python puzzle_solver.py path/to/your/json_file.json