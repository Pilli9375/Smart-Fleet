# ==============================================================================
# Step 3: Streamlit Web Dashboard (app.py)
# Subject: Soft Computing Project (College Level Viva Demo)
# ==============================================================================

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Import our problem data and genetic optimizer from Steps 1 & 2
from step1_fuzzy_data import stops, depot, get_fuzzy_satisfaction
from step2_genetic_optimizer import (
    run_optimizer,
    get_detailed_schedule,
    STOP_MAP,
    evaluate_solution
)

# ------------------------------------------------------------------------------
# 1. Page Configuration
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Smart Fleet - Fuzzy NSGA-II Optimizer",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Smart Fleet: Vehicle Routing with Fuzzy Logic & NSGA-II")
st.markdown(
    "**A Soft Computing Project** combining **Fuzzy Logic Customer Satisfaction** "
    "with **Multi-Objective Genetic Algorithm (NSGA-II)** to optimize delivery routes."
)

# ------------------------------------------------------------------------------
# 2. Sidebar Controls
# ------------------------------------------------------------------------------
st.sidebar.header("⚙️ Optimization Parameters")

van_capacity = st.sidebar.slider(
    "Max Van Capacity (kg)",
    min_value=60,
    max_value=150,
    value=100,
    step=10,
    help="Maximum package weight a single van can carry."
)

pop_size = st.sidebar.slider(
    "Population Size (Chromosomes)",
    min_value=20,
    max_value=100,
    value=40,
    step=10,
    help="Number of candidate routes in each generation."
)

generations = st.sidebar.slider(
    "Number of Generations",
    min_value=10,
    max_value=100,
    value=50,
    step=10,
    help="How many evolutionary cycles the genetic algorithm runs."
)

run_button = st.sidebar.button("🚀 Run Hybrid Fuzzy-NSGA-II Optimizer", type="primary")

# Sidebar Viva Quick Notes
st.sidebar.markdown("---")
st.sidebar.subheader("🎓 Viva Quick Reference")
st.sidebar.info(
    "**Objectives:**\n"
    "1. 🔻 Minimize Total Energy Cost\n"
    "2. 🔺 Maximize Fuzzy Customer Satisfaction\n\n"
    "**Key Concepts:**\n"
    "- **Fuzzy Membership:** Partial satisfaction for acceptable delays.\n"
    "- **Order Crossover (OX):** Prevents duplicate customer visits.\n"
    "- **Pareto Dominance:** Trade-off between fuel & punctuality."
)

# ------------------------------------------------------------------------------
# 3. Optimization Execution & Session State Management
# ------------------------------------------------------------------------------
# Run on first load or when user clicks the button
if "optimizer_data" not in st.session_state or run_button:
    with st.spinner("Evolving delivery routes using Genetic Algorithm..."):
        initial, fuel_saver, happy_cust, balanced, pareto_front = run_optimizer(
            pop_size=pop_size,
            generations=generations,
            max_van_capacity=van_capacity
        )
        st.session_state["optimizer_data"] = {
            "initial": initial,
            "fuel_saver": fuel_saver,
            "happy_cust": happy_cust,
            "balanced": balanced,
            "pareto_front": pareto_front,
            "capacity": van_capacity
        }

data = st.session_state["optimizer_data"]
initial = data["initial"]
balanced = data["balanced"]
pareto_front = data["pareto_front"]

# ------------------------------------------------------------------------------
# 4. Top KPI Metrics Row
# ------------------------------------------------------------------------------
energy_saved_pct = ((initial["energy"] - balanced["energy"]) / initial["energy"]) * 100
sat_gain_pct = ((balanced["satisfaction"] - initial["satisfaction"]) / initial["satisfaction"]) * 100

m1, m2, m3, m4 = st.columns(4)
m1.metric(
    label="⚡ Optimized Energy Cost",
    value=f"{balanced['energy']:.2f} units",
    delta=f"{energy_saved_pct:.1f}% saved",
    delta_color="normal"
)
m2.metric(
    label="😊 Fuzzy Satisfaction",
    value=f"{balanced['satisfaction'] * 100:.1f}%",
    delta=f"{sat_gain_pct:+.1f}% gained",
    delta_color="normal"
)
m3.metric(
    label="🚐 Fleet Size Required",
    value=f"{len(balanced['vans'])} Vans",
    delta=f"Capacity: {data['capacity']} kg"
)
m4.metric(
    label="🎯 Pareto Solutions",
    value=f"{len(pareto_front)} Trade-offs",
    delta="Non-Dominated"
)

st.markdown("---")

# ------------------------------------------------------------------------------
# 5. Main Dashboard Tabs
# ------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🗺️ 2D Route Map & Van Schedule",
    "📈 Pareto Front & Comparison",
    "🧠 Fuzzy Logic Explainer (Viva)"
])


# ==============================================================================
# TAB 1: 2D Route Map & Van Schedule
# ==============================================================================
with tab1:
    st.subheader("Optimized Van Delivery Routes")
    
    van_colors = ["#1f77b4", "#2ca02c", "#d62728", "#9467bd", "#ff7f0e", "#17becf"]
    fig_map, ax = plt.subplots(figsize=(9, 6.5))

    # 1. Plot Central Depot
    ax.scatter(depot["x"], depot["y"], color="gold", s=350, marker="*", edgecolor="black", zorder=5, label="Central Depot")
    ax.annotate("Depot (0,0)", (depot["x"], depot["y"]), textcoords="offset points", xytext=(0, 10), ha="center", fontweight="bold", fontsize=10)

    # 2. Plot All 10 Delivery Stops
    for s in stops:
        ax.scatter(s["x"], s["y"], color="#ffffff", s=180, edgecolor="#333333", zorder=4)
        ax.annotate(
            f"S{s['id']}\n({s['weight']}kg)",
            (s["x"], s["y"]),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=8,
            fontweight="bold"
        )

    # 3. Plot Paths for Each Van
    for idx, van_stops in enumerate(balanced["vans"]):
        color = van_colors[idx % len(van_colors)]
        # Complete path: Depot -> Stop 1 -> ... -> Stop N -> Depot
        x_coords = [depot["x"]] + [STOP_MAP[sid]["x"] for sid in van_stops] + [depot["x"]]
        y_coords = [depot["y"]] + [STOP_MAP[sid]["y"] for sid in van_stops] + [depot["y"]]

        van_load = sum(STOP_MAP[sid]["weight"] for sid in van_stops)
        ax.plot(
            x_coords, y_coords,
            color=color,
            linewidth=2.2,
            linestyle="-",
            marker="o",
            markersize=6,
            label=f"Van {idx + 1} ({len(van_stops)} stops, {van_load}kg)"
        )

        # Draw directional arrows along the path
        for i in range(len(x_coords) - 1):
            mid_x = (x_coords[i] + x_coords[i + 1]) / 2
            mid_y = (y_coords[i] + y_coords[i + 1]) / 2
            dx = (x_coords[i + 1] - x_coords[i]) * 0.05
            dy = (y_coords[i + 1] - y_coords[i]) * 0.05
            ax.annotate("", xy=(mid_x + dx, mid_y + dy), xytext=(mid_x - dx, mid_y - dy),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.5))

    ax.set_title("Fleet Vehicle Routes Starting and Returning to Depot", fontsize=12, fontweight="bold", pad=12)
    ax.set_xlabel("X Coordinate (km)", fontsize=10)
    ax.set_ylabel("Y Coordinate (km)", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", framealpha=0.9)
    fig_map.tight_layout()

    st.pyplot(fig_map)

    # Detailed Schedule Table
    st.subheader("📋 Itemized Van Delivery Schedule")
    schedule_data = get_detailed_schedule(balanced["vans"])
    df_schedule = pd.DataFrame(schedule_data)
    st.dataframe(df_schedule, use_container_width=True)


# ==============================================================================
# TAB 2: Pareto Front & Before vs. After Comparison
# ==============================================================================
with tab2:
    st.subheader("Multi-Objective Optimization Results")
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 🎯 Pareto Optimal Trade-off Curve (NSGA-II)")
        fig_pareto, ax_p = plt.subplots(figsize=(6, 4.5))

        p_energies = [sol["energy"] for sol in pareto_front]
        p_sats = [sol["satisfaction"] * 100 for sol in pareto_front]

        # Draw Pareto trade-off line and scatter points
        ax_p.plot(p_energies, p_sats, color="#4a5568", linestyle="--", alpha=0.7, label="Pareto Front")
        ax_p.scatter(p_energies, p_sats, color="#3182ce", s=90, zorder=4, label="Non-Dominated Solutions")

        # Highlight Best Balanced Point
        ax_p.scatter(
            balanced["energy"],
            balanced["satisfaction"] * 100,
            color="#e53e3e",
            s=220,
            marker="*",
            edgecolor="black",
            zorder=5,
            label="Selected Balanced Route"
        )

        ax_p.set_xlabel("Energy Cost (Lower is Better 🔻)", fontsize=10)
        ax_p.set_ylabel("Customer Satisfaction % (Higher is Better 🔺)", fontsize=10)
        ax_p.set_title("Pareto Front: Fuel vs. Satisfaction Trade-off", fontsize=11, fontweight="bold")
        ax_p.grid(True, linestyle="--", alpha=0.5)
        ax_p.legend(fontsize=8, loc="lower right")
        fig_pareto.tight_layout()
        st.pyplot(fig_pareto)

        st.caption(
            "💡 **Viva Concept:** The Pareto Front represents all routes where you cannot reduce Energy Cost "
            "without reducing Customer Satisfaction."
        )

    with col_right:
        st.markdown("#### 📊 Before vs. After Optimization")
        fig_bar, (ax_b1, ax_b2) = plt.subplots(1, 2, figsize=(6, 4.5))

        # Comparison 1: Energy Cost
        bars1 = ax_b1.bar(
            ["Random", "Optimized"],
            [initial["energy"], balanced["energy"]],
            color=["#cbd5e0", "#38a169"],
            width=0.55
        )
        ax_b1.set_ylabel("Energy Cost (units)", fontsize=9)
        ax_b1.set_title("Energy Cost (Lower is Better)", fontsize=10, fontweight="bold")
        ax_b1.grid(axis="y", linestyle="--", alpha=0.5)
        for b in bars1:
            ax_b1.text(b.get_x() + b.get_width()/2, b.get_height() + 1.5, f"{b.get_height():.1f}", ha="center", fontsize=8, fontweight="bold")

        # Comparison 2: Fuzzy Satisfaction %
        bars2 = ax_b2.bar(
            ["Random", "Optimized"],
            [initial["satisfaction"] * 100, balanced["satisfaction"] * 100],
            color=["#cbd5e0", "#3182ce"],
            width=0.55
        )
        ax_b2.set_ylabel("Fuzzy Satisfaction (%)", fontsize=9)
        ax_b2.set_title("Satisfaction (Higher is Better)", fontsize=10, fontweight="bold")
        ax_b2.set_ylim(0, 110)
        ax_b2.grid(axis="y", linestyle="--", alpha=0.5)
        for b in bars2:
            ax_b2.text(b.get_x() + b.get_width()/2, b.get_height() + 1.5, f"{b.get_height():.1f}%", ha="center", fontsize=8, fontweight="bold")

        fig_bar.tight_layout()
        st.pyplot(fig_bar)

        st.caption(
            f"✅ **Improvement:** Fuel energy cost cut by **{energy_saved_pct:.1f}%**, "
            f"while Customer Satisfaction boosted by **{sat_gain_pct:+.1f}%**."
        )


# ==============================================================================
# TAB 3: Fuzzy Logic Explainer (For Faculty Viva)
# ==============================================================================
with tab3:
    st.subheader("Fuzzy Logic Membership Function (Human Satisfaction Model)")
    
    st.markdown(
        """
        In classical binary logic, a delivery arrival is strictly **On-Time (1)** or **Late (0)**. 
        In real-world logistics, customers have **tolerance**: arriving 2 minutes after the preferred window 
        still gives high satisfaction. We model this using a **Linear Ramp Fuzzy Membership Function**:
        """
    )

    # Plot Fuzzy Membership Function Curve
    fig_fuzz, ax_f = plt.subplots(figsize=(8, 3.5))

    # Example: Stop 1 window [best_start=3, best_end=7, max_late=14]
    b_start, b_end, m_late = 3, 7, 14
    times = np.linspace(0, 20, 300)
    scores = [get_fuzzy_satisfaction(t, b_start, b_end, m_late) for t in times]

    ax_f.plot(times, scores, color="#2b6cb0", linewidth=2.5, label=r"Fuzzy Satisfaction Degree $\mu(t)$")
    ax_f.axvspan(0, b_end, color="#c6f6d5", alpha=0.4, label="100% Satisfied Window")
    ax_f.axvspan(b_end, m_late, color="#feebc8", alpha=0.4, label="Tolerated Late Window (Fuzzy)")
    ax_f.axvspan(m_late, 20, color="#fed7d7", alpha=0.4, label="Unacceptable Delay (0%)")

    ax_f.axvline(b_end, color="darkgreen", linestyle=":", label=f"Best End ({b_end} min)")
    ax_f.axvline(m_late, color="darkred", linestyle=":", label=f"Max Late ({m_late} min)")

    ax_f.set_xlabel("Van Arrival Time (minutes)", fontsize=10)
    ax_f.set_ylabel(r"Fuzzy Satisfaction $\mu(t)$", fontsize=10)
    ax_f.set_title("Linear Decreasing Fuzzy Membership Function", fontsize=11, fontweight="bold")
    ax_f.set_ylim(-0.05, 1.1)
    ax_f.set_xlim(0, 20)
    ax_f.grid(True, linestyle="--", alpha=0.5)
    ax_f.legend(loc="upper right", fontsize=8)
    fig_fuzz.tight_layout()

    st.pyplot(fig_fuzz)

    st.markdown("#### 📋 All 10 Delivery Stops & Parameters")
    df_stops = pd.DataFrame(stops)
    df_stops = df_stops.rename(columns={
        "id": "Stop ID",
        "name": "Location Name",
        "x": "X (km)",
        "y": "Y (km)",
        "weight": "Package Weight (kg)",
        "best_start": "Window Start (min)",
        "best_end": "Window End (min)",
        "max_late": "Max Late Limit (min)"
    })
    st.dataframe(df_stops, use_container_width=True)
