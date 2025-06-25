def solve_puzzle(constraints):
    """
    Solves a puzzle with given constraints using backtracking.
    """
    length = constraints.get("length", 3)
    unique = constraints.get("unique", False)
    puzzle_type = constraints.get("type", "")

    solution = None
    
    def is_valid(num, current_password):
        if unique and num in current_password:
            return False
        
        if puzzle_type == "prime":
            if num < 2: return False
            for i in range(2, int(num**0.5) + 1):
                if num % i == 0: return False
        elif puzzle_type == "even":
            if num % 2 != 0: return False
        elif puzzle_type == "odd":
            if num % 2 == 0: return False
        
        return True

    def backtrack(current_password):
        nonlocal solution
        # If a solution is already found, stop searching
        if solution is not None:
            return

        if len(current_password) == length:
            solution = list(current_password)
            return

        # For a digit-based puzzle, we iterate 0-9
        for i in range(10):
            if is_valid(i, current_password):
                current_password.append(i)
                backtrack(current_password)
                # If a solution is found, we can stop early
                if solution is not None:
                    return
                current_password.pop() # Backtrack

    backtrack([])
    return solution

if __name__ == "__main__":
    constraints = {
        "length": 3,
        "unique": True,
        "type": "prime"
    }
    solution = solve_puzzle(constraints)
    print("Solution:", solution)