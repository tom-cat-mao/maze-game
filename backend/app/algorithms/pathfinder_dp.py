import logging
import time
from collections import deque

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def solve_with_dp(maze):
    """
    Finds the path with the maximum possible score from 'S' to 'E' in a maze.
    This version allows for paths to be revisited, but rewards/traps can only be
    triggered once. It uses State Compression DP where the path cost between
    critical points is calculated dynamically.
    """
    start_time = time.time()
    logging.info("DP solver for maximum score started.")
    
    height = len(maze)
    width = len(maze[0])
    value_map = {'G': 1, 'T': -10, 'E': 5} # 'E' has a value now

    # --- 1. Identify all critical points (S, E, G, T) ---
    critical_points = []
    pos_to_id = {}
    
    start_pos = find_pos(maze, 'S')
    if not start_pos:
        logging.error("Start point 'S' not found in maze.")
        return [], 0

    # S is always id 0
    critical_points.append({'id': 0, 'pos': start_pos, 'char': 'S'})
    pos_to_id[start_pos] = 0
    
    for r in range(height):
        for c in range(width):
            if maze[r][c] in value_map:
                node_id = len(critical_points)
                critical_points.append({'id': node_id, 'pos': (r, c), 'char': maze[r][c]})
                pos_to_id[(r, c)] = node_id
    
    k = len(critical_points)
    id_to_pos = {info['id']: info['pos'] for info in critical_points}
    end_node_id = pos_to_id.get(find_pos(maze, 'E'), -1)

    logging.info(f"Found {k} critical points. End node ID: {end_node_id}")
    if k == 0: return [], 0
    if end_node_id == -1:
        logging.error("End point 'E' not found among critical points.")
        return [], 0

    # --- 2. Initialize DP table ---
    # dp[mask][i] = max score ending at node i, having visited nodes in mask
    dp = [[float('-inf')] * k for _ in range(1 << k)]
    # parent[mask][i] = (prev_node_id, path_from_prev_to_i)
    parent = [[None] * k for _ in range(1 << k)]
    
    # Start state: at node S (id 0), mask is 1 (only S visited), score is 0
    dp[1][0] = 0
    logging.info("DP table initialized. Starting main loop.")

    # --- 3. State Compression DP main loop ---
    for mask in range(1, 1 << k):
        # Time limit check
        if time.time() - start_time > 15: # 15-second time limit
            logging.warning("Solver timed out. Returning best path found so far.")
            break

        for i in range(k):
            if not ((mask >> i) & 1): continue # Node i must be in the current path
            if dp[mask][i] == float('-inf'): continue # Skip unreachable states

            for j in range(k):
                if not ((mask >> j) & 1): # If node j has not been visited yet
                    
                    # --- Dynamic Path Calculation ---
                    # Path from i to j, avoiding already visited critical points in the mask
                    path_ij = _find_path_bfs_dynamic(maze, id_to_pos[i], id_to_pos[j], mask, id_to_pos)
                    
                    if path_ij:
                        new_mask = mask | (1 << j)
                        reward = value_map.get(critical_points[j]['char'], 0)
                        new_reward = dp[mask][i] + reward
                        
                        if new_reward > dp[new_mask][j]:
                            dp[new_mask][j] = new_reward
                            parent[new_mask][j] = (i, path_ij)
                            logging.debug(f"DP Update: dp[{bin(new_mask)}][{j}] = {new_reward:.2f} (from node {i})")

    # --- 4. Find the best final path that ends at 'E' ---
    max_reward = float('-inf')
    final_mask = -1
    
    for mask in range(1, 1 << k):
        if (mask >> end_node_id) & 1: # Must include the end node
            if dp[mask][end_node_id] > max_reward:
                max_reward = dp[mask][end_node_id]
                final_mask = mask

    if final_mask == -1:
        logging.warning("No path to 'E' could be found.")
        # Fallback to simple BFS from S to E if no reward path is found
        path = _find_path_bfs_dynamic(maze, start_pos, id_to_pos[end_node_id], 0, id_to_pos)
        return path if path else [], 0

    logging.info(f"Path reconstruction started. Final mask: {bin(final_mask)}, Max reward: {max_reward}")

    # --- 5. Reconstruct the path ---
    final_path = []
    curr_mask = final_mask
    curr_node_idx = end_node_id
    
    while curr_node_idx != 0:
        res = parent[curr_mask][curr_node_idx]
        if not res:
            logging.error(f"Path reconstruction failed: parent is None for mask {bin(curr_mask)}, node {curr_node_idx}")
            break
        
        prev_node_idx, path_segment = res
        
        # Add the path segment, excluding the start point of the segment to avoid duplication
        final_path.extend(reversed(path_segment[1:]))
        
        # Move to the previous state
        curr_mask &= ~(1 << curr_node_idx)
        curr_node_idx = prev_node_idx

    # Add the starting position
    final_path.append(id_to_pos[0])
    final_path.reverse()
    
    logging.info(f"Path reconstruction complete. Total steps: {len(final_path)}")
    return final_path, max_reward

def _find_path_bfs_dynamic(maze, start, end, visited_mask, id_to_pos):
    """
    Finds the shortest path between two points using BFS, avoiding critical points
    that have already been visited (as defined by the mask).
    """
    q = deque([(start, [start])])
    visited_bfs = {start}
    
    # Create a set of forbidden positions for this specific BFS run
    # These are critical points in the mask, excluding the start and end of this segment
    forbidden_pos = {
        pos for id, pos in id_to_pos.items() 
        if (visited_mask >> id) & 1 and pos != start and pos != end
    }

    while q:
        (r, c), path = q.popleft()
        if (r, c) == end:
            return path
            
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and \
               maze[nr][nc] != '#' and (nr, nc) not in visited_bfs and \
               (nr, nc) not in forbidden_pos:
                
                visited_bfs.add((nr, nc))
                q.append(((nr, nc), path + [(nr, nc)]))
                
    return None # No path found

def find_pos(maze, char):
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            if val == char:
                return (r, c)
    return None
