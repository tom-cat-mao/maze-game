import pytest
from app.algorithms.boss_battle import solve_boss_battle

def test_solve_boss_battle_simple():
    """
    Tests a simple boss battle scenario where the optimal path is clear.
    """
    boss_hp = 50
    skills = [
        {"name": "Quick Attack", "damage": 10, "cooldown": 0},
        {"name": "Heavy Slam", "damage": 25, "cooldown": 1}, # Cooldown of 1 means cannot use for 1 turn after use
    ]
    
    # Optimal sequence should be: Heavy Slam, Quick Attack, Heavy Slam
    # Turn 1: Heavy Slam (HP: 50-25=25). Heavy Slam is on cooldown for Turn 2.
    # Turn 2: Quick Attack (HP: 25-10=15). Heavy Slam is now available.
    # Turn 3: Heavy Slam (HP: 15-25=-10). Boss defeated.
    # Total turns: 3
    expected_sequence = ["Heavy Slam", "Quick Attack", "Heavy Slam"]
    expected_turns = 3
    
    sequence, turns = solve_boss_battle(boss_hp, skills)
    
    assert turns == expected_turns
    assert sequence == expected_sequence

def test_boss_battle_no_solution():
    """
    Tests a scenario where the boss cannot be defeated in a reasonable number of turns.
    """
    boss_hp = 100
    skills = [
        {"name": "Weak Hit", "damage": 1, "cooldown": 0},
    ]
    # This would take 100 turns. The algorithm should have a turn limit to prevent long runs.
    # Let's assume a default limit of 20 turns.
    
    sequence, turns = solve_boss_battle(boss_hp, skills, turn_limit=20)
    
    assert sequence is None
    assert turns is None
