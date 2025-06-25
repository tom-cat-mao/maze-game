from collections import deque
import heapq

def solve_with_dp(maze):
    """
    Finds the path with the maximum possible reward from 'S' to 'E' using
    State Compression Dynamic Programming. This approach correctly handles the
    "items can only be collected once" rule by encoding the set of visited
    special nodes (Gems/Traps) into the DP state.

    This algorithm is guaranteed to find the optimal path but has a time
    complexity of O(k^2 * 2^k), where k is the number of special nodes.
    It is suitable for a small number of special nodes.
    """
    height = len(maze)
    width = len(maze[0])
    value_map = {'G': 10, 'T': -5}

    # --- 1. Identify all special nodes and assign IDs ---
    special_nodes = []
    node_positions = {}
    start_pos = find_pos(maze, 'S')
    end_pos = find_pos(maze, 'E')

    for r in range(height):
        for c in range(width):
            if maze[r][c] in ['G', 'T']:
                node_id = len(special_nodes)
                special_nodes.append({'id': node_id, 'pos': (r, c), 'char': maze[r][c]})
                node_positions[(r, c)] = node_id

    k = len(special_nodes)
    if k == 0: # No special nodes, just find a simple path
        return _bfs_simple(maze, start_pos, end_pos)

    # --- 2. Pre-calculate costs (path and value) between all pairs of special nodes ---
    # cost[i][j] = (path_value, path_list)
    costs = [[(float('-inf'), []) for _ in range(k)] for _ in range(k)]

    for i in range(k):
        for j in range(i, k):
            if i == j:
                costs[i][j] = (0, [special_nodes[i]['pos']])
            else:
                path_val, path = _bfs_path_cost(maze, special_nodes[i]['pos'], special_nodes[j]['pos'], node_positions)
                costs[i][j] = (path_val, path)
                costs[j][i] = (path_val, path) # Assuming symmetric paths

    # Costs from Start (S) and to End (E)
    start_costs = [_bfs_path_cost(maze, start_pos, node['pos'], node_positions) for node in special_nodes]
    end_costs = [_bfs_path_cost(maze, node['pos'], end_pos, node_positions) for node in special_nodes]

    # --- 3. Initialize DP table ---
    # dp[mask][i] = max_reward to visit nodes in mask, ending at node i
    dp = [[float('-inf')] * k for _ in range(1 << k)]
    parent = [[None] * k for _ in range(1 << k)]

    for i in range(k):
        # Initial move from Start to first special node
        path_val, _ = start_costs[i]
        if path_val != float('-inf'):
            dp[1 << i][i] = path_val + value_map[special_nodes[i]['char']]

    # --- 4. State Compression DP main loop ---
    for mask in range(1, 1 << k):
        for i in range(k):
            if (mask >> i) & 1:  # If node i is in the current set (mask)
                if dp[mask][i] == float('-inf'):
                    continue
                for j in range(k):
                    if not ((mask >> j) & 1):  # If node j is NOT in the current set
                        path_val, _ = costs[i][j]
                        if path_val != float('-inf'):
                            new_mask = mask | (1 << j)
                            new_reward = dp[mask][i] + path_val + value_map[special_nodes[j]['char']]
                            if new_reward > dp[new_mask][j]:
                                dp[new_mask][j] = new_reward
                                parent[new_mask][j] = i

    # --- 5. Find the best final path ---
    max_reward = float('-inf')
    last_mask = -1
    last_node = -1

    for mask in range(1, 1 << k):
        for i in range(k):
            if dp[mask][i] != float('-inf'):
                path_val, _ = end_costs[i]
                if path_val != float('-inf'):
                    final_reward = dp[mask][i] + path_val
                    if final_reward > max_reward:
                        max_reward = final_reward
                        last_mask = mask
                        last_node = i
    
    if last_node == -1: # No path found that goes through any special node
        return _bfs_simple(maze, start_pos, end_pos)

    # --- 6. Reconstruct the path ---
    final_path = []
    path_to_end, _ = end_costs[last_node]
    final_path_segment = _bfs_path_cost(maze, special_nodes[last_node]['pos'], end_pos, node_positions)[1]
    final_path.extend(final_path_segment)

    curr_mask = last_mask
    curr_node_idx = last_node
    while curr_mask > 0:
        prev_node_idx = parent[curr_mask][curr_node_idx]
        
        if prev_node_idx is None: # Reached the first special node
            path_segment = _bfs_path_cost(maze, start_pos, special_nodes[curr_node_idx]['pos'], node_positions)[1]
            final_path.extend(path_segment[:-1]) # Exclude last element to avoid dupes
            break
        
        path_segment = _bfs_path_cost(maze, special_nodes[prev_node_idx]['pos'], special_nodes[curr_node_idx]['pos'], node_positions)[1]
        final_path.extend(path_segment[:-1]) # Exclude last element
        
        curr_mask &= ~(1 << curr_node_idx)
        curr_node_idx = prev_node_idx
        
    final_path.reverse()
    
    # The value of E is not added to the total, as it's the destination.
    return final_path, max_reward


def _bfs_path_cost(maze, start, end, special_positions):
    """Calculates cost of path between two points, avoiding other special points."""
    q = deque([(start, [start])])
    visited = {start}
    while q:
        (r, c), path = q.popleft()
        if (r, c) == end:
            return 0, path # Path value is 0 as G/T are handled by DP
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and \
               maze[nr][nc] != '#' and (nr, nc) not in visited:
                # Path cannot go through OTHER special nodes
                if (nr, nc) in special_positions and (nr, nc) != end:
                    continue
                visited.add((nr, nc))
                q.append(((nr, nc), path + [(nr, nc)]))
    return float('-inf'), []

def _bfs_simple(maze, start, end):
    """Fallback for mazes with no special nodes."""
    q = deque([(start, [start])])
    visited = {start}
    while q:
        (r, c), path = q.popleft()
        if (r, c) == end:
            return path, 0
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and \
               maze[nr][nc] != '#' and (nr, nc) not in visited:
                visited.add((nr, nc))
                q.append(((nr, nc), path + [(nr, nc)]))
    return [], 0

def find_pos(maze, char):
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            if val == char:
                return (r, c)
    return None
