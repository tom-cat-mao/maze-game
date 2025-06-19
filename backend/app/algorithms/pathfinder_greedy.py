def solve_with_greedy(maze):
    """
    Solves the maze using a backtracking greedy algorithm. It tries to move
    to the best-looking neighbor, but if it gets stuck, it backtracks.
    """
    height = len(maze)
    width = len(maze[0])
    
    value_map = {'G': 10, 'T': -5, '.': 0, 'S': 0, 'E': 5}

    start_pos = find_pos(maze, 'S')
    end_pos = find_pos(maze, 'E')

    if not start_pos or not end_pos:
        raise ValueError("Start 'S' or End 'E' not found in maze")

    stack = [(start_pos, [start_pos])]
    visited = {start_pos}

    while stack:
        (r, c), path = stack.pop()

        if (r, c) == end_pos:
            total_value = 0
            for pr, pc in path:
                total_value += value_map.get(maze[pr][pc], 0)
            return path, total_value

        # Find all valid neighbors and sort them by the heuristic
        neighbors = []
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width and \
               maze[nr][nc] != '#' and (nr, nc) not in visited:
                
                cell_value = value_map.get(maze[nr][nc], 0)
                dist_to_end = abs(nr - end_pos[0]) + abs(nc - end_pos[1])
                heuristic = cell_value - dist_to_end * 0.1
                neighbors.append((heuristic, (nr, nc)))
        
        # Sort neighbors by heuristic descending (best first)
        neighbors.sort(key=lambda x: x[0], reverse=True)

        for _, (nr, nc) in neighbors:
            if (nr, nc) not in visited:
                visited.add((nr, nc))
                new_path = path + [(nr, nc)]
                stack.append(((nr, nc), new_path))

    return [], 0 # No path found

def find_pos(maze, char):
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            if val == char:
                return (r, c)
    return None
