import random

def generate_maze(width, height):
    """
    Generates a perfect maze using Prim's algorithm, ensuring a single
    path exists between any two cells.
    '#' = wall, '.' = path
    """
    if width < 5 or height < 5:
        raise ValueError("Maze dimensions must be at least 5x5.")
    
    # Initialize maze with walls
    maze = [['#' for _ in range(width)] for _ in range(height)]
    
    # Pick a random starting cell
    start_x, start_y = random.randint(1, width - 2), random.randint(1, height - 2)
    maze[start_y][start_x] = '.'
    
    # A 'frontier' is a list of walls adjacent to visited cells.
    frontiers = []
    for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = start_x + x, start_y + y
        if 1 <= nx < width - 1 and 1 <= ny < height - 1:
            frontiers.append((nx, ny))

    while frontiers:
        # Pick a random wall from the list
        wall_x, wall_y = random.choice(frontiers)
        frontiers.remove((wall_x, wall_y))
        
        # Find the cell this wall divides
        neighbors = []
        if wall_x > 1 and maze[wall_y][wall_x - 1] == '.':
            neighbors.append((wall_x + 1, wall_y))
        if wall_x < width - 2 and maze[wall_y][wall_x + 1] == '.':
            neighbors.append((wall_x - 1, wall_y))
        if wall_y > 1 and maze[wall_y - 1][wall_x] == '.':
            neighbors.append((wall_x, wall_y + 1))
        if wall_y < height - 2 and maze[wall_y + 1][wall_x] == '.':
            neighbors.append((wall_x, wall_y - 1))

        if len(neighbors) == 1:
            # This wall divides a visited cell from an unvisited one.
            # Carve a path through the wall.
            maze[wall_y][wall_x] = '.'
            
            # Add the new cell's frontiers to the list
            new_cell_x, new_cell_y = neighbors[0]
            if 1 <= new_cell_x < width - 1 and 1 <= new_cell_y < height - 1:
                maze[new_cell_y][new_cell_x] = '.'
                for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nx, ny = new_cell_x + x, new_cell_y + y
                    if 1 <= nx < width - 1 and 1 <= ny < height - 1 and maze[ny][nx] == '#':
                        if (nx, ny) not in frontiers:
                            frontiers.append((nx, ny))

    # Place Start and End points
    maze[1][1] = 'S'
    maze[height - 2][width - 2] = 'E'

    # Place other elements
    place_elements(maze, width, height)

    # Break some walls to create loops, making the maze non-perfect
    break_walls(maze, width, height, percentage=0.1) # Break 10% of internal walls

    return maze

def break_walls(maze, width, height, percentage=0.1):
    """
    Randomly removes a certain percentage of internal walls to create loops.
    """
    internal_walls = []
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            if maze[r][c] == '#':
                # Ensure it's an internal wall, not a border that could be part of the generation logic
                if (maze[r-1][c] == '.' and maze[r+1][c] == '.') or \
                   (maze[r][c-1] == '.' and maze[r][c+1] == '.'):
                    internal_walls.append((r, c))
    
    num_to_break = int(len(internal_walls) * percentage)
    random.shuffle(internal_walls)
    
    for i in range(num_to_break):
        if not internal_walls: break
        r, c = internal_walls.pop()
        maze[r][c] = '.'

def place_elements(maze, width, height):
    """Randomly places Gold, Traps, etc. on path cells."""
    path_cells = []
    for r in range(height):
        for c in range(width):
            # Exclude start and end positions from item placement
            if maze[r][c] == '.':
                path_cells.append((r, c))
    
    random.shuffle(path_cells)

    # Define proportions based on available path cells
    num_gold = int(len(path_cells) * 0.1)
    num_traps = int(len(path_cells) * 0.05)
    
    if width <= 10:
        num_levers = 2
        num_bosses = 1
    else:
        num_levers = 3
        num_bosses = 2

    for _ in range(num_gold):
        if not path_cells: break
        r, c = path_cells.pop()
        maze[r][c] = 'G'

    for _ in range(num_traps):
        if not path_cells: break
        r, c = path_cells.pop()
        maze[r][c] = 'T'

    for _ in range(num_levers):
        if not path_cells: break
        r, c = path_cells.pop()
        maze[r][c] = 'L'

    for _ in range(num_bosses):
        if not path_cells: break
        r, c = path_cells.pop()
        maze[r][c] = 'B'
