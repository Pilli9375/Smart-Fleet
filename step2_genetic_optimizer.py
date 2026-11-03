# ==============================================================================
# Step 2: Multi-Objective Genetic Algorithm (NSGA-II Style Pareto Optimizer)
# Subject: Soft Computing Project (College Level)
# ==============================================================================

import math
import random
from step1_fuzzy_data import stops, depot, get_fuzzy_satisfaction

# Quick lookup map: stop_id -> stop dictionary details
STOP_MAP = {s["id"]: s for s in stops}


# ------------------------------------------------------------------------------
# 1. Distance & Route Evaluation Function
# ------------------------------------------------------------------------------
def euclidean_distance(x1, y1, x2, y2):
    """Calculates straight-line distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def evaluate_solution(route_order, max_van_capacity=100):
    """
    Evaluates a given route order (e.g., [3, 1, 7, 2, ...]).
    
    1. Splits stops into separate vans when capacity (100 kg) is exceeded.
    2. Calculates Total Energy Cost (heavier vans burn more energy per km).
    3. Calculates Average Fuzzy Customer Satisfaction based on arrival times.
    """
    # Step A: Split route into separate vans according to capacity
    vans = []
    current_van = []
    current_weight = 0

    for stop_id in route_order:
        stop = STOP_MAP[stop_id]
        if current_weight + stop["weight"] <= max_van_capacity:
            current_van.append(stop_id)
            current_weight += stop["weight"]
        else:
            # Current van is full; start a new van
            vans.append(current_van)
            current_van = [stop_id]
            current_weight = stop["weight"]

    if current_van:
        vans.append(current_van)

    # Step B: Simulate each van's journey starting and returning to Central Depot
    total_energy_cost = 0.0
    all_satisfactions = []

    for van_stops in vans:
        current_time = 0.0
        current_x = depot["x"]
        current_y = depot["y"]

        # Initial load = sum of weights of packages this van is carrying
        current_load = sum(STOP_MAP[sid]["weight"] for sid in van_stops)

        # Visit each stop assigned to this van
        for sid in van_stops:
            stop = STOP_MAP[sid]
            dist = euclidean_distance(current_x, current_y, stop["x"], stop["y"])

            # Rule: 1 distance unit = 1 minute of travel
            current_time += dist

            # Score 1: Energy cost increases with remaining package weight
            leg_energy = dist * (1 + 0.005 * current_load)
            total_energy_cost += leg_energy

            # Package delivered: reduce current load
            current_load -= stop["weight"]

            # Score 2: Fuzzy satisfaction for this stop
            sat = get_fuzzy_satisfaction(
                arrival_time=current_time,
                best_start=stop["best_start"],
                best_end=stop["best_end"],
                max_late=stop["max_late"]
            )
            all_satisfactions.append(sat)

            # Update van's current location
            current_x, current_y = stop["x"], stop["y"]

        # Return journey back to Central Depot (van is now empty, load = 0)
        return_dist = euclidean_distance(current_x, current_y, depot["x"], depot["y"])
        total_energy_cost += return_dist * (1 + 0.005 * 0)

    # Calculate fleet-wide average satisfaction (0.0 to 1.0)
    avg_satisfaction = sum(all_satisfactions) / len(all_satisfactions)

    return round(total_energy_cost, 2), round(avg_satisfaction, 3), vans


# ------------------------------------------------------------------------------
# 2. Genetic Operators (Crossover & Mutation)
# ------------------------------------------------------------------------------
def order_crossover(parent1, parent2):
    """
    Order Crossover (OX) for Permutations:
    Ensures every stop from 1 to 10 appears exactly once without duplicates.
    """
    size = len(parent1)
    # Pick two random cut points
    cut1, cut2 = sorted(random.sample(range(size), 2))

    # Copy segment from parent1 to child
    child = [None] * size
    child[cut1:cut2 + 1] = parent1[cut1:cut2 + 1]

    # Fill remaining spots using stops from parent2 in their existing order
    p2_index = 0
    for i in range(size):
        if child[i] is None:
            while parent2[p2_index] in child:
                p2_index += 1
            child[i] = parent2[p2_index]

    return child


def swap_mutation(route, mutation_rate=0.2):
    """Randomly swaps two stops in the route with probability = mutation_rate."""
    mutated = list(route)
    if random.random() < mutation_rate:
        idx1, idx2 = random.sample(range(len(mutated)), 2)
        mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
    return mutated


# ------------------------------------------------------------------------------
# 3. Multi-Objective Pareto Dominance & Optimizer (NSGA-II Style)
# ------------------------------------------------------------------------------
def dominates(sol_a, sol_b):
    """
    A dominates B if:
    1. A is at least as good as B in both objectives (Lower Energy, Higher Satisfaction).
    2. A is strictly better in at least one objective.
    """
    better_or_equal = (sol_a["energy"] <= sol_b["energy"]) and (sol_a["satisfaction"] >= sol_b["satisfaction"])
    strictly_better = (sol_a["energy"] < sol_b["energy"]) or (sol_a["satisfaction"] > sol_b["satisfaction"])
    return better_or_equal and strictly_better


def run_optimizer(pop_size=40, generations=50):
    """
    Multi-Objective Genetic Algorithm:
    Evolves routes to simultaneously minimize Energy Cost & maximize Customer Satisfaction.
    """
    all_stop_ids = [s["id"] for s in stops]

    # Step 1: Create initial random population
    population = []
    for _ in range(pop_size):
        individual = list(all_stop_ids)
        random.shuffle(individual)
        energy, sat, vans = evaluate_solution(individual)
        population.append({
            "route": individual,
            "energy": energy,
            "satisfaction": sat,
            "vans": vans
        })

    # Save initial random solution to compare improvements later
    initial_sample = population[0]

    # Step 2: Evolution Loop over Generations
    for _ in range(generations):
        offspring = []

        # Generate children using selection, crossover, and mutation
        for _ in range(pop_size):
            # Tournament selection between two random parents
            p1, p2 = random.sample(population, 2)
            parent_a = p1 if dominates(p1, p2) else p2

            p3, p4 = random.sample(population, 2)
            parent_b = p3 if dominates(p3, p4) else p4

            # Crossover and Mutation
            child_route = order_crossover(parent_a["route"], parent_b["route"])
            child_route = swap_mutation(child_route, mutation_rate=0.25)

            c_energy, c_sat, c_vans = evaluate_solution(child_route)
            offspring.append({
                "route": child_route,
                "energy": c_energy,
                "satisfaction": c_sat,
                "vans": c_vans
            })

        # Combine parents and children (Elitism)
        combined = population + offspring

        # Count how many other individuals dominate each candidate (Pareto Rank)
        for ind in combined:
            ind["dom_count"] = sum(1 for other in combined if dominates(other, ind))

        # Sort by dominance count (0 = Pareto optimal) and keep best `pop_size`
        combined.sort(key=lambda x: x["dom_count"])
        population = combined[:pop_size]

    # Step 3: Extract the Pareto Front (Non-Dominated solutions where dom_count == 0)
    pareto_front = [ind for ind in population if ind["dom_count"] == 0]

    # Remove duplicates from Pareto front
    unique_pareto = []
    seen = set()
    for sol in pareto_front:
        key = (sol["energy"], sol["satisfaction"])
        if key not in seen:
            seen.add(key)
            unique_pareto.append(sol)

    # Step 4: Pick the Top 3 Representative Trade-off Solutions
    # 1. Best Fuel / Energy Saver (Minimum Energy Cost)
    best_energy_sol = min(unique_pareto, key=lambda x: x["energy"])

    # 2. Best Customer Happiness (Maximum Satisfaction)
    best_sat_sol = max(unique_pareto, key=lambda x: x["satisfaction"])

    # 3. Best Balanced Route (Compromise programming: highest balance score)
    min_e = min(s["energy"] for s in unique_pareto)
    max_e = max(s["energy"] for s in unique_pareto)
    min_s = min(s["satisfaction"] for s in unique_pareto)
    max_s = max(s["satisfaction"] for s in unique_pareto)

    def balance_score(sol):
        # Normalize energy (0 = best) and satisfaction (1 = best)
        norm_e = (sol["energy"] - min_e) / (max_e - min_e + 1e-6)
        norm_s = (sol["satisfaction"] - min_s) / (max_s - min_s + 1e-6)
        return norm_s - norm_e

    best_balanced_sol = max(unique_pareto, key=balance_score)

    return initial_sample, best_energy_sol, best_sat_sol, best_balanced_sol, len(unique_pareto)


# ------------------------------------------------------------------------------
# 4. Terminal Output / Viva Demonstration
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Seed for consistent reproducible viva demonstration
    random.seed(42)

    print("=" * 65)
    print(" SOFT COMPUTING PROJECT: STEP 2 - GENETIC OPTIMIZER ")
    print("=" * 65)

    initial, fuel_saver, happy_cust, balanced, pareto_count = run_optimizer(pop_size=40, generations=50)

    print("\n--- 1. BEFORE OPTIMIZATION (Random Initial Route) ---")
    print(f"Stop Order             : {initial['route']}")
    print(f"Energy Cost            : {initial['energy']} units")
    print(f"Fuzzy Satisfaction     : {initial['satisfaction'] * 100:.1f}% Happy")
    print(f"Vans Used              : {len(initial['vans'])} Vans")

    print("\n--- 2. PARETO OPTIMIZATION SUMMARY ---")
    print(f"Total Non-Dominated (Pareto Optimal) Solutions Found: {pareto_count}")
    print(f"Top 1 (Best Fuel Saver)        : Energy = {fuel_saver['energy']} | Satisfaction = {fuel_saver['satisfaction'] * 100:.1f}%")
    print(f"Top 2 (Best Customer Happiness): Energy = {happy_cust['energy']} | Satisfaction = {happy_cust['satisfaction'] * 100:.1f}%")

    print("\n--- 3. TOP TRADE-OFF: BEST BALANCED ROUTE (OPTIMIZED) ---")
    print(f"Stop Order             : {balanced['route']}")
    print(f"Energy Cost            : {balanced['energy']} units")
    print(f"Fuzzy Satisfaction     : {balanced['satisfaction'] * 100:.1f}% Happy")
    print(f"Vans Used              : {len(balanced['vans'])} Vans")

    print("\nVan Route Breakdown:")
    for v_idx, van_stops in enumerate(balanced["vans"], start=1):
        stop_names = [STOP_MAP[sid]["name"].split(" - ")[1] for sid in van_stops]
        load = sum(STOP_MAP[sid]["weight"] for sid in van_stops)
        print(f"  * Van {v_idx} (Load: {load}kg / 100kg): Depot -> {' -> '.join(stop_names)} -> Depot")

    # Improvements comparison
    energy_saved = ((initial["energy"] - balanced["energy"]) / initial["energy"]) * 100
    satisfaction_gain = ((balanced["satisfaction"] - initial["satisfaction"]) / initial["satisfaction"]) * 100

    print("\n--- 4. PERFORMANCE IMPROVEMENT ---")
    print(f"Energy Cost Reduction  : {energy_saved:+.2f}%")
    print(f"Satisfaction Increase  : {satisfaction_gain:+.2f}%")
    print("=" * 65)
