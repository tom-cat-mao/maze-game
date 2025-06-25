import logging
from collections import deque

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def solve_with_dp(maze):
    """
    Finds the path with the maximum possible reward from 'S' to 'E' using
    State Compression Dynamic Programming, driven purely by maximizing rewards.
    """
    logging.info("DP solver started.")
    height = len(maze)
    width = len(maze[0])
    value_map = {'G': 10, 'T': -5}

    # --- 1. Identify all critical points (S, E, G, T) ---
    critical_points = []
    pos_to_id = {}
    start_pos = find_pos(maze, 'S')
    end_pos = find_pos(maze, 'E')

    # S is id 0, E is id 1
    critical_points.extend([
        {'id': 0, 'pos': start_pos, 'char': 'S'},
        {'id': 1, 'pos': end_pos, 'char': 'E'}
    ])
    pos_to_id[start_pos] = 0
    pos_to_id[end_pos] = 1
    
    for r in range(height):
        for c in range(width):
            if maze[r][c] in value_map:
                node_id = len(critical_points)
                critical_points.append({'id': node_id, 'pos': (r, c), 'char': maze[r][c]})
                pos_to_id[(r, c)] = node_id
    
    k = len(critical_points)
    logging.info(f"Found {k} critical points.")
    if k <= 2:
        _, path = _find_path_bfs(maze, start_pos, end_pos)
        return path, 0

    # --- 2. Pre-calculate paths between all pairs of critical points ---
    costs = [[None] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            if i != j:
                _, path = _find_path_bfs(maze, critical_points[i]['pos'], critical_points[j]['pos'])
                costs[i][j] = path
    logging.info("Finished pre-calculating costs between all critical points.")
    # --- DEBUG: Print costs to End node ---
    for i in range(k):
        if i != 1 and costs[i][1]:
            logging.debug(f"Path from {critical_points[i]['char']}({i}) to E(1) exists. Length: {len(costs[i][1])}")
        elif i != 1:
            logging.debug(f"Path from {critical_points[i]['char']}({i}) to E(1) NOT found.")
    # --- END DEBUG ---

    # --- 3. Initialize DP table ---
    dp = [[float('-inf')] * k for _ in range(1 << k)]
    parent = [[None] * k for _ in range(1 << k)]
    dp[1][0] = 0  # Mask for S (id 0) is 1, reward is 0

    # --- 4. State Compression DP main loop ---
    logging.info("Starting State Compression DP main loop.")
    for mask in range(1, 1 << k):
        for i in range(k):
            if not ((mask >> i) & 1): continue
            if dp[mask][i] == float('-inf'): continue
            
            for j in range(k):
                if not ((mask >> j) & 1):
                    if costs[i][j]:
                        new_mask = mask | (1 << j)
                        reward = value_map.get(critical_points[j]['char'], 0)
                        new_reward = dp[mask][i] + reward
                        
                        if new_reward > dp[new_mask][j]:
                            dp[new_mask][j] = new_reward
                            parent[new_mask][j] = i
                            logging.debug(f"DP Update: dp[{bin(new_mask)}][{j}] = {new_reward} (from node {i})")
    
    # --- DEBUG: Print final DP table ---
    logging.debug("--- Final DP Table ---")
    for i in range(k):
        for mask in range(1 << k):
            if dp[mask][i] > float('-inf'):
                logging.debug(f"dp[{bin(mask)}][{i}] ({critical_points[i]['char']}) = {dp[mask][i]}")
    logging.debug("----------------------")

    # --- 5. Find the best final path to E ---
    max_reward = float('-inf')
    last_mask = -1
    last_node_before_end = -1
    end_node_id = 1

    for mask in range(1, 1 << k):
        if not (mask & (1 << end_node_id)):
            for i in range(k):
                if (mask >> i) & 1:
                    if dp[mask][i] > float('-inf') and costs[i][end_node_id]:
                        if dp[mask][i] > max_reward:
                            max_reward = dp[mask][i]
                            last_mask = mask
                            last_node_before_end = i

    logging.info(f"Found best path to E precursor: node {last_node_before_end} with mask {bin(last_mask) if last_mask != -1 else 'N/A'}, reward {max_reward}")

    if last_node_before_end == -1:
        _, path = _find_path_bfs(maze, start_pos, end_pos)
        return path, 0

    # --- 6. Reconstruct the path ---
    logging.info("Reconstructing final path.")
    final_path = []
    path_to_end = costs[last_node_before_end][end_node_id]
    final_path.extend(path_to_end)

    curr_mask = last_mask
    curr_node_idx = last_node_before_end
    
    while curr_node_idx != 0:
        prev_node_idx = parent[curr_mask][curr_node_idx]
        path_segment = costs[prev_node_idx][curr_node_idx]
        final_path.extend(reversed(path_segment[:-1]))
        curr_mask &= ~(1 << curr_node_idx)
        curr_node_idx = prev_node_idx
        
    final_path.reverse()
    
    logging.info("Path reconstruction complete.")
    return final_path, max_reward

def _find_path_bfs(maze, start, end):
    """Finds the shortest path between two points using BFS."""
    q = deque([(start, [start])])
    visited = {start}
    while q:
        (r, c), path = q.popleft()
        if (r, c) == end:
            return 0, path
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and \
               maze[nr][nc] != '#' and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append(((nr, nc), path + [(nr, nc)]))
    return float('-inf'), []

def find_pos(maze, char):
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            if val == char:
                return (r, c)
    return None
