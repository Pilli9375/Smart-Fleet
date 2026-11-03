# ==============================================================================
# Step 1: Delivery Stops Data & Fuzzy Satisfaction Function
# Subject: Soft Computing Project (College Level)
# ==============================================================================

# Central Depot: Starting and returning location for the delivery van
depot = {
    "id": 0,
    "name": "Central Depot",
    "x": 0,
    "y": 0
}

# List of 10 Delivery Stops around the depot
# Each stop contains:
# - id: Unique stop number
# - name: Customer or location name
# - x, y: Coordinates on the map (in kilometers)
# - weight: Package weight to deliver (in kg)
# - best_start, best_end: Preferred time window (in minutes)
# - max_late: The latest time customer will accept delivery (in minutes)
stops = [
    {"id": 1,  "name": "Stop 1 - City Mall",       "x": 2,  "y": 3,  "weight": 15, "best_start": 20,  "best_end": 40,  "max_late": 60},
    {"id": 2,  "name": "Stop 2 - Green Park",      "x": -3, "y": 4,  "weight": 25, "best_start": 30,  "best_end": 50,  "max_late": 75},
    {"id": 3,  "name": "Stop 3 - Tech Park",       "x": 5,  "y": -2, "weight": 10, "best_start": 40,  "best_end": 60,  "max_late": 90},
    {"id": 4,  "name": "Stop 4 - University Hub",  "x": -4, "y": -3, "weight": 30, "best_start": 50,  "best_end": 70,  "max_late": 100},
    {"id": 5,  "name": "Stop 5 - Metro Station",   "x": 1,  "y": 6,  "weight": 20, "best_start": 60,  "best_end": 80,  "max_late": 110},
    {"id": 6,  "name": "Stop 6 - Sunrise Hospital","x": -2, "y": 7,  "weight": 12, "best_start": 70,  "best_end": 90,  "max_late": 120},
    {"id": 7,  "name": "Stop 7 - Harbor Market",    "x": 6,  "y": 1,  "weight": 18, "best_start": 80,  "best_end": 100, "max_late": 135},
    {"id": 8,  "name": "Stop 8 - Silver Residency", "x": 3,  "y": -5, "weight": 22, "best_start": 90,  "best_end": 110, "max_late": 140},
    {"id": 9,  "name": "Stop 9 - Airport Cargo",    "x": -6, "y": -1, "weight": 35, "best_start": 100, "best_end": 120, "max_late": 150},
    {"id": 10, "name": "Stop 10 - Grand Plaza",     "x": 0,  "y": -6, "weight": 15, "best_start": 110, "best_end": 130, "max_late": 160}
]


# ------------------------------------------------------------------------------
# Fuzzy Satisfaction Function
# ------------------------------------------------------------------------------
# Why Fuzzy Logic?
# In classical logic, delivery is either strictly ON TIME (1) or LATE (0).
# Fuzzy logic allows partial satisfaction (e.g., 0.75 happy) if the van is slightly late.
def get_fuzzy_satisfaction(arrival_time, best_start, best_end, max_late):
    """
    Calculates customer satisfaction score between 0.0 and 1.0.
    1. Between best_start and best_end: 1.0 (100% happy)
    2. Between best_end and max_late: gradually drops from 1.0 to 0.0
    3. After max_late: 0.0 (0% happy)
    """
    # 1. Arrived within or earlier than the best delivery window
    if arrival_time <= best_end:
        return 1.0
    
    # 2. Arrived slightly late (Fuzzy membership ramp-down)
    elif arrival_time <= max_late:
        # Linear fuzzy score formula: (max_late - arrival) / (max_late - best_end)
        score = (max_late - arrival_time) / (max_late - best_end)
        return round(score, 2)
    
    # 3. Arrived past the maximum acceptable late time
    else:
        return 0.0


# ------------------------------------------------------------------------------
# Quick Test / Viva Demonstration
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 65)
    print(" SOFT COMPUTING PROJECT: STEP 1 - FUZZY SATISFACTION TEST")
    print("=" * 65)

    # Let's test using Stop 1
    sample_stop = stops[0]
    start = sample_stop["best_start"]
    end = sample_stop["best_end"]
    late_limit = sample_stop["max_late"]

    print(f"Stop Name                   : {sample_stop['name']}")
    print(f"Preferred Window [Start-End]: {start} to {end} mins")
    print(f"Max Acceptable Late Time    : {late_limit} mins")
    print("-" * 65)

    # 3 Example Arrival Times: On-Time, Slightly Late, Very Late
    test_cases = [
        ("On-Time Arrival",       30),  # Inside [20, 40]
        ("Slightly Late Arrival", 50),  # Between 40 and 60
        ("Very Late Arrival",     75)   # Greater than 60
    ]

    print(f"{'Scenario':<24} | {'Arrival':<10} | {'Fuzzy Score':<12} | {'Meaning'}")
    print("-" * 65)

    for label, arrival in test_cases:
        satisfaction = get_fuzzy_satisfaction(arrival, start, end, late_limit)
        percentage = int(satisfaction * 100)
        print(f"{label:<24} | {arrival} mins   | {satisfaction:<12} | {percentage}% Satisfied")

    print("-" * 65)
    print(f"Successfully loaded {len(stops)} stops and depot.")
