# ==============================================================================
# Step 1: Delivery Stops Data & Fuzzy Satisfaction Function
# Subject: Soft Computing Project (College Level)
# ==============================================================================

# Central Depot: Starting and returning location for the delivery vans
depot = {
    "id": 0,
    "name": "Central Depot",
    "x": 0,
    "y": 0
}

# List of 10 Delivery Stops around the Central Depot.
# Stops 1, 4, 7, 8, and 9 have tighter delivery windows to create a genuine conflict
# between minimizing Energy/Fuel Cost and maximizing Customer Satisfaction.
stops = [
    {"id": 1,  "name": "Stop 1 - City Mall",        "x": 2,  "y": 3,  "weight": 15, "best_start": 3,  "best_end": 7,  "max_late": 14}, # tight
    {"id": 2,  "name": "Stop 2 - Green Park",       "x": -3, "y": 4,  "weight": 25, "best_start": 8,  "best_end": 18, "max_late": 28},
    {"id": 3,  "name": "Stop 3 - Tech Park",        "x": 5,  "y": -2, "weight": 10, "best_start": 8,  "best_end": 18, "max_late": 28},
    {"id": 4,  "name": "Stop 4 - University Hub",   "x": -4, "y": -3, "weight": 30, "best_start": 3,  "best_end": 7,  "max_late": 14}, # tight
    {"id": 5,  "name": "Stop 5 - Metro Station",    "x": 1,  "y": 6,  "weight": 20, "best_start": 10, "best_end": 22, "max_late": 32},
    {"id": 6,  "name": "Stop 6 - Sunrise Hospital", "x": -2, "y": 7,  "weight": 12, "best_start": 12, "best_end": 24, "max_late": 35},
    {"id": 7,  "name": "Stop 7 - Harbor Market",     "x": 6,  "y": 1,  "weight": 18, "best_start": 3,  "best_end": 7,  "max_late": 14}, # tight
    {"id": 8,  "name": "Stop 8 - Silver Residency",  "x": 3,  "y": -5, "weight": 22, "best_start": 3,  "best_end": 7,  "max_late": 14}, # tight
    {"id": 9,  "name": "Stop 9 - Airport Cargo",     "x": -6, "y": -1, "weight": 35, "best_start": 3,  "best_end": 7,  "max_late": 14}, # tight
    {"id": 10, "name": "Stop 10 - Grand Plaza",      "x": 0,  "y": -6, "weight": 15, "best_start": 10, "best_end": 20, "max_late": 30}
]


# ------------------------------------------------------------------------------
# Fuzzy Satisfaction Function
# ------------------------------------------------------------------------------
# In Fuzzy Logic, instead of strict binary YES (1) or NO (0), human satisfaction
# is graded smoothly between 0.0 and 1.0.
def get_fuzzy_satisfaction(arrival_time, best_start, best_end, max_late):
    """
    Calculates customer satisfaction score between 0.0 and 1.0 based on arrival time:
    1. Arrived on-time or early (<= best_end): 1.0 (100% satisfied)
    2. Arrived slightly late (between best_end and max_late): linear decrease to 0.0
    3. Arrived past max_late (> max_late): 0.0 (0% satisfied)
    """
    # 1. On-time or early delivery
    if arrival_time <= best_end:
        return 1.0
    
    # 2. Tolerated delay (Fuzzy membership ramp-down)
    elif arrival_time <= max_late:
        score = (max_late - arrival_time) / (max_late - best_end)
        return round(score, 3)
    
    # 3. Completely late
    else:
        return 0.0


# ------------------------------------------------------------------------------
# Quick Test / Viva Demonstration
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 65)
    print(" SOFT COMPUTING PROJECT: STEP 1 - FUZZY SATISFACTION TEST")
    print("=" * 65)

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
        ("On-Time Arrival",       6),   # Inside [3, 7]
        ("Slightly Late Arrival", 10),  # Between 7 and 14
        ("Very Late Arrival",     18)   # Greater than 14
    ]

    print(f"{'Scenario':<24} | {'Arrival':<10} | {'Fuzzy Score':<12} | {'Meaning'}")
    print("-" * 65)

    for label, arrival in test_cases:
        satisfaction = get_fuzzy_satisfaction(arrival, start, end, late_limit)
        percentage = round(satisfaction * 100, 1)
        print(f"{label:<24} | {arrival} mins   | {satisfaction:<12} | {percentage}% Satisfied")

    print("-" * 65)
    print(f"Successfully loaded {len(stops)} stops and depot.")
