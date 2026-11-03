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
    """Calculates straight-line Euclidean distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def evaluate_solution(route_order, max_van_capacity=100):
    """
    Evaluates a given route order of stop IDs (e.g., [3, 1, 7, 2, ...]).
    
    1. Splits stops into separate vans whenever payload exceeds max_van_capacity.
    2. Calculates Total Energy Cost (heavier vans use more energy per km).
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

        # Initial load = sum of package weights this van is carrying
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

            # Package delivered: drop weight
            current_load -= stop["weight"]

            # Score 2: Fuzzy satisfaction for this stop
            sat = get_fuzzy_satisfaction(
                arrival_time=current_time,
                best_start=stop["best_start"],
                best_end=stop["best_end"],
                max_late=stop["max_late"]
            )
            all_satisfactions.append(sat)

            # Update van location
            current_x, current_y = stop["x"], stop["y"]

        # Return trip back to Central Depot (empty van, load = 0)
        return_dist = euclidean_distance(current_x, current_y, depot["x"], depot["y"])
        total_energy_cost += return_dist * (1 + 0.005 * 0)

    # Fleet-wide average fuzzy satisfaction (0.0 to 1.0)
    avg_satisfaction = sum(all_satisfactions) / len(all_satisfactions)

    return round(total_energy_cost, 2), round(avg_satisfaction, 3), vans


def get_detailed_schedule(vans):
    """
    Returns an itemized timeline for each stop across all vans.
    Used for clean tabular display and schedule inspection.
    """
    schedule = []
    for van_idx, van_stops in enumerate(vans, start=1):
        current_time = 0.0
        current_x = depot["x"]
        current_y = depot["y"]
        current_load = sum(STOP_MAP[sid]["weight"] for sid in van_stops)

        for sid in van_stops:
            stop = STOP_MAP[sid]
            dist = euclidean_distance(current_x, current_y, stop["x"], stop["y"])
            current_time += dist

            sat = get_fuzzy_satisfaction(
                arrival_time=current_time,
                best_start=stop["best_start"],
                best_end=stop["best_end"],
                max_late=stop["max_late"]
            )

            schedule.append({
                "Van": f"Van {van_idx}",
                "Stop ID": stop["id"],
                "Stop Name": stop["name"],
                "Load Before (kg)": current_load,
                "Package Weight (kg)": stop["weight"],
                "Arrival Time (min)": round(current_time, 2),
                "Best Window (min)": f"[{stop['best_start']}, {stop['best_end']}]",
                "Max Late (min)": stop["max_late"],
                "Fuzzy Satisfaction": f"{round(sat * 100, 1)}%"
            })

            current_load -= stop["weight"]
            current_x, current_y = stop["x"], stop["y"]

    return schedule


# ------------------------------------------------------------------------------
# 2. Genetic Operators (Crossover & Mutation)
# ------------------------------------------------------------------------------
def order_crossover(parent1, parent2):
    """
    Order Crossover (OX) for Permutations:
    Ensures every stop 1 to 10 appears exactly once without duplicates.
    """
    size = len(parent1)
    cut1, cut2 = sorted(random.sample(range(size), 2))

    child = [None] * size
    child[cut1:cut2 + 1] = parent1[cut1:cut2 + 1]

    p2_idx = 0
    for i in range(size):
        if child[i] is None:
            while parent2[p2_idx] in child:
                p2_idx += 1
            child[i] = parent2[p2_idx]

    return child


def swap_mutation(route, mutation_rate=0.2):
    """Randomly swaps two stops in the route with given mutation probability."""
    mutated = list(route)
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(mutated)), 2)
        mutated[i], mutated[j] = mutated[j], mutated[i]
    return mutated


# ------------------------------------------------------------------------------
# 3. Multi-Objective Pareto Dominance & Optimizer (NSGA-II Style)
# ------------------------------------------------------------------------------
def dominates(sol_a, sol_b):
    """
    Solution A dominates B if:
    1. A is at least as good in both objectives (Lower Energy, Higher Satisfaction).
    2. A is strictly better in at least one objective.
    """
    better_or_equal = (sol_a["energy"] <= sol_b["energy"]) and (sol_a["satisfaction"] >= sol_b["satisfaction"])
    strictly_better = (sol_a["energy"] < sol_b["energy"]) or (sol_a["satisfaction"] > sol_b["satisfaction"])
    return better_or_equal and strictly_better


def filter_pareto_front(solutions):
    """Filters a set of candidate solutions to keep only non-dominated solutions."""
    pareto = []
    for candidate in solutions:
        is_dominated = any(dominates(other, candidate) for other in solutions if other != candidate)
        if not is_dominated:
            # Prevent duplicate (energy, satisfaction) points in Pareto front
            if not any(candidate["energy"] == p["energy"] and candidate["satisfaction"] == p["satisfaction"] for p in pareto):
                pareto.append(candidate)
    return sorted(pareto, key=lambda x: x["energy"])


def run_optimizer(pop_size=40, generations=50, max_van_capacity=100):
    """
    Multi-Objective Genetic Algorithm:
    Searches for optimal trade-offs between Energy Cost and Customer Satisfaction.
    Maintains a global Pareto Archive of all non-dominated solutions found.
    """
    all_stop_ids = [s["id"] for s in stops]
    all_explored = []

    # Step 1: Create initial random population
    population = []
    for _ in range(pop_size):
        individual = list(all_stop_ids)
        random.shuffle(individual)
        energy, sat, vans = evaluate_solution(individual, max_van_capacity)
        item = {
            "route": individual,
            "energy": energy,
            "satisfaction": sat,
            "vans": vans
        }
        population.append(item)
        all_explored.append(item)

    # Keep a reference to an initial random solution for Before vs. After comparison
    initial_sample = population[0]

    # Step 2: Evolution Loop over Generations
    for _ in range(generations):
        offspring = []

        for _ in range(pop_size):
            # Tournament selection between two random individuals
            p1, p2 = random.sample(population, 2)
            parent_a = p1 if dominates(p1, p2) else p2

            p3, p4 = random.sample(population, 2)
            parent_b = p3 if dominates(p3, p4) else p4

            # Crossover & Mutation
            child_route = order_crossover(parent_a["route"], parent_b["route"])
            child_route = swap_mutation(child_route, mutation_rate=0.25)

            c_energy, c_sat, c_vans = evaluate_solution(child_route, max_van_capacity)
            child_item = {
                "route": child_route,
                "energy": c_energy,
                "satisfaction": c_sat,
                "vans": c_vans
            }
            offspring.append(child_item)
            all_explored.append(child_item)

        # Combine parents and children (Elitism)
        combined = population + offspring

        # Count how many other individuals dominate each candidate (Pareto Rank)
        for ind in combined:
            ind["dom_count"] = sum(1 for other in combined if dominates(other, ind))

        # Sort by dominance count (0 = non-dominated) and retain top pop_size
        combined.sort(key=lambda x: x["dom_count"])
        population = combined[:pop_size]

    # Step 3: Compute the Global Pareto Front across all explored solutions
    pareto_front = filter_pareto_front(all_explored)

    # Step 4: Pick the Top 3 Representative Trade-offs
    # 1. Best Fuel / Energy Saver (Minimum Energy Cost)
    best_energy_sol = min(pareto_front, key=lambda x: x["energy"])

    # 2. Best Customer Happiness (Maximum Satisfaction)
    best_sat_sol = max(pareto_front, key=lambda x: x["satisfaction"])

    # 3. Best Balanced Route (Compromise programming: highest balance score)
    min_e = min(s["energy"] for s in pareto_front)
    max_e = max(s["energy"] for s in pareto_front)
    min_s = min(s["satisfaction"] for s in pareto_front)
    max_s = max(s["satisfaction"] for s in pareto_front)

    def balance_score(sol):
        # Normalize: lower energy is better (0=best), higher sat is better (1=best)
        norm_e = (sol["energy"] - min_e) / (max_e - min_e + 1e-6)
        norm_s = (sol["satisfaction"] - min_s) / (max_s - min_s + 1e-6)
        return norm_s - norm_e

    best_balanced_sol = max(pareto_front, key=balance_score)

    return initial_sample, best_energy_sol, best_sat_sol, best_balanced_sol, pareto_front


# ------------------------------------------------------------------------------
# 4. Terminal Output / Viva Demonstration
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Reproducible seed for demonstration
    random.seed(42)

    print("=" * 68)
    print(" SOFT COMPUTING PROJECT: STEP 2 - GENETIC OPTIMIZER ")
    print("=" * 68)

    initial, fuel_saver, happy_cust, balanced, pareto_front = run_optimizer(
        pop_size=50, generations=60, max_van_capacity=100
    )

    print("\n--- 1. BEFORE OPTIMIZATION (Random Route) ---")
    print(f"Stop Order             : {initial['route']}")
    print(f"Energy Cost            : {initial['energy']} units")
    print(f"Fuzzy Satisfaction     : {initial['satisfaction'] * 100:.1f}% Happy")
    print(f"Vans Used              : {len(initial['vans'])} Vans")

    print(f"\n--- 2. PARETO OPTIMAL TRADE-OFFS ({len(pareto_front)} Solutions Found) ---")
    for idx, sol in enumerate(pareto_front, start=1):
        print(f"  Option {idx}: Energy = {sol['energy']:>6.2f} units | Satisfaction = {sol['satisfaction'] * 100:>5.1f}%")

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
    print("=" * 68)
