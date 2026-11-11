"""
generate_figures.py
Generates 6 publication-quality academic figures for the FleetPulse AI Project Report.
Replaces all raw Mermaid syntax with professional, high-resolution vector/raster diagrams.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Ensure figures directory exists
FIGURES_DIR = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8


# =====================================================================
# FIGURE 1: Soft Computing Paradigm & Motivation
# =====================================================================
def create_fig1():
    fig, ax = plt.subplots(figsize=(8.5, 4.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    # Background card
    rect_bg = patches.FancyBboxPatch((0.1, 0.1), 9.8, 4.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                    facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.0)
    ax.add_patch(rect_bg)

    # Title
    ax.text(5.0, 4.55, "Urban Freight Routing: Transition to Soft Computing Paradigm",
            ha="center", va="center", fontsize=11, fontweight="bold", color="#0f172a")

    # Left: Challenges
    challenges = [
        "Combinatorial Explosion:\n25! ≈ 1.55 × 10^25 routes",
        "Axle Payload Limit:\n≤ 100 kg / van",
        "Stochastic Dynamics:\nWeather & Traffic Spikes",
        "Crisp SLA Failure:\n1-min late = 0% utility"
    ]
    for idx, ch in enumerate(challenges):
        y_pos = 3.6 - idx * 0.9
        box = patches.FancyBboxPatch((0.4, y_pos - 0.35), 3.0, 0.7, boxstyle="round,pad=0.08,rounding_size=0.08",
                                     facecolor="#fee2e2", edgecolor="#f87171", linewidth=0.8)
        ax.add_patch(box)
        ax.text(1.9, y_pos, ch, ha="center", va="center", fontsize=7.5, color="#991b1b", fontweight="medium")

    # Center: Soft Computing Core
    center_box = patches.FancyBboxPatch((3.8, 1.2), 2.4, 2.2, boxstyle="round,pad=0.1,rounding_size=0.1",
                                        facecolor="#0284c7", edgecolor="#0369a1", linewidth=1.2)
    ax.add_patch(center_box)
    ax.text(5.0, 2.7, "SOFT COMPUTING\nPARADIGM", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#ffffff")
    ax.text(5.0, 1.8, "Synergistic Integration of\nFuzzy Logic Modeling\n+\nEvolutionary Search",
            ha="center", va="center", fontsize=7.5, color="#e0f2fe")

    # Right: Solutions
    solutions = [
        ("Continuous Fuzzy SLA Windows", "Trapezoidal, Gaussian, Sigmoidal\nμ(t) ∈ [0.0, 1.0] realistic satisfaction"),
        ("9-Rule Mamdani Traffic FIS", "Dynamic congestion drag multiplier\nτ ∈ [1.00×, 1.85×] speed scaling"),
        ("Memetic Hybrid NSGA-II", "OX1 Crossover + 2-Opt Local Refinement\nPareto-optimal bi-objective frontier")
    ]
    for idx, (sol_title, sol_desc) in enumerate(solutions):
        y_pos = 3.4 - idx * 1.15
        box = patches.FancyBboxPatch((6.6, y_pos - 0.42), 3.0, 0.85, boxstyle="round,pad=0.08,rounding_size=0.08",
                                     facecolor="#ecfdf5", edgecolor="#34d399", linewidth=0.8)
        ax.add_patch(box)
        ax.text(8.1, y_pos + 0.15, sol_title, ha="center", va="center", fontsize=7.5, fontweight="bold", color="#065f46")
        ax.text(8.1, y_pos - 0.15, sol_desc, ha="center", va="center", fontsize=6.8, color="#047857")

    # Arrows
    for idx in range(4):
        y_pos = 3.6 - idx * 0.9
        ax.annotate("", xy=(3.75, 2.4 + (idx - 1.5) * 0.4), xytext=(3.45, y_pos),
                    arrowprops=dict(arrowstyle="->", color="#64748b", lw=1.0))
    for idx in range(3):
        y_pos = 3.4 - idx * 1.15
        ax.annotate("", xy=(6.55, y_pos), xytext=(6.25, 2.4 + (idx - 1) * 0.5),
                    arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.2))

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig1_soft_computing_paradigm.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated Figure 1: {path}")


# =====================================================================
# FIGURE 2: End-to-End System Architecture Pipeline
# =====================================================================
def create_fig2():
    fig, ax = plt.subplots(figsize=(9.2, 3.2), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.2)
    ax.axis('off')

    stages = [
        ("Stage 1: Input Layer", "#f1f5f9", "#475569", [
            "GIS GPS Coordinates (25 nodes)",
            "Parcel Weights (10–45 kg)",
            "Priority Weights (Critical..Normal)",
            "SLA Intervals [e_i, l_i], Cutoffs u_i",
            "Weather & Traffic Sensor Feeds"
        ]),
        ("Stage 2: Soft Perception", "#e0f2fe", "#0284c7", [
            "Multi-Kernel Satisfaction μ(t)",
            "Trapezoidal / Gaussian / Sigmoidal",
            "Mamdani Rule Base (9 Rules)",
            "Traffic & Weather Fuzzification",
            "Centroid Defuzzification (τ)"
        ]),
        ("Stage 3: Metaheuristic Engine", "#fef3c7", "#d97706", [
            "Proposed: Hybrid Fuzzy-NSGA-II",
            "Benchmark: MO-ACO (Ant Colony)",
            "Benchmark: MOPSO (Particle Swarm)",
            "Benchmark: Standard GA (Single-Obj)",
            "Benchmark: Greedy Nearest-Neighbor"
        ]),
        ("Stage 4: Telematics & Output", "#dcfce7", "#16a34a", [
            "Non-Dominated Pareto Frontier",
            "Normalized Utopia Knee Selection",
            "Sub-Tour Vehicle Partitions",
            "HTML5 Vector Radar Canvas HUD",
            "Monte Carlo Statistical Validator"
        ])
    ]

    for idx, (title, bg_col, border_col, items) in enumerate(stages):
        x_pos = 0.3 + idx * 2.4
        box = patches.FancyBboxPatch((x_pos, 0.2), 2.15, 2.7, boxstyle="round,pad=0.08,rounding_size=0.1",
                                     facecolor=bg_col, edgecolor=border_col, linewidth=1.2)
        ax.add_patch(box)
        ax.text(x_pos + 1.075, 2.65, title, ha="center", va="center", fontsize=7.8, fontweight="bold", color="#0f172a")

        line = patches.ConnectionPatch(xyA=(x_pos + 0.1, 2.45), xyB=(x_pos + 2.05, 2.45),
                                       coordsA="data", coordsB="data", color=border_col, linewidth=0.8)
        ax.add_artist(line)

        for i_idx, item in enumerate(items):
            ax.text(x_pos + 0.1, 2.2 - i_idx * 0.42, f"• {item}", ha="left", va="center", fontsize=6.5, color="#1e293b")

        if idx < 3:
            ax.annotate("", xy=(x_pos + 2.42, 1.55), xytext=(x_pos + 2.18, 1.55),
                        arrowprops=dict(arrowstyle="->", color="#0f172a", lw=1.5))

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig2_system_pipeline.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated Figure 2: {path}")


# =====================================================================
# FIGURE 3: Hybrid NSGA-II Algorithmic Flowchart
# =====================================================================
def create_fig3():
    fig, ax = plt.subplots(figsize=(8.8, 4.4), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    rect_bg = patches.FancyBboxPatch((0.1, 0.1), 9.8, 4.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                    facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.0)
    ax.add_patch(rect_bg)
    ax.text(5.0, 4.65, "Memetic Hybrid Fuzzy-NSGA-II Algorithmic Search Architecture",
            ha="center", va="center", fontsize=11, fontweight="bold", color="#0f172a")

    steps = [
        (0.6, 2.4, 1.8, 1.6, "1. Heuristic Seeding", "#e0f2fe", "#0284c7",
         "• Seed 1: Earliest Deadline\n• Seed 2: Spatial Urgency\n• Seed 3: Greedy Baseline\n• Seed 4..P: Stochastic"),
        (2.9, 2.4, 1.8, 1.6, "2. Route Partitioning", "#fef3c7", "#d97706",
         "• Capacity Split: ≤100 kg\n• Instantaneous Load Physics\n• Congestion Drag Factor (τ)\n• Energy f1 + Satisfaction f2"),
        (5.2, 2.4, 1.8, 1.6, "3. Fast Non-Dom Sorting", "#f3e8ff", "#9333ea",
         "• Pareto Ranking (F1, F2...)\n• Crowding Distance metric\n• Binary Tournament Select\n• Elitist (P + P) Retention"),
        (7.5, 2.4, 1.8, 1.6, "4. Memetic Recombination", "#ecfdf5", "#059669",
         "• Order Crossover (OX1)\n• Tour validity guaranteed\n• Inversion Mutation (Pm=0.25)\n• 2-Opt Local Uncrossing")
    ]

    for (x, y, w, h, title, bg, border, content) in steps:
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.1",
                                     facecolor=bg, edgecolor=border, linewidth=1.1)
        ax.add_patch(box)
        ax.text(x + w/2, y + h - 0.22, title, ha="center", va="center", fontsize=7.8, fontweight="bold", color="#0f172a")
        ax.text(x + 0.1, y + h/2 - 0.1, content, ha="left", va="center", fontsize=6.6, color="#1e293b")

    # Connect top row
    ax.annotate("", xy=(2.85, 3.2), xytext=(2.45, 3.2), arrowprops=dict(arrowstyle="->", color="#0f172a", lw=1.2))
    ax.annotate("", xy=(5.15, 3.2), xytext=(4.75, 3.2), arrowprops=dict(arrowstyle="->", color="#0f172a", lw=1.2))
    ax.annotate("", xy=(7.45, 3.2), xytext=(7.05, 3.2), arrowprops=dict(arrowstyle="->", color="#0f172a", lw=1.2))

    # Loop back arrow from Step 4 to Step 2
    ax.annotate("Next Generation\n(Size 2P -> P)", xy=(3.8, 2.35), xytext=(8.4, 1.8),
                arrowprops=dict(arrowstyle="->", color="#9333ea", lw=1.2, connectionstyle="arc3,rad=0.2"),
                fontsize=7.0, color="#7e22ce", ha="center", fontweight="bold")

    # Bottom Decision / Utopia Box
    box_utopia = patches.FancyBboxPatch((3.0, 0.4), 4.0, 1.0, boxstyle="round,pad=0.08,rounding_size=0.1",
                                        facecolor="#0f172a", edgecolor="#0284c7", linewidth=1.2)
    ax.add_patch(box_utopia)
    ax.text(5.0, 1.05, "Step 5: Multi-Criteria Utopia Knee-Point Selector", ha="center", va="center", fontsize=8.2, fontweight="bold", color="#38bdf8")
    ax.text(5.0, 0.65, "d_utopia = √[ 0.45·((f1 - f1_min)/(f1_max - f1_min))^2 + 0.55·((f2_max - f2)/(f2_max - f2_min))^2 ]\nSelects single balanced commercial dispatch schedule from Pareto front",
            ha="center", va="center", fontsize=6.4, color="#e2e8f0")

    ax.annotate("", xy=(5.0, 1.45), xytext=(7.5, 2.35),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.3, connectionstyle="arc3,rad=-0.15"))

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig3_nsga2_workflow.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated Figure 3: {path}")


# =====================================================================
# FIGURE 4: Multi-Kernel Fuzzy Satisfaction Decay Curves
# =====================================================================
def create_fig4():
    fig, ax = plt.subplots(figsize=(7.5, 3.8), dpi=300)

    # Time window parameters
    e_i = 10.0   # Preferred window start
    l_i = 30.0   # Preferred window end (100% satisfaction up to this point)
    u_i = 60.0   # Maximum late cutoff (0% satisfaction beyond this)

    t = np.linspace(10, 70, 400)

    # 1. Trapezoidal
    mu_trap = np.piecewise(t, [t <= l_i, (t > l_i) & (t <= u_i), t > u_i],
                           [1.0, lambda x: (u_i - x) / (u_i - l_i), 0.0])

    # 2. Gaussian
    sigma_i = (u_i - l_i) / 2.2
    mu_gauss = np.piecewise(t, [t <= l_i, t > l_i],
                            [1.0, lambda x: np.exp(-0.5 * ((x - l_i) / sigma_i) ** 2)])

    # 3. Sigmoidal
    gamma_i = 6.0 / (u_i - l_i)
    mid_i = (l_i + u_i) / 2.0
    mu_sigm = np.piecewise(t, [t <= l_i, t > l_i],
                           [1.0, lambda x: 1.0 / (1.0 + np.exp(gamma_i * (x - mid_i)))])

    # Plot curves
    ax.plot(t, mu_trap, label="Trapezoidal (Piecewise Linear SLA)", color="#0284c7", lw=2.2)
    ax.plot(t, mu_gauss, label="Gaussian (Exponential Bell Curve)", color="#10b981", lw=2.2, linestyle="--")
    ax.plot(t, mu_sigm, label="Sigmoidal (Logistic Midpoint Drop)", color="#f59e0b", lw=2.2, linestyle="-.")

    # Highlight preferred window
    ax.axvspan(e_i, l_i, color="#dbeafe", alpha=0.5, label="Preferred Window [10, 30 min] (μ = 1.0)")
    ax.axvline(l_i, color="#64748b", linestyle=":", lw=1.0)
    ax.axvline(u_i, color="#ef4444", linestyle=":", lw=1.0)

    ax.text(20, 0.5, "100% SLA\nGrace Period", ha="center", va="center", fontsize=8, fontweight="bold", color="#1e40af")
    ax.text(l_i + 1, 0.08, "l_i (30 min)", fontsize=7.5, color="#475569")
    ax.text(u_i + 1, 0.08, "u_i (60 min)", fontsize=7.5, color="#dc2626")

    ax.set_title("Multi-Kernel Fuzzy Customer Satisfaction Decay: μ(t) vs Arrival Time", fontsize=10, fontweight="bold", pad=10)
    ax.set_xlabel("Vehicle Arrival Time t_i (minutes)", fontsize=8.5)
    ax.set_ylabel("Fuzzy Satisfaction Degree μ(t_i)", fontsize=8.5)
    ax.set_xlim(10, 70)
    ax.set_ylim(-0.05, 1.08)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper right", fontsize=7.2, framealpha=0.95)

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig4_fuzzy_decay.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated Figure 4: {path}")


# =====================================================================
# FIGURE 5: Decoupled 3-Tier Layered Software Architecture
# =====================================================================
def create_fig5():
    fig, ax = plt.subplots(figsize=(8.6, 3.6), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')

    rect_bg = patches.FancyBboxPatch((0.1, 0.1), 9.8, 3.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                    facecolor="#f8fafc", edgecolor="#cbd5e1", linewidth=1.0)
    ax.add_patch(rect_bg)
    ax.text(5.0, 3.65, "FleetPulse AI Decoupled 3-Tier Layered Software Architecture",
            ha="center", va="center", fontsize=10.5, fontweight="bold", color="#0f172a")

    tiers = [
        (0.4, 0.4, 2.8, 2.9, "Tier 1: Telemetry HUD", "app.py (Streamlit Frontend)", "#0f172a", "#38bdf8", [
            "HTML5 Vector Radar Canvas HUD",
            "Multi-Algorithm Benchmark Arena",
            "Pareto Frontier Studio (Plotly)",
            "3D Rotatable Fuzzy Surface",
            "5-Seed Monte Carlo Validator",
            "Industrial Zinc Dark Theme"
        ]),
        (3.6, 0.4, 2.8, 2.9, "Tier 2: Metaheuristic Core", "core_optimizers.py (Solvers)", "#1e293b", "#34d399", [
            "Hybrid Fuzzy-NSGA-II Engine",
            "Multi-Objective ACO (MO-ACO)",
            "Multi-Objective PSO (MOPSO)",
            "Standard Genetic Algorithm (SGA)",
            "Greedy Nearest-Neighbor Dispatcher",
            "Utopia Knee-Point Selection"
        ]),
        (6.8, 0.4, 2.8, 2.9, "Tier 3: Physics & Fuzzy Core", "core_data_and_fuzzy.py (Engine)", "#0f172a", "#fbbf24", [
            "GIS Amaravati Node Coordinates",
            "Load Friction Physics (0.006/kg)",
            "Multi-Kernel SLA Functions",
            "9-Rule Mamdani Inference Matrix",
            "Centroid Defuzzification (τ)",
            "Solomon C101 & R101 Benchmarks"
        ])
    ]

    for (x, y, w, h, tier_label, sub_label, bg, accent, items) in tiers:
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08,rounding_size=0.1",
                                     facecolor=bg, edgecolor=accent, linewidth=1.3)
        ax.add_patch(box)
        ax.text(x + w/2, y + h - 0.25, tier_label, ha="center", va="center", fontsize=8.2, fontweight="bold", color=accent)
        ax.text(x + w/2, y + h - 0.55, sub_label, ha="center", va="center", fontsize=6.8, color="#94a3b8")

        for i_idx, item in enumerate(items):
            ax.text(x + 0.18, y + h - 0.95 - i_idx * 0.32, f"• {item}", ha="left", va="center", fontsize=6.6, color="#e2e8f0")

    # Arrows between tiers
    ax.annotate("Dispatches Orders\n& Parameters", xy=(3.55, 2.1), xytext=(3.25, 2.1),
                arrowprops=dict(arrowstyle="->", color="#0284c7", lw=1.2), fontsize=6.0, color="#0284c7", ha="center")
    ax.annotate("Evaluates Routes\n& Physics", xy=(6.75, 2.1), xytext=(6.45, 2.1),
                arrowprops=dict(arrowstyle="->", color="#10b981", lw=1.2), fontsize=6.0, color="#10b981", ha="center")

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig5_software_architecture.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated Figure 5: {path}")


# =====================================================================
# FIGURE 6: 5-Algorithm Head-to-Head Benchmarking Bar Chart
# =====================================================================
def create_fig6():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.6, 3.8), dpi=300)

    algorithms = ["Hybrid NSGA-II\n(Proposed)", "MO-ACO\n(Colony)", "Greedy\nBaseline", "MOPSO\n(Swarm)", "Standard GA\n(Single-Obj)"]
    satisfaction = [73.50, 71.35, 63.06, 61.36, 54.19]
    hypervolume = [21.96, 21.23, 0.0, 14.81, 11.75]  # Greedy is single-point (HV=0)

    colors_sat = ["#0284c7", "#10b981", "#64748b", "#f59e0b", "#f43f5e"]
    colors_hv = ["#0284c7", "#10b981", "#cbd5e1", "#f59e0b", "#f43f5e"]

    # Bar chart 1: Customer Satisfaction
    bars1 = ax1.bar(algorithms, satisfaction, color=colors_sat, width=0.55, edgecolor="#0f172a", linewidth=0.8)
    ax1.set_title("Fuzzy Customer Satisfaction (%)", fontsize=9.5, fontweight="bold", pad=8)
    ax1.set_ylabel("Satisfaction Degree (%)", fontsize=8.0)
    ax1.set_ylim(0, 85)
    ax1.tick_params(axis='x', labelsize=6.8)
    ax1.tick_params(axis='y', labelsize=7.5)
    ax1.grid(axis='y', linestyle=":", alpha=0.6)

    for bar, val in zip(bars1, satisfaction):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.2, f"{val:.1f}%",
                 ha="center", va="bottom", fontsize=7.2, fontweight="bold", color="#0f172a")

    # Star on rank 1
    ax1.text(0, 73.50 + 5.5, "★ RANK #1", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#0284c7")

    # Bar chart 2: Hypervolume
    bars2 = ax2.bar(algorithms, hypervolume, color=colors_hv, width=0.55, edgecolor="#0f172a", linewidth=0.8)
    ax2.set_title("Pareto Hypervolume (HV Indicator)", fontsize=9.5, fontweight="bold", pad=8)
    ax2.set_ylabel("Hypervolume (Higher = Superior)", fontsize=8.0)
    ax2.set_ylim(0, 26)
    ax2.tick_params(axis='x', labelsize=6.8)
    ax2.tick_params(axis='y', labelsize=7.5)
    ax2.grid(axis='y', linestyle=":", alpha=0.6)

    for idx, (bar, val) in enumerate(zip(bars2, hypervolume)):
        txt = f"{val:.2f}" if val > 0 else "N/A"
        ax2.text(bar.get_x() + bar.get_width() / 2, max(0.5, bar.get_height()) + 0.5, txt,
                 ha="center", va="bottom", fontsize=7.2, fontweight="bold", color="#0f172a")

    ax2.text(0, 21.96 + 1.8, "★ CHAMPION", ha="center", va="center", fontsize=7.0, fontweight="bold", color="#0284c7")

    plt.tight_layout()
    path = os.path.join(FIGURES_DIR, "fig6_benchmark_comparison.png")
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Generated Figure 6: {path}")


def main():
    print("=" * 60)
    print(" GENERATING PUBLICATION-GRADE REPORT FIGURES")
    print("=" * 60)
    create_fig1()
    create_fig2()
    create_fig3()
    create_fig4()
    create_fig5()
    create_fig6()
    print("=" * 60)
    print(" ALL 6 FIGURES GENERATED SUCCESSFULLY IN figures/")
    print("=" * 60)


if __name__ == "__main__":
    main()
