import heapq
import logging
from typing import List, Tuple, Dict, Set

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Constants ---
# Mapping from maze characters to their values/penalties
VALUE_MAP = {'G': 10, 'T': -5, 'S': 0, 'E': 0, '.': 0, 'B': 0, 'L': 0}

class MazeGreedyNavigator:
    """
    Implements a greedy navigation algorithm with a 3x3 vision limit.
    The navigator chooses targets based on a cost-benefit ratio and uses A* for pathfinding.
    """
    def __init__(self, maze: List[List[str]]):
        """
        Initializes the maze navigator.
        
        Args:
            maze: The maze map, represented as a list of strings.
        """
        self.maze_str = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        
        self.treasure_values: Dict[Tuple[int, int], int] = {}
        self.trap_penalties: Dict[Tuple[int, int], int] = {}
        
        self.start_pos = self._find_char_position('S')
        self.end_pos = self._find_char_position('E')
        
        self._process_maze()

        self.current_pos = self.start_pos
        self.collected_treasures: Set[Tuple[int, int]] = set()
        self.triggered_traps: Set[Tuple[int, int]] = set()
        
        self.path = [self.start_pos]
        self.total_score = VALUE_MAP.get(self.maze_str[self.start_pos[0]][self.start_pos[1]], 0)

    def _find_char_position(self, char: str) -> Tuple[int, int]:
        """Finds the position of a specific character in the maze."""
        for r, row in enumerate(self.maze_str):
            for c, cell in enumerate(row):
                if cell == char:
                    return (r, c)
        raise ValueError(f"Character '{char}' not found in the maze.")

    def _process_maze(self):
        """Populates treasure and trap dictionaries from the maze string."""
        for r in range(self.rows):
            for c in range(self.cols):
                char = self.maze_str[r][c]
                if char == 'G':
                    self.treasure_values[(r, c)] = VALUE_MAP['G']
                elif char == 'T':
                    self.trap_penalties[(r, c)] = abs(VALUE_MAP['T'])

    def _get_vision_area(self) -> List[Tuple[int, int]]:
        """Gets all accessible positions within the 3x3 vision area."""
        row, col = self.current_pos
        vision = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < self.rows and 0 <= new_col < self.cols and
                        self.maze_str[new_row][new_col] != '#'):
                    vision.append((new_row, new_col))
        return vision

    def _manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Calculates the Manhattan distance between two points."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def _calculate_cost_benefit_ratio(self, target_pos: Tuple[int, int]) -> float:
        """Calculates the cost-benefit ratio (benefit / distance) for a target position."""
        if target_pos == self.current_pos:
            return 0.0
        
        distance = self._manhattan_distance(self.current_pos, target_pos)
        if distance == 0:
            return 0.0
        
        benefit = 0.0
        if target_pos in self.treasure_values and target_pos not in self.collected_treasures:
            benefit = float(self.treasure_values[target_pos])
        elif target_pos in self.trap_penalties and target_pos not in self.triggered_traps:
            benefit = -float(self.trap_penalties[target_pos])
        
        return benefit / distance

    def _find_path_a_star(self, target: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Finds the shortest path to a target using the A* algorithm."""
        if target == self.current_pos:
            return []
        
        logging.info(f"A* trying to find path from {self.current_pos} to {target}")
        open_set = [(0, self.current_pos, [])]
        closed_set = set()
        
        while open_set:
            f_score_pop, current, path = heapq.heappop(open_set)
            logging.info(f"  A* pop: f={f_score_pop}, pos={current}")
            
            if current in closed_set:
                continue
            
            path_so_far = path + [current]
            closed_set.add(current)
            
            if current == target:
                logging.info(f"  A* found target. Path: {path_so_far}")
                return path_so_far
            
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = current[0] + dr, current[1] + dc
                neighbor = (new_row, new_col)
                
                if (0 <= new_row < self.rows and 0 <= new_col < self.cols and
                        self.maze_str[new_row][new_col] != '#' and neighbor not in closed_set):
                    
                    g_score = len(path_so_far)
                    h_score = self._manhattan_distance(neighbor, target)
                    f_score = g_score + h_score
                    logging.info(f"    A* considering neighbor {neighbor}: g={g_score}, h={h_score}, f={f_score}")
                    heapq.heappush(open_set, (f_score, neighbor, path_so_far))
        
        logging.warning(f"A* could not find path from {self.current_pos} to {target}")
        return []  # Path not found

    def _get_best_target_in_vision(self) -> Tuple[int, int] | None:
        """Finds the target with the best cost-benefit ratio in the vision area."""
        vision_area = self._get_vision_area()
        best_target = None
        best_ratio = 0.0  # Only consider positive ratios
        
        logging.info(f"Vision scan at {self.current_pos}: {vision_area}")
        for pos in vision_area:
            if pos == self.current_pos:
                continue
            
            ratio = self._calculate_cost_benefit_ratio(pos)
            logging.info(f"  - Target {pos}: ratio={ratio:.2f}")
            if ratio > best_ratio:
                best_ratio = ratio
                best_target = pos
        
        if best_target:
            logging.info(f"Best target in vision: {best_target} with ratio {best_ratio:.2f}")
        else:
            logging.info("No valuable targets in vision.")
            
        return best_target

    def _move_along_path(self, path_to_target: List[Tuple[int, int]]):
        """Moves the navigator along a given path, updating state."""
        for next_pos in path_to_target[1:]:  # Skip the first element (current position)
            self.current_pos = next_pos
            self.path.append(next_pos)
            
            char_at_pos = self.maze_str[next_pos[0]][next_pos[1]]
            
            if char_at_pos == 'G' and next_pos not in self.collected_treasures:
                score = VALUE_MAP['G']
                self.total_score += score
                self.collected_treasures.add(next_pos)
                logging.info(f"Collected treasure at {next_pos}, value: {score}. New score: {self.total_score}")
            
            elif char_at_pos == 'T' and next_pos not in self.triggered_traps:
                score = VALUE_MAP['T']
                self.total_score += score
                self.triggered_traps.add(next_pos)
                logging.info(f"Triggered trap at {next_pos}, penalty: {score}. New score: {self.total_score}")

    def _move_towards_end(self):
        """Moves one step towards the end position."""
        logging.info("No valuable target. Moving towards End.")
        path_to_end = self._find_path_a_star(self.end_pos)
        
        if len(path_to_end) > 1:
            self._move_along_path(path_to_end[:2]) # Move only one step
        else:
            logging.warning("Cannot find path to end. Stuck.")
            # This case should ideally not happen in a valid maze.
            # We add a break condition in the main loop to prevent infinite loops.

    def navigate(self) -> Tuple[List[Tuple[int, int]], int]:
        """Executes the greedy navigation algorithm until the end is reached."""
        path_limit = self.rows * self.cols * 2 # Safety break for complex mazes
        while self.current_pos != self.end_pos and len(self.path) < path_limit:
            best_target = self._get_best_target_in_vision()
            
            if best_target:
                path_to_target = self._find_path_a_star(best_target)
                if path_to_target:
                    logging.info(f"Found path to best target {best_target}: {path_to_target}")
                    self._move_along_path(path_to_target)
                else:
                    logging.warning(f"Could not find path to target {best_target}. Fallback to end.")
                    self._move_towards_end()
            else:
                self._move_towards_end()
        
        # Add final score for reaching the end
        if self.current_pos == self.end_pos:
            self.total_score += VALUE_MAP.get('E', 0)
            logging.info(f"Reached End at {self.end_pos}. Final Score: {self.total_score}")

        if len(self.path) >= path_limit:
            logging.error("Path limit exceeded, navigation terminated.")

        return self.path, self.total_score

def solve_with_greedy(maze: List[List[str]]) -> Tuple[List[Tuple[int, int]], int]:
    """
    Solves the maze using the 3x3 vision greedy navigator.
    
    Args:
        maze: The maze map.
        
    Returns:
        A tuple containing the final path and the total score.
    """
    try:
        navigator = MazeGreedyNavigator(maze)
        path, value = navigator.navigate()
        return path, value
    except Exception as e:
        logging.error(f"An error occurred during greedy solving: {e}")
        return [], 0
