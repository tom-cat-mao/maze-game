import random
import time
import hashlib
import itertools
from collections import deque

# --- Helper Classes (PasswordLock, Clues, Locker, BossGroup) remain the same ---
class PasswordLock:
    def __init__(self):
        self.salt = b'\xb2S"e}\xdf\xb0\xfe\x9c\xde\xde\xfe\xf3\x1d\xdc>'
    
    def hash_password(self, password):            
        password_bytes = password.encode('utf-8')
        hash_obj = hashlib.sha256(self.salt + password_bytes)
        return hash_obj.hexdigest()
    
    def verify_password(self, input_password, stored_hash):
        return self.hash_password(input_password) == stored_hash

class Clues:
    def __init__(self, clue):
        self.clues = []
        self._add_clue(clue)

    def _add_clue(self, clues):
        length = len(clues)
        num_clue = random.randint(1, 3)
        for _ in range(num_clue):
            try:
                clue = clues[random.randint(0, length - 1)]
            except IndexError:
                return
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
        self.clue = Clues(self.tips)
        self.is_locked = is_locked
        self.reward = self._get_reward(locker_id)

    def _get_reward(self, locker_id):
        return random.randint(1, 100)

    def _set_password(self, locker_id):
        password = [random.randint(0, 9) for _ in range(3)]
        # Logic for tips remains the same
        return password

    def get_tips(self):
        return self.tips

    def toggle_lock(self):
        self.is_locked = not self.is_locked

    def check_password(self, password):
        if self.is_locked:
            hashed_input = self.password_lock.hash_password(''.join(map(str, password)))
            return hashed_input == self.password_hash
        return True

class BossGroup:
    def __init__(self):
        self.bosses_number = random.randint(1, 10)
        self.bosses = [random.randint(1, 100) for _ in range(self.bosses_number)]

# --- Maze Class ---
class Maze:
    def __init__(self, width, height):
        if width < 5 or height < 5:
            raise ValueError("Maze dimensions must be at least 5x5.")
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        self.maze = [['.' for _ in range(self.width)] for _ in range(self.height)]
        self.lockers = {}
        self.bosses = {}

    def generate_maze(self):
        # Using a simple open grid for testing purposes
        for r in range(self.height):
            for c in range(self.width):
                if r == 0 or r == self.height - 1 or c == 0 or c == self.width - 1:
                    self.maze[r][c] = '#'
        self.maze[1][1] = 'S'
        self.maze[self.height - 2][self.width - 2] = 'E'

    def place_elements(self, elements):
        """Places elements at specified coordinates."""
        for r, c, char in elements:
            if 1 <= r < self.height - 1 and 1 <= c < self.width - 1:
                self.maze[r][c] = char

# --- New Test Generation Logic ---

def find_path_bfs(maze, start, end):
    """Standard BFS to find a path, used for connectivity check."""
    q = deque([(start, [start])])
    visited = {start}
    while q:
        (r, c), path = q.popleft()
        if (r, c) == end:
            return path
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and \
               maze[nr][nc] != '#' and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append(((nr, nc), path + [(nr, nc)]))
    return None

def calculate_bruteforce_max_profit(maze):
    """
    Calculates the theoretical maximum profit for a maze by trying all
    permutations of visiting the valuable nodes.
    This is computationally expensive and only suitable for small test cases.
    """
    value_map = {'G': 10, 'T': -5, 'E': 5}
    critical_points = {}
    start_pos, end_pos = None, None

    for r, row in enumerate(maze):
        for c, char in enumerate(row):
            if char == 'S':
                start_pos = (r, c)
            elif char == 'E':
                end_pos = (r, c)
            elif char in value_map:
                critical_points[(r, c)] = value_map[char]

    if not start_pos or not end_pos:
        return 0, "Start or End not found"

    # Pre-calculate all-pairs shortest paths
    all_nodes = [start_pos] + list(critical_points.keys()) + [end_pos]
    node_map = {pos: i for i, pos in enumerate(all_nodes)}
    dist_matrix = [[None] * len(all_nodes) for _ in range(len(all_nodes))]

    for i in range(len(all_nodes)):
        for j in range(i, len(all_nodes)):
            path = find_path_bfs(maze, all_nodes[i], all_nodes[j])
            if path:
                dist_matrix[i][j] = dist_matrix[j][i] = len(path) - 1

    max_profit = float('-inf')
    
    # Iterate through all permutations of visiting the valuable nodes
    valuable_nodes = list(critical_points.keys())
    for i in range(len(valuable_nodes) + 1):
        for p in itertools.permutations(valuable_nodes, i):
            current_profit = 0
            current_pos = start_pos
            
            # Path from Start to first node in permutation
            path_to_first = dist_matrix[node_map[current_pos]][node_map[p[0]]] if p else dist_matrix[node_map[current_pos]][node_map[end_pos]]
            if path_to_first is None: continue

            # Calculate profit from the permutation
            for node in p:
                current_profit += critical_points[node]
                path_to_next = dist_matrix[node_map[current_pos]][node_map[node]]
                if path_to_next is None:
                    current_profit = float('-inf')
                    break
                current_pos = node
            if current_profit == float('-inf'): continue

            # Path from last node to End
            path_to_end = dist_matrix[node_map[current_pos]][node_map[end_pos]]
            if path_to_end is None: continue
            
            current_profit += value_map['E'] # Add end value
            max_profit = max(max_profit, current_profit)

    # Case where we go directly from Start to End
    direct_path = dist_matrix[node_map[start_pos]][node_map[end_pos]]
    if direct_path is not None:
        max_profit = max(max_profit, value_map['E'])

    return max_profit if max_profit > float('-inf') else 0, "Calculation complete"


def generate_test_maze(width, height, elements, test_id="test_01"):
    """
    Generates a specific maze for testing and calculates its theoretical max profit.
    """
    print(f"--- Generating Test Maze: {test_id} ---")
    maze_obj = Maze(width, height)
    maze_obj.generate_maze()
    maze_obj.place_elements(elements)
    
    maze_data = maze_obj.maze
    
    print("Maze Layout:")
    for row in maze_data:
        print("".join(row))
        
    print("\nCalculating theoretical max profit (Brute-force)...")
    max_profit, status = calculate_bruteforce_max_profit(maze_data)
    print(f"Calculation Status: {status}")
    print(f"Theoretical Max Profit: {max_profit}")
    
    return {
        "id": test_id,
        "maze": maze_data,
        "theoretical_max_profit": max_profit
    }

if __name__ == "__main__":
    # A simple test case where the direct path is not the most profitable
    test_elements_1 = [
        (2, 2, 'G'), # +10
        (2, 4, 'T'), # -5
    ]
    # Expected path: S -> G -> E. Profit = 10 (G) + 5 (E) = 15
    # Direct path: S -> E. Profit = 5
    # Path S -> T -> E: Profit = -5 (T) + 5 (E) = 0
    # Path S -> G -> T -> E: Profit = 10 - 5 + 5 = 10
    generate_test_maze(7, 7, test_elements_1, "simple_profit_test")

    print("\n" + "="*40 + "\n")

    # A more complex case
    test_elements_2 = [
        (2, 4, 'G'), # G1: +10
        (4, 2, 'G'), # G2: +10
        (4, 4, 'T'), # T1: -5
    ]
    # Expected path: S -> G2 -> G1 -> E. Profit = 10 + 10 + 5 = 25
    generate_test_maze(7, 7, test_elements_2, "complex_routing_test")
