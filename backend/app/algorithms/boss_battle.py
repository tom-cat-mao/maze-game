import heapq

def solve_boss_battle(boss_hp, skills, turn_limit=20):
    """
    Finds the optimal sequence of skills to defeat a boss using Branch and Bound.
    """
    
    # Heuristic function: estimated turns to win (best case scenario)
    max_damage_per_turn = max(skill['damage'] for skill in skills) if skills else 1
    def h(hp):
        return (hp / max_damage_per_turn) if max_damage_per_turn > 0 else float('inf')

    # State: (f_cost, g_cost, hp, cooldowns_tuple, path_list)
    # g_cost is the number of turns taken so far.
    # cooldowns are stored as a tuple to be hashable for the visited set.
    initial_cooldowns = tuple([0] * len(skills))
    
    # Priority queue for the frontier, ordered by f_cost
    pq = [(h(boss_hp), 0, boss_hp, initial_cooldowns, [])]
    
    # Visited set to avoid re-exploring the same state (hp, cooldowns)
    visited = set()

    while pq:
        f_cost, g_cost, current_hp, current_cooldowns, path = heapq.heappop(pq)

        if (current_hp, current_cooldowns) in visited:
            continue
        
        visited.add((current_hp, current_cooldowns))

        if g_cost >= turn_limit:
            continue

        # Decrement cooldowns for the next turn
        next_cooldowns_list = [max(0, c - 1) for c in current_cooldowns]

        # Explore using each available skill
        for i, skill in enumerate(skills):
            if current_cooldowns[i] == 0:
                new_hp = current_hp - skill['damage']
                new_path = path + [skill['name']]
                
                if new_hp <= 0:
                    # Solution found
                    return new_path, g_cost + 1

                new_cooldowns_list = list(next_cooldowns_list)
                new_cooldowns_list[i] = skill['cooldown']
                new_cooldowns = tuple(new_cooldowns_list)
                
                new_g = g_cost + 1
                new_f = new_g + h(new_hp)
                
                heapq.heappush(pq, (new_f, new_g, new_hp, new_cooldowns, new_path))

    return None, None # No solution found within the turn limit
