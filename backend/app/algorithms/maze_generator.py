import random
import time
import hashlib
import json

class PasswordLock:
    def __init__(self):
        self.salt = b'\xb2S"e}\xdf\xb0\xfe\x9c\xde\xde\xfe\xf3\x1d\xdc>'
    
    def hash_password(self, password):            
        # 将密码转换为字节流
        password_bytes = password.encode('utf-8')
        
        # 将盐值和密码组合并进行哈希
        hash_obj = hashlib.sha256(self.salt + password_bytes)
        password_hash = hash_obj.hexdigest()
        
        return password_hash
    
    def verify_password(self, input_password, stored_hash):
        # 使用相同的盐值对输入密码进行哈希
        calculated_hash = self.hash_password(input_password)
        
        # 比较计算出的哈希值与存储的哈希值
        return calculated_hash == stored_hash

class Clues:
    def __init__(self, clue):
        self.clues = []
        self._add_clue(clue)

    def _add_clue(self, clues):
        """
        Adds a clue to the list of clues.
        """
        length = len(clues)
        num_clue = random.randint(1, 3)
        for _ in range(num_clue):
            try:
                # Clues = [[], [], []]
                clue = clues[random.randint(0, length - 1)]
            except IndexError:
                # If the list is empty, skip adding a clue
                return
            # Append the clue to the list
            self.clues.append(clue)

    def get_clues(self):
        return self.clues

class Locker:
    def __init__(self, locker_id, is_locked=True):
        self.password_lock = PasswordLock()
        self.locker_id = locker_id
        self.tips = []
        self.password = self._set_password(locker_id)
        self.password_hash = self.password_lock.hash_password(''.join(map(str, self.password)))
        # The locker can be locked or unlocked
        self.clue = Clues(self.tips)
        self.is_locked = is_locked
        self.reward = self._get_reward(locker_id)

    def _get_reward(self, locker_id):
        """
        Determines the reward for unlocking the locker.
        """
        return random.randint(1, 100)

    def _set_password(self, locker_id):
        """
        Sets a 3-digit password for the locker.
        - The password is prime numbers or others between 0 and 9.
        - The password's first digit is even or odd.
        - The each digit is unique or not.
        """
        prime_numbers = [2, 3, 5, 7]
        even_numbers = [0, 2, 4, 6, 8]
        odd_numbers = [1, 3, 5, 7, 9]

        password = []
        for _ in range(3):
            digit = random.randint(0, 9)
            password.append(digit)
        
        prime_flag = True
        unique_flag = True

        # Check password uniqueness
        if len(set(password)) != len(password):
            unique_flag = False

        for i, digit in enumerate(password):
            if digit not in prime_numbers:
                prime_flag = False
            if digit in even_numbers:
                # Tips for even digit, e.g. [position, 0]. Position is 1-based.
                self.tips.append([i + 1, 0])
            if digit in odd_numbers:
                # Tips for odd digit, e.g. [position, 1]. Position is 1-based.
                self.tips.append([i + 1, 1])
            
            # The mask constraint is 0-indexed.
            mask = [-1, -1, -1]
            mask[i] = digit
            self.tips.append(mask)

        if prime_flag:
            self.tips.append([-1,-1])   

        return password

    def get_tips(self):
        """
        Returns tips about the locker password.
        """
        return self.tips

    def toggle_lock(self):
        self.is_locked = not self.is_locked

    def check_password(self, password):
        """
        Checks if the provided password matches the locker password.
        Returns True if it matches, False otherwise.
        """
        if self.is_locked:
            hashed_input = self.password_lock.hash_password(''.join(map(str, password)))
            return hashed_input == self.password_hash
        else:
            # If the locker is not locked, any password is accepted
            return True

    def __repr__(self):
        return f"Locker({self.locker_id}, {'Locked' if self.is_locked else 'Unlocked'})"

class BossGroup:
    def __init__(self):
        self.bosses_number = random.randint(1, 10)
        self.bosses = []
        self._add_boss()

    def _add_boss(self):
        """
        Adds bosses to the group. e.g. [blood1, blood2, blood3, ...]
        """
        for _ in range(self.bosses_number):
            blood = random.randint(1, 100)
            self.bosses.append(blood)

class Maze:
    def __init__(self, width, height):
        """ Initializes a maze with given width and height.
        The maze is represented as a grid of characters.
        '.' represents a path, '#' represents a wall.
        """
        if width < 7 or height < 7:
            raise ValueError("Maze dimensions must be at least 7x7.")
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1

        self.width = width
        self.height = height
        self.locker_id = set()
        self.lockers = {}
        self.bosses = {}
        self.maze = []
        self.unique_path = []
        self.unique = False
        self.start_pos = None
        self.end_pos = None
        self.player_skills = self._set_player_skills()

    def _set_player_skills(self):
        """
        Sets the player's skills for the maze game.
        Skills are represented as a list of tuples (damage, cooldown).
        """
        skill_number = random.randint(1, 10)
        skills = []
        skills.append([3, 0])  # Add a default skill with no damage and no cooldown
        for _ in range(skill_number):
            damage = random.randint(1, 50)
            cooldown = random.randint(1, 5)
            skills.append([damage, cooldown])
        return skills

    def _recursive_division(self, r, c, height, width):
        """
        Recursively divides a chamber of the maze with a wall and a passage.
        (r, c) is the top-left corner of the chamber.
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
                self.maze[wall_r][i] = '#'
            self.maze[wall_r][passage_c] = '.'

            # Recurse on the two new sub-chambers
            self._recursive_division(r, c, wall_r - r, width)
            self._recursive_division(wall_r + 1, c, r + height - (wall_r + 1), width)

        else:  # VERTICAL
            # Column for the wall (must be an even index)
            wall_c = c + random.randrange(1, width, 2)
            # Row for the passage (must be an odd index to be a path)
            passage_r = r + random.randrange(0, height, 2)

            for i in range(r, r + height):
                self.maze[i][wall_c] = '#'
            self.maze[passage_r][wall_c] = '.'

            # Recurse on the two new sub-chambers
            self._recursive_division(r, c, height, wall_c - c)
            self._recursive_division(r, wall_c + 1, height, c + width - (wall_c + 1))


    def generate_maze(self):
        """
        Generates a maze using the Recursive Division algorithm.
        '#' = wall, '.' = path
        """
        width = self.width
        height = self.height
        # Initialize maze with open paths
        self.maze = [['.' for _ in range(width)] for _ in range(height)]

        # Add boundary walls
        for c in range(width):
            self.maze[0][c] = '#'
            self.maze[height - 1][c] = '#'
        for r in range(height):
            self.maze[r][0] = '#'
            self.maze[r][width - 1] = '#'

        # Start recursive division on the inner grid
        self._recursive_division(1, 1, height - 2, width - 2)

        # Find all valid locations on the boundary walls for Start/End points
        top_wall, bottom_wall, left_wall, right_wall = [], [], [], []
        # Top wall
        for c in range(1, width - 1):
            if self.maze[1][c] == '.': top_wall.append((0, c))
        # Bottom wall
        for c in range(1, width - 1):
            if self.maze[height - 2][c] == '.': bottom_wall.append((height - 1, c))
        # Left wall
        for r in range(1, height - 1):
            if self.maze[r][1] == '.': left_wall.append((r, 0))
        # Right wall
        for r in range(1, height - 1):
            if self.maze[r][width - 2] == '.': right_wall.append((r, width - 1))

        possible_walls = [wall for wall in [top_wall, bottom_wall, left_wall, right_wall] if wall]

        # Pick two distinct random locations for Start and End from different walls
        if len(possible_walls) >= 2:
            wall1_list, wall2_list = random.sample(possible_walls, 2)
            self.start_pos = random.choice(wall1_list)
            self.end_pos = random.choice(wall2_list)
        else:
            # Fallback: if openings are only on one wall, or less than 2 total openings.
            valid_wall_cells = [cell for wall in possible_walls for cell in wall]
            if len(valid_wall_cells) >= 2:
                self.start_pos, self.end_pos = random.sample(valid_wall_cells, 2)
            else:
                # Ultimate fallback for very small/unusual mazes
                self.start_pos = (0, 1) if self.maze[1][1] == '.' else (1,0)
                self.end_pos = (height - 1, width - 2)

        self.maze[self.start_pos[0]][self.start_pos[1]] = 'S'
        self.maze[self.end_pos[0]][self.end_pos[1]] = 'E'

    def place_elements(self):
        """Randomly places Gold, Traps, etc. on path cells."""
        path_cells = []
        for r in range(self.height):
            for c in range(self.width):
                # Exclude start and end positions from item placement
                if self.maze[r][c] == '.':
                    path_cells.append((r, c))
        
        random.shuffle(path_cells)

        # Define proportions based on available path cells
        num_gold = int(len(path_cells) * 0.1)
        num_traps = int(len(path_cells) * 0.05)

        num_bosses = 1
        if self.width <= 10:
            num_levers = 2
        else:
            num_levers = 3
        
        # Set the boss in final position
        if num_bosses > 0 and self.unique_path:
            # Find the empty cell around the end point
            r, c = self.unique_path[-2]  # Get the second last cell in the unique path
            if (r, c) in path_cells:
                path_cells.remove((r, c))  # Remove it from path cells
            self.maze[r][c] = 'B'
            self.bosses_group = BossGroup()
            self.bosses[(r, c)] = self.bosses_group

        # Place Gold, Traps, Levers
        # Set gold
        for _ in range(num_gold):
            if not path_cells: break
            r, c = path_cells.pop()
            self.maze[r][c] = 'G'

        # Set traps
        for _ in range(num_traps):
            if not path_cells: break
            r, c = path_cells.pop()
            self.maze[r][c] = 'T'

        # Set levers
        for _ in range(num_levers):
            if not path_cells: break
            r, c = path_cells.pop()
            self.maze[r][c] = 'L'
            if not self.locker_id:
                locker_id = 1
            else:
                locker_id = max(self.locker_id) + 1
            self.locker_id.add(locker_id)
            locker = Locker(locker_id)
            self.lockers[(r, c)] = locker

    def _get_adjacent_path_cell(self, r, c):
        """Given a coordinate (r, c) on a wall, find the adjacent path cell."""
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.height and 0 <= nc < self.width and self.maze[nr][nc] != '#':
                return (nr, nc)
        return None

    def _find_char(self, char):
        """
        Finds the first occurrence of a character in the maze.
        Returns the coordinates (row, column) of the character.
        """
        for r, row in enumerate(self.maze):
            for c, val in enumerate(row):
                if val == char:
                    return (r, c)
        return None

    def unique_path_checker(self):
        """
        Check if the maze has a unique path from start to end using DFS.
        If a unique path is found, it is stored in self.unique_path.
        """
        self.unique_path = []
        s_pos = self._find_char('S')
        e_pos = self._find_char('E')

        if not s_pos or not e_pos: return False

        start_node = self._get_adjacent_path_cell(s_pos[0], s_pos[1])
        end_node = self._get_adjacent_path_cell(e_pos[0], e_pos[1])

        if not start_node or not end_node: return False

        stack = [(start_node, [start_node])]
        paths_found = []

        while stack:
            current, path = stack.pop()

            if current == end_node:
                full_path = [s_pos] + path + [e_pos]
                paths_found.append(full_path)
                if len(paths_found) > 1:
                    self.unique_path = []
                    return False
                continue

            r, c = current
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                neighbor = (nr, nc)

                # A valid move is within bounds, not a wall, and not creating a cycle.
                if 0 <= nr < self.height and 0 <= nc < self.width and \
                   self.maze[nr][nc] != '#' and neighbor not in path:
                    new_path = list(path)
                    new_path.append(neighbor)
                    stack.append((neighbor, new_path))

        if len(paths_found) == 1:
            self.unique_path = paths_found[0]
            return True

        return False

def json_saver(maze_obj):
    """
    Saves the maze object to a JSON file.
    """
    """
    json style:
    {
        "width": 15,
        "height": 15,
        "maze": [
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", "S", ".", ".", "#", "L", "#", ".", ".", "#", ".", "#", ".", "#", ".", "#", "."],
            ["#", "L", "#", "#", "#", ".", "#", ".", "#", "." ... ]}"""

    path_file = "file_path.json"
    maze_data = {
        "width": maze_obj.width,
        "height": maze_obj.height,
        "maze": maze_obj.maze,
    }

    with open(path_file, 'w') as f:
        json.dump(maze_data, f, indent=4)
    print(f"Maze data saved to {path_file}")

def generate_maze(width, height):
    """
    A standalone generator function that creates a maze, ensures it has a
    unique path, places elements, and yields the maze state at key steps.
    This function is intended to be imported and used by the API endpoint.
    """
    while True:
        maze_obj = Maze(width, height)
        maze_obj.generate_maze()
        # Yield the maze after the basic structure is generated
        yield {'maze': maze_obj.maze}
        
        if maze_obj.unique_path_checker():
            # Yield the maze with a guaranteed unique path
            maze_obj.place_elements()
            
            boss_hps = []
            if hasattr(maze_obj, 'bosses_group') and maze_obj.bosses_group:
                boss_hps = maze_obj.bosses_group.bosses

            # Yield the final maze with all elements placed and boss data
            yield {'maze': maze_obj.maze, 'bosses': boss_hps}
            break # Exit the loop once a valid maze is created

if __name__ == "__main__":
    width, height = 15, 15  # Example dimensions
    maze_obj = Maze(width, height)

    # 1. Generate the maze structure.
    maze_obj.generate_maze()

    # 2. Check for a unique path now that the maze is generated.
    maze_obj.unique = maze_obj.unique_path_checker()

    if maze_obj.unique:
        print("The maze has a unique path from start to end.")
        # 3. Place elements since a unique path exists.
        maze_obj.place_elements()
        print("Elements placed in the maze.")
    else:
        print("The maze does not have a unique path from start to end.")

    # Print the final maze for visualization
    for row in maze_obj.maze:
        print(''.join(row))
    print("\n" + "="*40 + "\n")

    # Print unique path if it exists
    if maze_obj.unique:
        print("Unique path from start to end:", maze_obj.unique_path)

    # Check the lockers and their tips
    for locker_pos, locker in maze_obj.lockers.items():
        print(f"Locker at {locker_pos}, ID: {locker.locker_id}, Password: {locker.password}, Tips: {locker.get_tips()}, Clues: {locker.clue.get_clues()}")

    for boss_pos, boss_group in maze_obj.bosses.items():
        print(f"Boss at {boss_pos}, HP: {boss_group.bosses}")

    print(f"Skills: {maze_obj.player_skills}")
    for skill in maze_obj.player_skills:
        print(f"Player Skill - Damage: {skill[0]}, Cooldown: {skill[1]}")
    
    json_saver(maze_obj)
    # print(f"Maze data saved to {path_file}")
