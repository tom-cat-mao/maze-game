import pytest
from app.algorithms.maze_generator import generate_maze

def find_char(maze, char):
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            if val == char:
                return (r, c)
    return None

def is_connected(maze):
    """Checks if Start and End are connected using BFS."""
    start_pos = find_char(maze, 'S')
    end_pos = find_char(maze, 'E')
    
    if not start_pos or not end_pos:
        return False

    q = [start_pos]
    visited = {start_pos}
    
    while q:
        r, c = q.pop(0)
        
        if (r, c) == end_pos:
            return True
            
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and \
               maze[nr][nc] != '#' and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append((nr, nc))
                
    return False

def test_generate_maze_always_solvable():
    """
    Tests that the generated maze always has a path from Start to End.
    Runs multiple times to account for randomness.
    """
    for i in range(10): # Run the test 10 times
        maze = generate_maze(15, 15)
        assert find_char(maze, 'S') is not None, f"Run {i+1}: Start 'S' not found"
        assert find_char(maze, 'E') is not None, f"Run {i+1}: End 'E' not found"
        assert is_connected(maze), f"Run {i+1}: Maze is not solvable"

def test_maze_dimensions():
    """Tests that the maze is generated with the correct dimensions."""
    width, height = 21, 31
    maze = generate_maze(width, height)
    assert len(maze) == height
    assert all(len(row) == width for row in maze)

def test_maze_has_walls_as_border():
    """Tests that the maze has a border of walls."""
    maze = generate_maze(11, 11)
    height = len(maze)
    width = len(maze[0])
    assert all(maze[0][c] == '#' for c in range(width))
    assert all(maze[height-1][c] == '#' for c in range(width))
    assert all(maze[r][0] == '#' for r in range(height))
    assert all(maze[r][width-1] == '#' for r in range(height))

def test_maze_has_loops_after_breaking_walls():
    """
    Tests that breaking walls introduces loops (cells with >2 path neighbors).
    """
    maze = generate_maze(25, 25) # generate_maze now breaks walls by default
    
    has_loop = False
    for r in range(1, len(maze) - 1):
        for c in range(1, len(maze[0]) - 1):
            if maze[r][c] != '#':
                neighbors = 0
                if maze[r-1][c] != '#': neighbors += 1
                if maze[r+1][c] != '#': neighbors += 1
                if maze[r][c-1] != '#': neighbors += 1
                if maze[r][c+1] != '#': neighbors += 1
                
                if neighbors > 2:
                    has_loop = True
                    break
        if has_loop:
            break
            
    assert has_loop, "The maze generated should have loops after breaking walls."
