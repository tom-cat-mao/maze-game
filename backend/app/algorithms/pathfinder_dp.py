from collections import deque

def solve_with_dp(maze):
    """
    Finds a path from 'S' to 'E' using Breadth-First Search (BFS).
    This implementation is chosen for its robustness and guaranteed termination.
    It finds the shortest path in terms of steps, not the highest value path.
    """
    height = len(maze)
    width = len(maze[0])
    
    value_map = {'G': 10, 'T': -5, '.': 0, 'S': 0, 'E': 5}

    start_pos = find_pos(maze, 'S')
    end_pos = find_pos(maze, 'E')

    if not start_pos or not end_pos:
        raise ValueError("Start 'S' or End 'E' not found in maze")

    queue = deque([(start_pos[0], start_pos[1], [list(start_pos)])])
    visited = {start_pos}

    while queue:
        r, c, path = queue.popleft()

        if (r, c) == end_pos:
            total_value = 0
            for pr, pc in path:
                total_value += value_map.get(maze[pr][pc], 0)
            return path, total_value

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < height and 0 <= nc < width and \
               maze[nr][nc] != '#' and (nr, nc) not in visited:
                
                visited.add((nr, nc))
                new_path = path + [[nr, nc]]
                queue.append((nr, nc, new_path))

    return [], 0

def find_pos(maze, char):
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            if val == char:
                return (r, c)
    return None


if __name__ == "__main__":
    maze = [
        "###############",
        "#SG.#L#...#.#.#",
        "#L###.#.#.#.#.#",
        "#.......#G..TB#",
        "#.#############",
        "#.#.T.#.......#",
        "#.#.#.#####.###",
        "#.#.#.G.#.#.#.#",
        "#.#G###.#.#.#B#",
        "#.#...#......G#",
        "#.#.#G#######.#",
        "#T#.#.#...#.G.#",
        "#.###.#G###.#L#",
        "#.G..T#.....#E#",
        "###############"
    ]

    path, total_value = solve_with_dp(maze)
    print("Path:", path)
    print("Total Value:", total_value)