import logging
from collections import deque

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def solve_with_dp(maze):
    """
    Finds the path with the maximum possible reward from 'S' to 'E' using
    State Compression Dynamic Programming. The end node 'E' is treated as the
    final destination and not as an intermediate step.
    """
    logging.info("DP solver started: Refactored Logic")
    height = len(maze)
    width = len(maze[0])
    value_map = {'G': 10, 'T': -5}

    # --- 1. Identify critical points (S, G, T) and End Point (E) ---
    start_pos = find_pos(maze, 'S')
    end_pos = find_pos(maze, 'E')

    if not start_pos or not end_pos:
        logging.error("Start or End node not found in maze.")
        return [], 0

    # Critical points for DP now only include S, G, and T
    critical_points = [{'id': 0, 'pos': start_pos, 'char': 'S'}]
    pos_to_id = {start_pos: 0}
    
    for r in range(height):
        for c in range(width):
            if maze[r][c] in value_map:
                node_id = len(critical_points)
                critical_points.append({'id': node_id, 'pos': (r, c), 'char': maze[r][c]})
                pos_to_id[(r, c)] = node_id
    
    k = len(critical_points)
    logging.info(f"Found {k} critical points (S, G, T). End point E is separate.")
    
    # If only S exists, just find a direct path to E
    if k <= 1:
        _, path = _find_path_bfs(maze, start_pos, end_pos)
        return (path, 0) if path else ([], 0)

    # --- 2. Pre-calculate paths ---
    all_critical_pos = {p['pos'] for p in critical_points}

    # a) Between all pairs of critical points (S, G, T)
    costs = [[None] * k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            if i == j: continue
            # Path should not go through other critical points or the end point
            start_pos_i = critical_points[i]['pos']
            end_pos_j = critical_points[j]['pos']
            avoid_points = (all_critical_pos - {start_pos_i, end_pos_j}) | {end_pos}
            _, path = _find_path_bfs(maze, start_pos_i, end_pos_j, avoid_points=avoid_points)
            costs[i][j] = path
    
    # b) From each critical point to the end point 'E'
    costs_to_end = [None] * k
    for i in range(k):
        # Path should not go through other critical points
        start_pos_i = critical_points[i]['pos']
        avoid_points = all_critical_pos - {start_pos_i}
        _, path = _find_path_bfs(maze, start_pos_i, end_pos, avoid_points=avoid_points)
        costs_to_end[i] = path

    logging.info("Finished pre-calculating costs.")

    # --- 3. Initialize DP table ---
    dp = [[float('-inf')] * k for _ in range(1 << k)]
    parent = [[None] * k for _ in range(1 << k)]
    dp[1][0] = 0  # Mask for S (id 0) is 1, reward is 0

    # --- 4. State Compression DP main loop (only on S, G, T) ---
    logging.info("Starting State Compression DP main loop.")
    for mask in range(1, 1 << k):
        for i in range(k):
            if not ((mask >> i) & 1): continue
            if dp[mask][i] == float('-inf'): continue
            
            for j in range(k):
                if not ((mask >> j) & 1): # If j is not visited
                    if costs[i][j]: # And a path from i to j exists
                        new_mask = mask | (1 << j)
                        reward = value_map.get(critical_points[j]['char'], 0)
                        new_reward = dp[mask][i] + reward
                        
                        if new_reward > dp[new_mask][j]:
                            dp[new_mask][j] = new_reward
                            parent[new_mask][j] = i
    
    # --- 5. Find the best final path to E ---
    max_reward = float('-inf')
    final_mask = -1
    last_node_idx = -1

    # Check every state (mask, i) and see what the total reward would be if we go to E from there
    for mask in range(1, 1 << k):
        for i in range(k):
            # If state is reachable and there's a path from i to E
            if dp[mask][i] > float('-inf') and costs_to_end[i]:
                # Total reward is the reward accumulated so far
                current_reward = dp[mask][i]
                if current_reward > max_reward:
                    max_reward = current_reward
                    final_mask = mask
                    last_node_idx = i

    # If no path to E could be constructed
    if last_node_idx == -1:
        _, path = _find_path_bfs(maze, start_pos, end_pos)
        return (path, 0) if path else ([], 0)

    # --- 6. Reconstruct the path ---
    # a) Backtrack from the last node to Start
    path_segment_to_last_node = []
    path_nodes = []
    curr_mask = final_mask
    curr_node_idx = last_node_idx

    while curr_node_idx is not None:
        path_nodes.append(curr_node_idx)
        prev_node_idx = parent[curr_mask][curr_node_idx]
        if prev_node_idx is None:
            break
        curr_mask &= ~(1 << curr_node_idx)
        curr_node_idx = prev_node_idx
    
    path_nodes.reverse()

    # b) Stitch together the path from S to the last node
    for i in range(len(path_nodes) - 1):
        start_node_id = path_nodes[i]
        end_node_id_segment = path_nodes[i+1]
        segment = costs[start_node_id][end_node_id_segment]
        if not path_segment_to_last_node:
            path_segment_to_last_node.extend(segment)
        else:
            path_segment_to_last_node.extend(segment[1:])

    # c) Append the final leg from the last node to E
    final_leg_to_end = costs_to_end[last_node_idx]
    if not path_segment_to_last_node: # Case where S is the last_node
         final_path = final_leg_to_end
    else:
         final_path = path_segment_to_last_node + final_leg_to_end[1:]

    return final_path, max_reward

def _find_path_bfs(maze, start, end, avoid_points=None):
    """
    Finds the shortest path between two points using BFS, avoiding a given set of points.
    """
    if not start or not end: return float('-inf'), []
    
    q = deque([(start, [start])])
    visited = {start}
    if avoid_points:
        visited.update(avoid_points)

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
