import random
import time

def _recursive_division(maze, r, c, height, width):
    """
    Recursively divides a chamber of the maze with a wall and a passage.
    (r, c) is the top-left corner of the chamber.
    Yields the maze state at each step.
    """
    if width <= 1 or height <= 1:
        return

    # Determine orientation of the wall to be added
    if width < height:
        orientation = 'HORIZONTAL'
    elif height < width:
        orientation = 'VERTICAL'
    else:
        orientation = random.choice(['HORIZONTAL', 'VERTICAL'])

    if orientation == 'HORIZONTAL':
        # Row for the wall (must be an even index)
        wall_r = r + random.randrange(1, height, 2)
        # Column for the passage (must be an odd index to be a path)
        passage_c = c + random.randrange(0, width, 2)

        for i in range(c, c + width):
            maze[wall_r][i] = '#'
            yield maze
        maze[wall_r][passage_c] = '.'
        yield maze

        # Recurse on the two new sub-chambers
        yield from _recursive_division(maze, r, c, wall_r - r, width)
        yield from _recursive_division(maze, wall_r + 1, c, r + height - (wall_r + 1), width)

    else:  # VERTICAL
        # Column for the wall (must be an even index)
        wall_c = c + random.randrange(1, width, 2)
        # Row for the passage (must be an odd index to be a path)
        passage_r = r + random.randrange(0, height, 2)

        for i in range(r, r + height):
            maze[i][wall_c] = '#'
            yield maze
        maze[passage_r][wall_c] = '.'
        yield maze

        # Recurse on the two new sub-chambers
        yield from _recursive_division(maze, r, c, height, wall_c - c)
        yield from _recursive_division(maze, r, wall_c + 1, height, c + width - (wall_c + 1))


def generate_maze(width, height):
    """
    Generates a maze using the Recursive Division algorithm.
    '#' = wall, '.' = path
    """
    if width < 5 or height < 5:
        raise ValueError("Maze dimensions must be at least 5x5.")

    # The recursive division algorithm works best with odd dimensions
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1
    
    # Initialize maze with open paths
    maze = [['.' for _ in range(width)] for _ in range(height)]
    yield maze

    # Add boundary walls
    for c in range(width):
        maze[0][c] = '#'
        maze[height - 1][c] = '#'
    for r in range(height):
        maze[r][0] = '#'
        maze[r][width - 1] = '#'
    yield maze

    # Start recursive division on the inner grid
    yield from _recursive_division(maze, 1, 1, height - 2, width - 2)

    # Place Start and End points
    maze[1][1] = 'S'
    maze[height - 2][width - 2] = 'E'
    yield maze

    # Place other elements
    place_elements(maze, width, height)
    yield maze

    # Break some walls to create loops, making the maze non-perfect
    break_walls(maze, width, height, percentage=0.1) # Break 10% of internal walls
    yield maze


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


if __name__ == "__main__":
    width, height = 15, 15  # Example dimensions
    maze_generator = generate_maze(width, height)
    
    for maze in maze_generator:
        for row in maze:
            print(''.join(row))
        time.sleep(0.5)  # Adjust the speed of generation here
        print("\n" + "="*40 + "\n")  # Separator between steps