# battle_logic.py
import math
import random

# Type effectiveness multipliers
TYPE_MULTIPLIERS = {
    "normal": {"rock": 0.5, "ghost": 0, "steel": 0.5},
    "fire": {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 2, "bug": 2, "rock": 0.5, "dragon": 0.5, "steel": 2},
    "water": {"fire": 2, "water": 0.5, "grass": 0.5, "ground": 2, "rock": 2, "dragon": 0.5},
    "electric": {"water": 2, "electric": 0.5, "grass": 0.5, "ground": 0, "flying": 2, "dragon": 0.5},
    "grass": {"fire": 0.5, "water": 2, "grass": 0.5, "poison": 0.5, "ground": 2, "flying": 0.5, "bug": 0.5, "rock": 2, "dragon": 0.5, "steel": 0.5},
    "ice": {"fire": 0.5, "water": 0.5, "grass": 2, "ice": 0.5, "ground": 2, "flying": 2, "dragon": 2, "steel": 0.5},
    "fighting": {"normal": 2, "ice": 2, "poison": 0.5, "flying": 0.5, "psychic": 0.5, "bug": 0.5, "rock": 2, "ghost": 0, "dark": 2, "steel": 2, "fairy": 0.5},
    "poison": {"grass": 2, "poison": 0.5, "ground": 0.5, "rock": 0.5, "ghost": 0.5, "steel": 0, "fairy": 2},
    "ground": {"fire": 2, "electric": 2, "grass": 0.5, "poison": 2, "flying": 0, "bug": 0.5, "rock": 2, "steel": 2},
    "flying": {"electric": 0.5, "grass": 2, "fighting": 2, "bug": 2, "rock": 0.5, "steel": 0.5},
    "psychic": {"fighting": 2, "poison": 2, "psychic": 0.5, "dark": 0, "steel": 0.5},
    "bug": {"fire": 0.5, "grass": 2, "fighting": 0.5, "poison": 0.5, "flying": 0.5, "psychic": 2, "ghost": 0.5, "steel": 0.5, "fairy": 0.5},
    "rock": {"fire": 2, "ice": 2, "fighting": 0.5, "ground": 0.5, "flying": 2, "bug": 2, "steel": 0.5},
    "ghost": {"normal": 0, "fighting": 0, "poison": 2, "bug": 2, "ghost": 2, "dark": 0.5},
    "dragon": {"dragon": 2, "steel": 0.5, "fairy": 0},
    "steel": {"fire": 0.5, "water": 0.5, "electric": 0.5, "ice": 2, "rock": 2, "steel": 0.5, "fairy": 2},
    "fairy": {"fire": 0.5, "fighting": 2, "poison": 0.5, "dragon": 2, "dark": 2, "steel": 0.5}
}

# A simple dictionary to map moves to a type and a base power.
# This is a critical addition for accurate damage calculation.
MOVES_DATA = {
    "tackle": {"type": "normal", "power": 40},
    "vine-whip": {"type": "grass", "power": 45},
    "flamethrower": {"type": "fire", "power": 90},
    "water-gun": {"type": "water", "power": 40},
    "thunderbolt": {"type": "electric", "power": 90},
    "scratch": {"type": "normal", "power": 40},
    "ember": {"type": "fire", "power": 40},
    "ice-beam": {"type": "ice", "power": 90},
    "body-slam": {"type": "normal", "power": 85},
    "hydro-pump": {"type": "water", "power": 110},
    "razor-leaf": {"type": "grass", "power": 55},
    "double-edge": {"type": "normal", "power": 120},
    "peck": {"type": "flying", "power": 35},
    "poison-sting": {"type": "poison", "power": 15},
    "thunder-shock": {"type": "electric", "power": 40},
    "earthquake": {"type": "ground", "power": 100},
    "confusion": {"type": "psychic", "power": 50},
    "wing-attack": {"type": "flying", "power": 60},
    "hyper-beam": {"type": "normal", "power": 150},
    # Add status effect moves
    "poison-powder": {"type": "poison", "power": 0, "status": "poison"},
    "thunder-wave": {"type": "electric", "power": 0, "status": "paralysis"},
    "flame-wheel": {"type": "fire", "power": 60, "status": "burn"}
}

def get_type_effectiveness(attacking_type, defending_types):
    """
    Calculates the total damage multiplier based on type matchups.
    """
    modifier = 1.0
    for defending_type in defending_types:
        if attacking_type in TYPE_MULTIPLIERS and defending_type in TYPE_MULTIPLIERS[attacking_type]:
            modifier *= TYPE_MULTIPLIERS[attacking_type][defending_type]
    return modifier

def calculate_damage(attacker, defender, move_data, type_effectiveness, level=50):
    """
    Calculates the damage dealt using a simplified formula.
    """
    move_power = move_data.get("power", 0)
    
    # Check if the move is a status move (power 0)
    if move_power == 0:
        return 0

    # Determine if the move is physical or special based on move type
    # For a more robust simulation, you'd have a separate moves.json.
    # We'll make a simplified assumption for this project:
    physical_types = ["normal", "fighting", "flying", "poison", "ground", "rock", "bug", "ghost", "steel", "dragon"]
    
    if move_data['type'] in physical_types:
        attack_stat = attacker['stats']['attack']
        defense_stat = defender['stats']['defense']
    else:
        attack_stat = attacker['stats']['special-attack']
        defense_stat = defender['stats']['special-defense']

    # Simplified damage formula
    damage = ((((2 * level / 5) + 2) * attack_stat * move_power) / defense_stat) / 50
    
    # Apply type effectiveness multiplier
    damage *= type_effectiveness
    
    # Add a random modifier (0.85 to 1.0)
    damage *= random.uniform(0.85, 1.0)
    
    return max(1, math.floor(damage))

def simulate_battle(p1_name: str, p2_name: str, pokemon_data: dict) -> dict:
    """
    Simulates a battle between two Pokémon and returns a detailed log.
    """
    log = []
    
    # Get Pokémon data and initialize battle state
    p1 = pokemon_data.get(p1_name)
    p2 = pokemon_data.get(p2_name)

    # Initialize stats for battle simulation
    p1_state = {"name": p1['name'], "hp": p1['stats']['hp'], "status": None}
    p2_state = {"name": p2['name'], "hp": p2['stats']['hp'], "status": None}
    
    # Initial log messages
    log.append(f"A wild {p1_state['name'].capitalize()} and {p2_state['name'].capitalize()} are ready to battle!")
    log.append(f"{p1_state['name'].capitalize()} has {p1_state['hp']} HP.")
    log.append(f"{p2_state['name'].capitalize()} has {p2_state['hp']} HP.")
    log.append("---")

    # Determine turn order based on Speed
    if p1['stats']['speed'] > p2['stats']['speed']:
        turn_order = [p1_state, p2_state]
        pokemon_stats_map = {p1_state['name']: p1, p2_state['name']: p2}
    else:
        turn_order = [p2_state, p1_state]
        pokemon_stats_map = {p1_state['name']: p1, p2_state['name']: p2}

    log.append(f"{turn_order[0]['name'].capitalize()} is faster and will go first!")

    # Start the turn loop
    turn_count = 0
    while p1_state['hp'] > 0 and p2_state['hp'] > 0 and turn_count < 100:
        turn_count += 1
        log.append(f"\n--- Turn {turn_count} ---")
        
        # Apply status effects at the start of the turn
        for p_state in turn_order:
            if p_state['status'] == 'poison' and p_state['hp'] > 0:
                poison_damage = math.floor(p_state['hp'] * 0.1) # 10% of current HP
                p_state['hp'] -= poison_damage
                log.append(f"{p_state['name'].capitalize()} is hurt by poison! It lost {poison_damage} HP.")
            elif p_state['status'] == 'burn' and p_state['hp'] > 0:
                burn_damage = math.floor(p_state['hp'] * 0.1) # 10% of current HP
                p_state['hp'] -= burn_damage
                log.append(f"{p_state['name'].capitalize()} is hurt by its burn! It lost {burn_damage} HP.")
        
        # Check if the battle ended due to status effects
        if p1_state['hp'] <= 0 or p2_state['hp'] <= 0:
            break

        for i in range(2):
            attacker_state = turn_order[i]
            defender_state = turn_order[(i+1)%2]
            
            attacker_info = pokemon_stats_map[attacker_state['name']]
            defender_info = pokemon_stats_map[defender_state['name']]

            # Paralysis check
            if attacker_state['status'] == 'paralysis' and random.random() < 0.25:
                log.append(f"{attacker_state['name'].capitalize()} is paralyzed and can't move!")
                continue # Skip this attack

            # Choose a random move
            move_name = random.choice(attacker_info['moves'])
            move_data = MOVES_DATA.get(move_name, {"type": "normal", "power": 40}) # Default to a generic move

            # Apply a status effect if the move has one
            if "status" in move_data:
                defender_state['status'] = move_data['status']
                log.append(f"{attacker_state['name'].capitalize()} used {move_name}, inflicting {defender_state['status']} on {defender_state['name'].capitalize()}!")
            
            # Calculate and apply damage
            type_eff = get_type_effectiveness(move_data['type'], defender_info['types'])
            damage_dealt = calculate_damage(attacker_info, defender_info, move_data, type_eff)
            
            defender_state['hp'] -= damage_dealt
            log.append(f"{attacker_state['name'].capitalize()} used {move_name}, dealing {damage_dealt} damage.")

            # Check if the defender fainted
            if defender_state['hp'] <= 0:
                break
        
        # Update HP in log
        log.append(f"HP: {p1_state['name'].capitalize()} {max(0, p1_state['hp'])} | {p2_state['name'].capitalize()} {max(0, p2_state['hp'])}")
    
    # Determine the winner
    winner = None
    if p1_state['hp'] <= 0:
        winner = p2_state['name'].capitalize()
    elif p2_state['hp'] <= 0:
        winner = p1_state['name'].capitalize()
    
    if winner:
        log.append("---")
        log.append(f"Battle over! The winner is {winner}!")
    else:
        log.append("---")
        log.append("The battle ended in a stalemate!")

    return {
        "battle_log": log,
        "winner": winner
    }