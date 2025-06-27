import logging
from collections import deque
import json

# --- Constants ---
SCORE_MAP = {'G': 10, 'T': -5, 'S': 0, 'E': 0, '.': 0, 'B':0, 'L':0}
MOVE_COST = 0 # As per user request, movement has no cost.

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def solve_with_dp(maze):
    """
    Solves the maze using a Tree-based Dynamic Programming approach.
    The maze is treated as a tree structure with a main path (S to E) and side branches.
    The algorithm finds the path with the maximum possible score.
    """
    height = len(maze)
    width = len(maze[0])

    # 1. Pre-processing: Build graph and find main path
    graph = _build_graph(maze, height, width)
    start_node = _find_char(maze, 'S')
    end_node = _find_char(maze, 'E')
    
    main_path = _find_shortest_path_bfs(graph, start_node, end_node)
    if not main_path:
        logging.warning("No path found from S to E.")
        return [], 0
        
    main_path_set = set(main_path)
    
    # Memoization tables for DP
    memo_away = {}
    memo_to_e = {}
    # Memoization for path reconstruction
    path_decision_memo = {}

    # 2. Core DP Calculation (from E back to S)
    # We build the to_E DP values iteratively from E backwards along the main path.
    for i in range(len(main_path) - 1, -1, -1):
        current_node = main_path[i]
        
        # The parent in the context of "towards E" tree is the next node on the main path
        parent_on_main_path = main_path[i + 1] if i + 1 < len(main_path) else None
        
        _calculate_dp_values(current_node, parent_on_main_path, graph, main_path_set, memo_away, path_decision_memo, maze)

        # Now calculate dp_to_e for the current node
        side_branch_profit = 0
        # The children of current_node for the to_E calculation are its neighbors
        # that are NOT on the main path towards E or S.
        children_of_main_node = [
            n for n in graph[current_node] 
            if n != parent_on_main_path and (i > 0 and n != main_path[i-1])
        ]

        for neighbor in children_of_main_node:
            if neighbor in memo_away and memo_away[neighbor] > 0:
                side_branch_profit += memo_away[neighbor]

        # Get score from the next node on the main path
        next_node_score = memo_to_e.get(parent_on_main_path, 0)
        
        current_score = SCORE_MAP.get(maze[current_node[0]][current_node[1]], 0)
        
        memo_to_e[current_node] = current_score + side_branch_profit + next_node_score

    # 3. Path Reconstruction
    logging.info(f"Path Decision Memo: {path_decision_memo}")
    final_path = _reconstruct_path(start_node, main_path, graph, path_decision_memo)
    max_score = memo_to_e.get(start_node, 0)

    return final_path, max_score


def _calculate_dp_values(u, parent, graph, main_path_set, memo_away, path_decision_memo, maze):
    """
    Recursively calculates dp_away for a node u and its descendants using memoization.
    This explores a branch off the main path.
    """
    if u in memo_away:
        return

    path_decision_memo[u] = {}
    # Recursive step: calculate for all children first
    children = [v for v in graph[u] if v != parent]
    for v in children:
        # A child on a side-branch cannot be on the main path
        if v in main_path_set: continue
        _calculate_dp_values(v, u, graph, main_path_set, memo_away, path_decision_memo, maze)

    # Calculate dp_away[u] using children's values (0/1 Knapsack logic)
    away_profit_from_children = 0
    for v in children:
        if v in main_path_set: continue
        # With no move cost, we take any branch with positive returns.
        if v in memo_away and memo_away[v] > 0:
            away_profit_from_children += memo_away[v]
            path_decision_memo[u][v] = True
        else:
            path_decision_memo[u][v] = False


    u_char = maze[u[0]][u[1]]
    memo_away[u] = SCORE_MAP.get(u_char, 0) + away_profit_from_children


def _reconstruct_path(start_node, main_path, graph, path_decision_memo):
    """
    Reconstructs the final path by walking the main path and dispatching
    to explore profitable side branches based on the decisions made during DP.
    """
    final_path = []
    main_path_set = set(main_path)

    for i in range(len(main_path)):
        current_node = main_path[i]
        final_path.append(current_node)

        # The decisions for branches off the main path are stored in the DP calculation
        # for the main path nodes themselves.
        decisions = path_decision_memo.get(current_node, {})
        logging.info(f"Reconstructing at {current_node}, decisions: {decisions}")
        for neighbor, should_explore in decisions.items():
            if should_explore:
                logging.info(f"  -> Exploring branch at {neighbor}")
                # This neighbor is the root of a profitable side branch.
                branch_excursion = _build_branch_excursion(neighbor, current_node, graph, path_decision_memo)
                final_path.extend(branch_excursion)
                final_path.append(current_node) # Return to the main path node

    return final_path

def _build_branch_excursion(u, parent, graph, path_decision_memo):
    """
    Recursively builds the path for an excursion into a side branch.
    """
    path = [u]
    decisions = path_decision_memo.get(u, {})
    for v, should_explore in decisions.items():
        if should_explore:
            sub_branch_path = _build_branch_excursion(v, u, graph, path_decision_memo)
            path.extend(sub_branch_path)
            path.append(u) # Backtrack to u
    return path


def _build_graph(maze, height, width):
    """Builds a graph representation of the maze."""
    graph = {}
    for r in range(height):
        for c in range(width):
            if maze[r][c] != '#':
                node = (r, c)
                neighbors = []
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < height and 0 <= nc < width and maze[nr][nc] != '#':
                        neighbors.append((nr, nc))
                graph[node] = neighbors
    return graph


def _find_char(maze, char):
    """Finds the first occurrence of a character in the maze."""
    for r, row in enumerate(maze):
        for c, val in enumerate(row):
            if val == char:
                return (r, c)
    return None

def _find_shortest_path_bfs(graph, start, end):
    """Finds the shortest path between two nodes in a graph using BFS."""
    if start not in graph or end not in graph:
        return None
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        current, path = queue.popleft()
        if current == end:
            return path
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append((neighbor, new_path))
    return None

def json_loader(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data["maze"]

if __name__ == "__main__":
    maze = json_loader("D:\\1-sjh-workspace\\maze-game\\test\\dp_test\\result_maze_15_15_2_formatted.json")
    final_path, max_score = solve_with_dp(maze)
    print(f"Final Path: {final_path}")
    print(f"Maximum Score: {max_score}")