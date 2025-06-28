import heapq
import math
import json

class State:
    """
    Represents a state in the search space of the boss rush problem.
    A state is defined by the current boss, their HP, skill cooldowns, and time elapsed.
    """
    def __init__(self, boss_index, boss_hp, skill_cooldowns, time_elapsed, path):
        self.boss_index = boss_index
        self.boss_hp = boss_hp
        self.skill_cooldowns = tuple(skill_cooldowns)  # Use tuple to make it hashable
        self.time_elapsed = time_elapsed
        self.path = path # List of (time, skill_name) tuples

    # The __lt__ method is needed for the object to be orderable by the priority queue (heapq)
    # when two priorities are the same. This is a fallback comparison.
    def __lt__(self, other):
        return self.time_elapsed < other.time_elapsed
    
def calculate_lower_bound(state, bosses, skills, max_potential_dps):
    """
    Calculates a lower bound on the total time to complete the boss rush from the current state.
    This is the core of the "bound" part of the algorithm.
    """
    if max_potential_dps == 0:
        return float('inf')

    # Calculate total remaining HP from the current boss onwards
    remaining_hp = state.boss_hp
    for i in range(state.boss_index + 1, len(bosses)):
        remaining_hp += bosses[i]

    # Estimate time to deal remaining damage with maximum possible DPS
    estimated_time_to_finish = remaining_hp / max_potential_dps

    # The lower bound is the time already elapsed plus the optimistic estimate to finish
    return state.time_elapsed + estimated_time_to_finish

def solve_boss_battle(bosses_list, skills_list, turn_limit=20):
    """
    Solves the boss rush problem using a Branch and Bound algorithm.

    Args:
        bosses_list (list): A list of integers for each boss's health.
        skills_list (list): A list of lists, where each inner list is [harm, cooldown, name].

    Returns:
        A tuple containing:
        - The minimum time to defeat all bosses.
        - The optimal sequence of skill uses (path).
    """
    num_bosses = len(bosses_list)
    num_skills = len(skills_list)

    # --- Pre-calculation for the Lower Bound ---
    # Calculate a theoretical maximum DPS to use in the bounding function.
    # We add 1 to cooldown to account for the time step of using the skill.
    max_potential_dps = sum(harm / (cooldown + 1) for harm, cooldown in skills_list if (cooldown + 1) > 0)
    if max_potential_dps == 0 and sum(bosses_list) > 0:
        print("No skills with positive damage. Cannot defeat bosses.")
        return float('inf'), []

    # --- Initialization ---
    initial_state = State(
        boss_index=0,
        boss_hp=bosses_list[0],
        skill_cooldowns=[0] * num_skills,
        time_elapsed=0,
        path=[]
    )

    min_completion_time = float('inf')
    best_path = []

    # The priority queue will store tuples of (lower_bound, state)
    priority_queue = []
    initial_lower_bound = calculate_lower_bound(initial_state, bosses_list, skills_list, max_potential_dps)
    heapq.heappush(priority_queue, (initial_lower_bound, initial_state))

    # Visited set to store (boss_index, boss_hp, skill_cooldowns) tuples to avoid cycles
    # and redundant computations.
    visited = set()

    # --- Main Algorithm Loop ---
    while priority_queue:
        current_lower_bound, current_state = heapq.heappop(priority_queue)

        # --- Pruning Step 1 ---
        # If the current best possible time is already worse than the best solution found, prune.
        if current_lower_bound >= min_completion_time:
            continue

        # Create a hashable representation of the core state properties
        visited_key = (current_state.boss_index, current_state.boss_hp, current_state.skill_cooldowns)
        if visited_key in visited:
            continue
        visited.add(visited_key)

        # --- Branching Step ---
        # Find skills that are ready to use (cooldown is 0)
        ready_skills_indices = [i for i, cd in enumerate(current_state.skill_cooldowns) if cd == 0]

        if not ready_skills_indices:
            # If no skills are ready, we must wait.
            # Advance time to the moment the next skill becomes available.
            min_wait_time = min(cd for cd in current_state.skill_cooldowns if cd > 0)
            
            new_time = current_state.time_elapsed + min_wait_time
            new_cooldowns = [max(0, cd - min_wait_time) for cd in current_state.skill_cooldowns]
            
            next_state = State(
                boss_index=current_state.boss_index,
                boss_hp=current_state.boss_hp,
                skill_cooldowns=new_cooldowns,
                time_elapsed=new_time,
                path=current_state.path
            )

            # --- Pruning Step 2 (for the waiting state) ---
            next_lower_bound = calculate_lower_bound(next_state, bosses_list, skills_list, max_potential_dps)
            if next_lower_bound < min_completion_time:
                heapq.heappush(priority_queue, (next_lower_bound, next_state))

        else:
            # Explore using each ready skill
            for skill_idx in ready_skills_indices:
                harm, cooldown = skills_list[skill_idx]

                # --- Create a new state by using the skill ---
                # Assume using a skill takes 1 time unit
                time_step = 1
                new_time = current_state.time_elapsed + time_step

                # Reduce cooldowns for all skills by the time step
                new_cooldowns = list(current_state.skill_cooldowns)
                for i in range(num_skills):
                    new_cooldowns[i] = max(0, new_cooldowns[i] - time_step)
                
                # Apply skill damage and set its cooldown
                new_boss_hp = current_state.boss_hp - harm
                new_cooldowns[skill_idx] = cooldown
                new_path = current_state.path + [(current_state.time_elapsed, skill_idx)]
                
                new_boss_index = current_state.boss_index
                
                # --- Check for Boss Defeat ---
                if new_boss_hp <= 0:
                    # Move to the next boss
                    new_boss_index += 1
                    if new_boss_index < num_bosses:
                        new_boss_hp = bosses_list[new_boss_index]
                    else:
                        # --- Goal Reached: All bosses defeated ---
                        if new_time < min_completion_time:
                            min_completion_time = new_time
                            best_path = new_path
                        continue # This branch is complete, no need to add to queue

                # --- Create and push the new state to the queue ---
                next_state = State(new_boss_index, new_boss_hp, new_cooldowns, new_time, new_path)

                # --- Pruning Step 2 (for the skill-use state) ---
                next_lower_bound = calculate_lower_bound(next_state, bosses_list, skills_list, max_potential_dps)
                if next_lower_bound < min_completion_time:
                    heapq.heappush(priority_queue, (next_lower_bound, next_state))

    return min_completion_time, best_path

def json_loader(json_file):
    """
    Converts a JSON file to a Python object.
    Args:
        json_file (str): Path to the JSON file to be converted.
    Returns:
        tuple: A tuple containing the constraints and the password.
    Example: password = [2, 0, 5], constraints = [[-1, -1], [0, 0], [1, 1], [2, -1, -1], [-1, 2, -1], [-1, -1, 5]]
    """
    """
    json style:
    {
  "B": [11, 13, 8, 17],
  "PlayerSkills": [
    [6, 2],
    [2, 0],
    [4, 1]
  ],
  "min_turns": 13,
  "actions": [0, 2, 1, 2, 0, 2, 1, 0, 1, 2, 0, 1, 2]
}
    """
    with open(json_file, 'r') as file:
        data = json.load(file)
    bosses = data["B"]
    skills = data["PlayerSkills"]

    return bosses, skills

if __name__ == "__main__":
    json_file = "file_path"
    bosses, skills = json_loader(json_file)
    min_time, path = solve_boss_battle(bosses, skills)
    print(f"Minimum time to defeat all bosses: {min_time}")
    print("Optimal skill usage path:")
    # print(f"actions: {path}")
    for time, skill_idx in path:
        print(f"At time {time}: use skill {skill_idx}")
