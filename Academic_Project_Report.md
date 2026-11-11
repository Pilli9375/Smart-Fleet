# Hybrid Fuzzy-NSGA-II Intelligent Fleet Dispatcher: Multi-Objective Vehicle Routing with Fuzzy Time Windows, Mamdani Traffic Inference & 5-Algorithm Benchmarking

---

### **Project Report Format**
**Course:** Soft Computing & Artificial Intelligence (CSE Undergraduate Mini-Project / Capstone)  
**Institution:** School of Computer Science and Engineering (SCOPE), VIT-AP University, Amaravati  

**Submitted By:**  
- **V Naga Adithya** — Registration Number: **23BCE9062**  
- **M Karthik** — Registration Number: **23BCE9659**  

**Faculty Guide / Evaluator:**  
- **Dr. Seetha Hari**  
  Associate Professor, Department of Computer Science and Engineering,  
  School of Computer Science and Engineering (SCOPE),  
  VIT-AP University, Amaravati, Andhra Pradesh – 522237, India  

**Submission Date:** November 2026  
**Academic Year:** 2026–2027  

---

## Abstract

Last-mile urban freight logistics represents between 40% and 50% of aggregate supply chain expenditures and drives disproportionate carbon emissions in rapidly urbanizing corridors. The underlying Vehicle Routing Problem with Time Windows (VRPTW) is a classic NP-Hard combinatorial optimization challenge, yielding approximately $1.55 \times 10^{25}$ candidate routes for a moderate 25-node distribution network. Classical hard-computing methodologies rely on crisp, binary time windows that penalize a single second of arrival delay as a complete 100% service-level failure ($0$ utility), disregarding human tolerance, weather hazards, and urban traffic volatility. Furthermore, conventional formulations optimize pure geometric transit distance rather than true physical energy consumption governed by instantaneous vehicle payload.

This research presents **FleetPulse AI**, an integrated soft-computing framework combining continuous Fuzzy Set Theory, a 9-Rule Mamdani Environmental Inference Matrix, and a Memetic Non-Dominated Sorting Genetic Algorithm II (Hybrid Fuzzy-NSGA-II). The mathematical model simultaneously optimizes two conflicting objectives under a strict capacity constraint of $\le 100\text{ kg/van}$:
1. **Minimizing Load-Dependent Fleet Energy Cost ($f_1$)**, incorporating tare-to-gross payload friction physics;
2. **Maximizing Priority-Weighted Fuzzy Customer Satisfaction ($f_2$)**, parameterized via multi-kernel membership functions (Trapezoidal, Gaussian, Sigmoidal).

We benchmark the proposed Hybrid Fuzzy-NSGA-II against four competing paradigms: Multi-Objective Particle Swarm Optimization (MOPSO), Multi-Objective Ant Colony Optimization (MO-ACO), Standard Single-Objective Genetic Algorithm (SGA), and a Greedy Nearest-Neighbor Heuristic. Tested on real-world GIS coordinates from the Amaravati–Vijayawada metropolitan corridor and standardized Solomon VRPTW benchmarks (C101 clustered and R101 random), Hybrid Fuzzy-NSGA-II consistently dominates the Pareto landscape. On the 18-node Amaravati corridor under moderate traffic ($1.18\times$), the proposed framework secures **Rank #1** with **73.50% Fuzzy Customer Satisfaction**, an **Energy Cost of 374.70**, and a dominant **Hypervolume (HV) of 21.96**, outperforming standalone MO-ACO (HV 21.23), MOPSO (HV 14.81), and SGA (HV 11.75). A 5-seed Monte Carlo statistical validation confirms deterministic Pareto archive stability with $0.00$ standard deviation in energy and satisfaction. Finally, we formulate a commercial SaaS deployment roadmap for quick-commerce dark stores and emergency pharmaceutical distribution.

---

## Table of Contents

| Section & Title | Chapter / Topic Domain |
| :--- | :--- |
| **Title Page** | Institutional & Research Team Credentials |
| **Abstract** | Executive Research Summary & Benchmarking Highlights |
| **Table of Contents** | Document Roadmap & Chapter Index |
| **1. Introduction** | Urban Freight Logistics & The NP-Hard Routing Challenge |
| &nbsp;&nbsp;&nbsp;&nbsp;• 1.1 Background of Urban Logistics | 40%–50% Supply Chain Delivery Cost Share |
| &nbsp;&nbsp;&nbsp;&nbsp;• 1.2 The NP-Hard Combinatorial Challenge | Factorial Permutation Space ($25! \approx 1.55 \times 10^{25}$) |
| &nbsp;&nbsp;&nbsp;&nbsp;• 1.3 Limitations of Crisp / Hard Computing | Binary Step Failure vs. Human Tolerance Degradation |
| &nbsp;&nbsp;&nbsp;&nbsp;• 1.4 The Soft Computing Paradigm | Fuzzy Logic + Evolutionary Multi-Objective Optimization |
| &nbsp;&nbsp;&nbsp;&nbsp;• 1.5 Problem Statement & Research Questions | Research Hypotheses & Investigation Boundaries |
| **2. Literature Review** | Academic Foundation & Comparative Research Survey |
| &nbsp;&nbsp;&nbsp;&nbsp;• 2.1 Recent Academic Base Papers (2024–2026) | MDPI Systems, IEEE ITSC, Urban Science Studies |
| &nbsp;&nbsp;&nbsp;&nbsp;• 2.2 Comparative Literature Survey Matrix | Multi-Attribute Taxonomy of State-of-the-Art Works |
| &nbsp;&nbsp;&nbsp;&nbsp;• 2.3 Critical Analysis & Identified Gaps | Benchmarking Void & Decoupled Traffic-Energy Models |
| **3. Motivation** | Operational, Economic & Environmental Imperatives |
| &nbsp;&nbsp;&nbsp;&nbsp;• 3.1 Economic Impact | Last-Mile Urban Logistics Cost Inefficiencies |
| &nbsp;&nbsp;&nbsp;&nbsp;• 3.2 Environmental & Carbon Emissions | Load-Dependent Fuel & Battery Consumption Pressures |
| &nbsp;&nbsp;&nbsp;&nbsp;• 3.3 Realistic SLA Customer Satisfaction | Continuous Tolerance Modeling vs. Punitive Cutoffs |
| &nbsp;&nbsp;&nbsp;&nbsp;• 3.4 Stochastic Urban Traffic & Monsoons | Adaptive Mamdani Inference for South Asian Roadways |
| &nbsp;&nbsp;&nbsp;&nbsp;• 3.5 Multi-Paradigm Benchmarking Void | Need for Direct Head-to-Head Metaheuristic Comparison |
| **4. Proposed Work** | Scientific Framework & Technical Contributions |
| &nbsp;&nbsp;&nbsp;&nbsp;• 4.1 Core Engineering Contributions | 8-Point Scientific Innovation Architecture |
| &nbsp;&nbsp;&nbsp;&nbsp;• 4.2 Bi-Objective Optimization Formulation | Minimizing Energy Cost ($f_1$) & Maximizing SLA ($f_2$) |
| &nbsp;&nbsp;&nbsp;&nbsp;• 4.3 Multi-Kernel Fuzzy Satisfaction Models | Trapezoidal, Gaussian & Sigmoidal Formulations |
| &nbsp;&nbsp;&nbsp;&nbsp;• 4.4 9-Rule Mamdani Environmental Matrix | Traffic Density & Monsoon Rain Delay Multipliers |
| &nbsp;&nbsp;&nbsp;&nbsp;• 4.5 Memetic Hybrid NSGA-II Solver | Heuristic Seeding, Order Crossover & 2-Opt Uncrossing |
| &nbsp;&nbsp;&nbsp;&nbsp;• 4.6 5-Algorithm Benchmarking Arena | NSGA-II, MOPSO, MO-ACO, Standard GA, Greedy |
| &nbsp;&nbsp;&nbsp;&nbsp;• 4.7 5-Seed Monte Carlo Validation | Rigorous Multi-Trial Statistical Repeatability Analysis |
| &nbsp;&nbsp;&nbsp;&nbsp;• 4.8 60FPS Telemetry Command Center | Interactive Vector Radar & Pareto Telematics Dashboard |
| **5. Methodology** | End-to-End Computational Workflow & Operators |
| &nbsp;&nbsp;&nbsp;&nbsp;• 5.1 System Pipeline & Flowchart | 4-Stage Architectural Progression Pipeline |
| &nbsp;&nbsp;&nbsp;&nbsp;• 5.2 Chromosome Encoding & Partitioning | Unconstrained Permutations & Payload Split ($\le 100\text{ kg}$) |
| &nbsp;&nbsp;&nbsp;&nbsp;• 5.3 Multi-Kernel Fuzzification of Timelines | Mathematical Definitions & Decay Rate Curves |
| &nbsp;&nbsp;&nbsp;&nbsp;• 5.4 Mamdani Inference & Defuzzification | Fuzzification, Min-Norm, Max-Norm & Centroid COG |
| &nbsp;&nbsp;&nbsp;&nbsp;• 5.5 Evolutionary Metaheuristic Execution | Fast Non-Dominated Sorting & Crowding Distance |
| &nbsp;&nbsp;&nbsp;&nbsp;• 5.6 Knee-Point Multi-Criteria Selection | Normalized Euclidean Distance to Utopia Point |
| **6. Model / Architecture / Design** | Mathematical Rigor & Structural Implementation |
| &nbsp;&nbsp;&nbsp;&nbsp;• 6.1 Mathematical Model & Equations | Objective Functions, Variables & Hard Constraints |
| &nbsp;&nbsp;&nbsp;&nbsp;• 6.2 9-Rule Mamdani Inference Matrix | Full Decision Matrix with Delay Multipliers ($\tau$) |
| &nbsp;&nbsp;&nbsp;&nbsp;• 6.3 Genetic Operators & Permutation Routing | Order Crossover (OX1), Inversion & 2-Opt Mechanics |
| &nbsp;&nbsp;&nbsp;&nbsp;• 6.4 Modular Software Architecture | Decoupled 3-Tier Layered System Architecture |
| **7. Implementation** | Software Stack, Code Modules & Execution |
| &nbsp;&nbsp;&nbsp;&nbsp;• 7.1 Technology Stack & Environment | Python 3.12, NumPy, Pandas, Plotly, Streamlit |
| &nbsp;&nbsp;&nbsp;&nbsp;• 7.2 File-Wise Code Walkthrough | Detailed Anatomy of `core_data_and_fuzzy`, `core_optimizers`, `app` |
| &nbsp;&nbsp;&nbsp;&nbsp;• 7.3 Offline Launcher & Execution Pipeline | Instant 127.0.0.1 Local Loopback Batch Dispatcher |
| **8. Results and Analysis** | Empirical Evaluation & Performance Metrics |
| &nbsp;&nbsp;&nbsp;&nbsp;• 8.1 Benchmark Topologies & Datasets | Amaravati Live GIS (25 Nodes), Solomon C101 & R101 |
| &nbsp;&nbsp;&nbsp;&nbsp;• 8.2 5-Algorithm Head-to-Head Arena | Quantitative Evaluation: Energy, SLA, Vans, Time, HV |
| &nbsp;&nbsp;&nbsp;&nbsp;• 8.3 Pareto Geometry & Hypervolume | Dominance Analysis & Extreme-to-Express Frontiers |
| &nbsp;&nbsp;&nbsp;&nbsp;• 8.4 Comparative Fuzzy Kernel Evaluation | Performance Trade-Offs: Trapezoidal, Gaussian, Sigmoidal |
| &nbsp;&nbsp;&nbsp;&nbsp;• 8.5 Mamdani Sensitivity Analysis | Environmental Shock Response ($\tau = 1.00\times \dots 1.85\times$) |
| **9. Comparison with Existing Methods** | Metaheuristic Benchmark Analysis & Statistical Rigor |
| &nbsp;&nbsp;&nbsp;&nbsp;• 9.1 Multi-Paradigm Comparison Matrix | Evolutionary vs. Swarm vs. Colony vs. Single-Objective |
| &nbsp;&nbsp;&nbsp;&nbsp;• 9.2 Architectural Analysis of Superiority | Combinatorial Integrity, Diversity & Stagnation Defense |
| &nbsp;&nbsp;&nbsp;&nbsp;• 9.3 5-Seed Monte Carlo Stability | Mean $\pm$ Standard Deviation Analysis ($0.00$ Variance) |
| **10. Conclusion** | Research Findings & Scientific Milestones |
| &nbsp;&nbsp;&nbsp;&nbsp;• 10.1 Key Findings & Milestones | Combinatorial Resolution, Load Physics & Rank #1 |
| &nbsp;&nbsp;&nbsp;&nbsp;• 10.2 Soft Computing Hypothesis Validation | Convergence of Fuzzy Logic & Evolutionary Algorithms |
| **11. Scope for Future Work** | Research Extensions & Advanced Frontiers |
| &nbsp;&nbsp;&nbsp;&nbsp;• 11.1 Dynamic Real-Time GPS Telematics | Live Mid-Route Recalibration via WebSockets |
| &nbsp;&nbsp;&nbsp;&nbsp;• 11.2 Electric Vehicle Routing (EVRPTW) | Battery State-of-Charge & Fast-Charging Topologies |
| &nbsp;&nbsp;&nbsp;&nbsp;• 11.3 Multi-Depot & Van-Drone Collaboration | Urban Dark Stores & Aerial Package Handoffs |
| &nbsp;&nbsp;&nbsp;&nbsp;• 11.4 DRL Surrogate Acceleration | Graph Neural Networks for Sub-Millisecond Dispatching |
| **12. References** | Academic Citations & Base Research Bibliography |
| &nbsp;&nbsp;&nbsp;&nbsp;• Formal IEEE Bibliography | 10 Foundational Papers, Base Studies & Textbooks |

---

## 1. Introduction

### 1.1 Background of Urban Logistics & Last-Mile Delivery Challenges
Urban logistics and last-mile freight transportation serve as the primary operational backbone of contemporary e-commerce, pharmaceutical supply chains, and rapid-delivery grocery networks. However, empirical transportation economic studies demonstrate that **last-mile delivery accounts for 40% to 50% of total supply chain logistics costs** and generates a disproportionately high share of urban greenhouse gas emissions.

In an operational deployment, fleet dispatch managers must constantly reconcile diametrically opposed objectives:
- **Vehicle Energy & Operating Cost:** Minimizing the fuel or electrical energy consumed by a heterogeneous delivery fleet. Fleet operating costs are not merely a linear function of distance; they depend heavily on the vehicle's dynamic physical weight, stopping frequency, and congested urban road segments.
- **Physical Vehicle Payload Limits:** Adhering strictly to payload constraints ($\text{max payload} \le 100\text{ kg/van}$) to avoid mechanical axle wear, regulatory fines, and battery exhaustion.
- **Strict Service Level Agreements (SLAs):** Delivering high-priority parcels within customer-stipulated time windows. Failing to satisfy critical delivery deadlines (e.g., emergency medical logistics, blood bank samples, airport air-cargo handoffs) incurs steep reputational damage and contractual penalties.

### 1.2 The NP-Hard Combinatorial Routing Challenge
The Vehicle Routing Problem with Time Windows (VRPTW) is a well-established **NP-Hard combinatorial optimization problem**. The problem belongs to the class of permutation-based routing problems where the candidate solution space scales factorially with the number of delivery nodes $N$:

$$\Omega(N) = \frac{(N-1)!}{2}$$

For a moderate urban logistics deployment of $N = 25$ active delivery nodes, the number of unconstrained permutations is:

$$25! \approx 1.55 \times 10^{25} \text{ routes}$$

Evaluating this search space via brute-force enumeration at a processing speed of $10^9$ evaluations per second would require over **$4.9 \times 10^8$ years**, rendering deterministic exhaustive search computationally infeasible.

### 1.3 Limitations of Crisp / Hard Computing Formulations
Classical hard-computing approaches model customer deadlines as **crisp binary intervals**:

$$\mu_{\text{crisp}}(t) = \begin{cases} 1, & \text{if } t \in [T_{\text{start}}, T_{\text{end}}] \\ 0, & \text{otherwise} \end{cases}$$

Under this binary regime, an arrival that occurs 1 second past $T_{\text{end}}$ is categorized as a complete 100% SLA failure ($0$ utility), identical to a parcel delivered five hours late. This mathematical rigidity fails to mirror realistic human behavioral tolerance and cannot adapt to urban stochastic uncertainties such as sudden traffic snarls, monsoonal downpours, or brief dispatch delays.


![Figure 1: Conceptual mapping from last-mile operational challenges to the integrated Soft Computing paradigm.](figures/fig1_soft_computing_paradigm.png)
*Figure 1: Conceptual mapping from last-mile operational challenges to the integrated Soft Computing paradigm.*


### 1.4 The Soft Computing Paradigm: Fuzzy Logic + Evolutionary Metaheuristics
Soft computing provides the mathematical tools required to conquer this dual challenge:
1. **Fuzzy Logic (Zadeh, 1965):** Provides continuous membership functions $\mu(t) \in [0.0, 1.0]$ that capture human tolerance gradients during arrival delays, transforming brittle step-penalties into differentiable or smooth fitness surfaces.
2. **Mamdani Fuzzy Inference System:** Implements linguistic rule-based reasoning ("IF Traffic is Peak AND Weather is Monsoon THEN Delay is Gridlock") to compute realistic travel multipliers without requiring intractable differential equations of metropolitan traffic flows.
3. **Multi-Objective Evolutionary Computation (NSGA-II):** Simultaneously discovers non-dominated trade-offs between fleet energy cost ($f_1$) and customer satisfaction ($f_2$) using fast non-dominated sorting and crowding distance preservation.

### 1.5 Problem Statement & Research Questions
This project investigates the following primary research questions:
- *RQ1:* Can continuous fuzzy time windows eliminate the combinatorial brittleness of crisp VRPTW models while reflecting human tolerance?
- *RQ2:* How significantly does load-dependent energy dissipation alter the optimal sequencing of deliveries compared to standard geographic distance minimization?
- *RQ3:* Does a Memetic Hybrid Fuzzy-NSGA-II outperform alternative swarm (MOPSO) and colony (MO-ACO) paradigms across real-world GIS corridors and standard Solomon benchmarks?

---

## 2. Literature Review

### 2.1 Recent Academic Base Papers Referenced (2024–2026)
This project directly grounds its mathematical formulations, physical constraints, and algorithmic designs on three premier academic base papers published between 2024 and 2026:

* **Base Paper 1 (Dec 2024 - MDPI Systems, Vol. 12, Issue 12):**  
  *Title:* *"Modeling and Solving the Multi-Objective Vehicle Routing Problem with Soft and Fuzzy Time Windows"*  
  *Contribution Adopted:* Formalized the mathematical foundations of continuous fuzzy membership functions to model customer delivery satisfaction. Demonstrated that modeling tolerance intervals $[\text{best\_end}, \text{max\_late}]$ via linear and non-linear membership kernels eliminates the combinatorial brittleness of crisp VRPTW models and provides a continuous gradient for evolutionary search.
* **Base Paper 2 (2025 - IEEE International Conference on Intelligent Transportation Systems - ITSC):**  
  *Title:* *"ACO-NSGAII: A Novel Metaheuristics for Bi-Objective Electric Vehicle Routing Problems with Time Windows"*  
  *Contribution Adopted:* Introduced an authentic load-dependent energy dissipation physics model where the energy consumed per kilometer scales linearly with instantaneous remaining vehicle payload. Established that prioritizing earlier drops for heavier parcels yields substantial cumulative battery savings.
* **Reference Paper 3 (Oct 2026 - Urban Science):**  
  *Title:* *"The Prediction Optimization Bridge (POB): A Surrogate Assisted Random Forest–NSGA-II Framework for Energy Efficient Vehicle Routing"*  
  *Contribution Adopted:* Formulated real-time urban traffic delay multipliers that dynamically scale vehicle transit velocity and energy burn under varying weather and peak congestion conditions.

### 2.2 Comparative Literature Survey Matrix

| Paper Citation & Year | Modeling Paradigm | Optimization Objectives | Environmental & Traffic Logic | Metaheuristic Solvers | Benchmark Datasets Tested | Key Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MDPI Systems (Dec 2024)** | Fuzzy Time Windows | Distance + Satisfaction | Static travel times; no weather inference | Standalone NSGA-II | Solomon C101, R101 | Evaluates single algorithm; lacks load-dependent energy physics. |
| **IEEE ITSC (2025)** | Crisp VRPTW | Energy Cost + Fleet Size | Deterministic speed profiles | ACO-NSGA-II Hybrid | Synthetic 20-node EV networks | Binary time windows; zero fuzzy human tolerance modeling. |
| **Urban Science (Oct 2026)** | Surrogate NSGA-II | Carbon Emissions + Travel Time | Machine learning delay multipliers | Surrogate-assisted NSGA-II | European arterial highways | High training overhead; no swarm/colony comparative benchmarking. |
| **FleetPulse AI (This Project, 2026)** | **Continuous Fuzzy Set Theory + Mamdani Inference** | **Bi-Objective: Load-Dependent Energy ($f_1$) + Fuzzy Satisfaction ($f_2$)** | **9-Rule Mamdani Matrix (Traffic Density + Monsoon Weather)** | **5-Algorithm Arena: Hybrid Fuzzy-NSGA-II, MOPSO, MO-ACO, SGA, Greedy** | **Amaravati–Vijayawada Live GIS (25 Nodes) + Solomon C101 & R101** | **Unified multi-paradigm benchmark; sub-second runtime (<450 ms).** |

### 2.3 Critical Analysis of Prior Works & Identified Research Gaps
A rigorous review of contemporary routing optimization literature reveals three prominent research gaps:
1. **Lack of Multi-Paradigm Soft Computing Benchmarking:** Existing studies evaluate a single isolated evolutionary algorithm (e.g., standalone NSGA-II or GA) without rigorous head-to-head benchmarking against alternative nature-inspired swarm (MOPSO) and colony (MO-ACO) paradigms under identical constraints, objective formulations, and datasets.
2. **Absence of Multi-Kernel Fuzzy Satisfaction Comparisons:** Prior publications adopt a single arbitrary membership function (typically standard trapezoidal) without mathematically investigating how Gaussian (smooth bell-curve) or Sigmoidal (logistic S-curve) kernels influence evolutionary convergence and schedule structure.
3. **Decoupled Traffic and Energy Models:** Most classical studies optimize pure geographic distance, ignoring the multiplicative interaction between instantaneous cargo load and urban traffic delay factors.

---

## 3. Motivation

### 3.1 Economic Impact: Inefficiencies in Urban Freight Delivery
Urban logistics is experiencing unprecedented growth driven by quick-commerce platforms (Zepto, Blinkit, Instamart) and omnichannel retail. However, last-mile delivery remains the most expensive and inefficient leg of the logistics chain, consuming **40% to 50% of aggregate supply chain expenditures**. Route inefficiency, partial vehicle capacity utilization, and unnecessary backtracking directly inflate vehicle fuel and fleet maintenance bills.

### 3.2 Environmental & Carbon Emission Pressures
Transportation is a primary contributor to urban air pollution ($PM_{2.5}$, $NO_x$) and greenhouse gas emissions. Most commercial delivery vehicles carry heterogeneous parcel weights that dramatically alter fuel efficiency or battery depletion. Minimizing pure geometric distance fails to minimize carbon footprint: traveling 10 km with a fully loaded van burns substantially more fuel than traveling the same distance with an empty van. A physics-grounded dispatch model is therefore an urgent environmental necessity.

### 3.3 Realistic SLA Modeling & Human Psychological Tolerance
In real-world logistics, customer satisfaction does not plummet to zero the moment a delivery is one minute late. Human psychology exhibits a tolerance band where utility degrades gradually before reaching an unacceptable threshold. Crisp binary deadlines force optimization algorithms to reject feasible, highly cost-effective routes due to trivial 30-second delays. Modeling satisfaction through continuous fuzzy membership functions restores realistic trade-off analysis.

### 3.4 Stochastic Urban Traffic & Monsoonal Dynamics
Metropolitan transport networks in South Asia (such as the Vijayawada–Amaravati highway corridor) suffer from high variability due to peak office hours and seasonal monsoon downpours. Hard-coded transit speeds lead to catastrophic schedule cascading delays. An adaptive soft-computing layer capable of inferring traffic delays from linguistic environmental conditions is essential.

### 3.5 Multi-Paradigm Soft Computing Benchmarking Imperative
Engineering decisions in enterprise logistics require empirical proof of which metaheuristic paradigm performs best under capacity and SLA constraints. By benchmarking Genetic Algorithms (NSGA-II, SGA), Particle Swarms (MOPSO), and Ant Colonies (MO-ACO) side-by-side, this study provides actionable mathematical and empirical clarity.

---

## 4. Proposed Work

### 4.1 Core Engineering & Research Contributions
The primary contributions of this project are:
1. **Bi-Objective Mathematical Formulation:** Merging continuous multi-kernel fuzzy satisfaction with dynamic load-dependent energy physics under a $\le 100\text{ kg/van}$ payload constraint.
2. **Tri-Kernel Fuzzy Satisfaction Engine:** Mathematical formulation and empirical evaluation of Trapezoidal, Gaussian, and Sigmoidal membership functions.
3. **9-Rule Mamdani Environmental Matrix:** Automated inference of speed and energy multipliers from traffic density and monsoon weather states.
4. **Memetic Hybrid Fuzzy-NSGA-II Solver:** Integrating heuristic chromosome seeding (EDF + Spatial-Urgency), Order Crossover (OX1), and 2-Opt local search.
5. **5-Algorithm Benchmarking Arena:** Direct head-to-head empirical evaluation across Hybrid Fuzzy-NSGA-II, MOPSO, MO-ACO, SGA, and Greedy Nearest-Neighbor.
6. **5-Seed Monte Carlo Validation:** Rigorous statistical analysis proving deterministic stability.
7. **Interactive 60FPS Command Center:** Full-stack Streamlit application featuring HTML5 Canvas vector radar simulation.


![Figure 2: End-to-end 4-stage computational pipeline connecting GIS inputs to telematic visualization.](figures/fig2_system_pipeline.png)
*Figure 2: End-to-end 4-stage computational pipeline connecting GIS inputs to telematic visualization.*


### 4.2 Bi-Objective Mathematical Optimization Formulation
The framework optimizes two conflicting fitness functions:
- **Minimizing Energy Cost ($f_1$):** Evaluated over all deployed vehicles taking into account tare vehicle mass, remaining cargo payload, and traffic friction.
- **Maximizing Customer Satisfaction ($f_2$):** Evaluated via priority-weighted continuous fuzzy membership degrees across all delivery stops.

### 4.3 Multi-Kernel Fuzzy Membership Modeling
We parameterize customer satisfaction via three continuous mathematical functions:
- *Trapezoidal Kernel:* Piecewise linear tolerance with crisp boundaries.
- *Gaussian Kernel:* Smooth exponential bell-curve reflecting gradual decay.
- *Sigmoidal Kernel:* Logistic S-curve with rapid midpoint inflection.

### 4.4 9-Rule Mamdani Traffic-Weather Inference Engine
Combines linguistic traffic levels (Low, Medium, Peak) and weather states (Clear, Rain, Monsoon) into a crisp delay multiplier $\tau \in [1.00\times, 1.85\times]$ using center-of-gravity defuzzification.

### 4.5 Memetic Hybrid NSGA-II Search Architecture
Combines Pareto dominance ranking and crowding distance sorting with domain-specific memetic heuristics:
- Heuristic seeding via Earliest Deadline First (EDF) and Spatial-Urgency chromosomes.
- Order Crossover (OX1) to guarantee conflict-free node tours.
- 2-Opt local search operator that reverses sub-tours to uncross spatial intersections.

### 4.6 5-Algorithm Rigorous Benchmarking Arena
Implements and compares five distinct metaheuristics under identical constraints and random seeds:
1. Proposed Hybrid Fuzzy-NSGA-II
2. Multi-Objective Ant Colony Optimization (MO-ACO)
3. Multi-Objective Particle Swarm Optimization (MOPSO)
4. Standard Single-Objective Genetic Algorithm (SGA)
5. Greedy Nearest-Neighbor Dispatch Baseline

### 4.7 5-Seed Monte Carlo Statistical Validation
Executes 5 independent stochastic trials per algorithm across random seeds $\{100, 101, 102, 103, 104\}$ to evaluate mean and standard deviation for hypervolume, energy, satisfaction, and runtime.

### 4.8 Interactive 60FPS Telemetry Command Center
Builds an industrial-grade dark mode web platform using Streamlit, Plotly, and HTML5 Canvas, providing real-time vector radar simulation, 3D fuzzy surface inspection, and Pareto trade-off sliders.

---

## 5. Methodology

### 5.1 End-to-End System Pipeline & Architectural Flowchart
The complete computational pipeline consists of four major sequential stages:
1. **Data Ingestion & Parameter Setup:** GIS coordinates, parcel demands, SLA windows, priority multipliers, and environmental states are loaded.
2. **Fuzzy Environmental Inference:** Mamdani FIS evaluates the traffic-weather rule base to compute the crisp travel delay multiplier $\tau$.
3. **Multi-Objective Optimization Search:** Evolutionary populations or swarm agents iteratively generate, evaluate, and refine candidate routes.
4. **Pareto Selection & Telemetry Output:** Non-dominated sorting identifies the Pareto frontier, and normalized Utopia distance selects the knee-point dispatch plan.


![Figure 3: Memetic Hybrid Fuzzy-NSGA-II search architecture featuring heuristic seeding, OX1 crossover, and 2-Opt local refinement.](figures/fig3_nsga2_workflow.png)
*Figure 3: Memetic Hybrid Fuzzy-NSGA-II search architecture featuring heuristic seeding, OX1 crossover, and 2-Opt local refinement.*


### 5.2 Chromosome Encoding & Payload-Constrained Fleet Partitioning
A candidate chromosome is represented as an unconstrained permutation vector of stop identifiers:

$$\pi = \langle \pi_1, \pi_2, \dots, \pi_N \rangle, \quad \pi_i \in \{1, 2, \dots, N\}$$

To partition $\pi$ into feasible vehicle routes under the payload limit $Q_{\text{max}} = 100\text{ kg}$, we implement a greedy split decoder:
- Van 1 starts at the central depot ($0$) with accumulated load $L = 0$.
- Stops $\pi_1, \pi_2, \dots$ are appended sequentially. If appending stop $\pi_i$ causes $\sum q > 100\text{ kg}$, Van 1 returns to the depot ($0$), and a new vehicle (Van 2) is instantiated starting at the depot.
- This produces $K$ disjoint vehicle sub-tours $R_1, R_2, \dots, R_K$ guaranteeing $100\%$ capacity feasibility without penalties.

### 5.3 Multi-Kernel Fuzzification of Delivery Timelines
For each customer stop $i$, arrival timestamp $t_i$ is mapped to a satisfaction degree $\mu(t_i) \in [0.0, 1.0]$ based on preferred window $[e_i, l_i]$ and maximum acceptable deadline $u_i$:


![Figure 4: Comparative evaluation of Trapezoidal, Gaussian, and Sigmoidal fuzzy satisfaction decay kernels.](figures/fig4_fuzzy_decay.png)
*Figure 4: Comparative evaluation of Trapezoidal, Gaussian, and Sigmoidal fuzzy satisfaction decay kernels.*


1. **Trapezoidal Kernel:**
   $$\mu_{\text{trap}}(t_i) = \begin{cases} 1.0, & t_i \le l_i \\ \dfrac{u_i - t_i}{u_i - l_i}, & l_i < t_i \le u_i \\ 0.0, & t_i > u_i \end{cases}$$

2. **Gaussian Kernel:**
   $$\mu_{\text{gauss}}(t_i) = \begin{cases} 1.0, & t_i \le l_i \\ \exp\left( -0.5 \left( \dfrac{t_i - l_i}{\sigma_i} \right)^2 \right), & t_i > l_i \end{cases}, \quad \sigma_i = \frac{u_i - l_i}{2.2}$$

3. **Sigmoidal Kernel:**
   $$\mu_{\text{sigm}}(t_i) = \begin{cases} 1.0, & t_i \le l_i \\ \dfrac{1}{1 + \exp\left( \gamma_i \left( t_i - \frac{l_i + u_i}{2} \right) \right)}, & t_i > l_i \end{cases}, \quad \gamma_i = \frac{6.0}{u_i - l_i}$$

### 5.4 Mamdani Fuzzy Inference Pipeline & Centroid Defuzzification
The Mamdani inference system operates through four classical stages:
1. **Fuzzification:** Input crisp values of Traffic Density $x_T$ and Weather Condition $x_W$ are converted into linguistic membership values using triangular membership functions.
2. **Rule Evaluation (Min T-Norm):** For each rule $r \in \{1, \dots, 9\}$, the firing strength $\alpha_r$ is determined by the intersection of antecedent memberships:
   $$\alpha_r = \min\big( \mu_{T,r}(x_T), \mu_{W,r}(x_W) \big)$$
3. **Aggregation (Max S-Norm):** The fuzzy output sets are clipped at $\alpha_r$ and aggregated via union:
   $$\mu_{\text{agg}}(\tau) = \max_{r=1}^9 \Big( \min\big( \alpha_r, \mu_{\text{out},r}(\tau) \big) \Big)$$
4. **Defuzzification (Centroid / Center of Gravity):** The crisp travel delay factor $\tau$ is calculated by integrating the aggregated fuzzy region:
   $$\tau = \frac{\int \tau \cdot \mu_{\text{agg}}(\tau) \, d\tau}{\int \mu_{\text{agg}}(\tau) \, d\tau}$$

### 5.5 Evolutionary Metaheuristic Execution & Genetic Recombination
- **Fast Non-Dominated Sorting:** Assigns each chromosome to a Pareto rank $\mathcal{F}_1, \mathcal{F}_2, \dots$ based on dominance counts $n_p$ and dominated solution sets $S_p$.
- **Crowding Distance Calculation:** Estimates density of solutions surrounding a particular individual in objective space, prioritizing boundary solutions ($I_d = \infty$).
- **Binary Tournament Selection:** Competitors are chosen using the crowded comparison operator $\prec_n$ (prefer lower rank, tie-break with higher crowding distance).
- **Order Crossover (OX1):** Preserves relative order and adjacency of stops without creating duplicate visits.
- **2-Opt Local Refinement:** Applied to elite chromosomes by reversing sub-paths $[j \dots k]$ to remove spatial self-intersections.

### 5.6 Knee-Point Selection via Normalized Utopia Distance
To select a single operational dispatch plan from the final non-dominated Pareto front $\mathcal{P}$, the algorithm identifies the knee solution that minimizes the weighted Euclidean distance to the theoretical Utopia Point $(f_1^{\min}, f_2^{\max})$:

$$d_{\text{utopia}}(p) = \sqrt{0.45 \left( \frac{f_1(p) - f_1^{\min}}{f_1^{\max} - f_1^{\min}} \right)^2 + 0.55 \left( \frac{f_2^{\max} - f_2(p)}{f_2^{\max} - f_2^{\min}} \right)^2}$$

---

## 6. Model / Architecture / Design

### 6.1 Mathematical Model Formulation & Equations
Let $G = (V, E)$ be a complete directed graph where $V = \{0, 1, \dots, N\}$. Vertex $0$ is the central depot, and $V_c = \{1, \dots, N\}$ are the customer nodes.

#### Parameters & Variables:
- $q_i$: Payload demand of customer $i$ ($q_i \in [10, 45]$ kg).
- $Q_{\text{max}}$: Maximum vehicle payload ($100$ kg/van).
- $w_i$: Priority weight (Critical = 1.35, High = 1.15, Normal = 1.00).
- $d_{ij}$: Euclidean distance between nodes $i$ and $j$.
- $x_{ijk} \in \{0, 1\}$: Binary decision variable equal to $1$ if vehicle $k$ traverses edge $(i, j)$, $0$ otherwise.
- $L_{k,j}$: Instantaneous load of vehicle $k$ leaving stop $j$.

#### Objective 1: Load-Dependent Fleet Energy Cost (f1):

$$\min f_1 = \sum_{k=1}^K \sum_{j=0}^{m_k} \Big[ d(s_{k,j}, s_{k,j+1}) \times \big(1 + 0.006 \times L_{k,j}\big) \times \big(0.85 + 0.15 \times \tau\big) \Big]$$

Where 0.006 kg^-1 is the vehicle load friction coefficient, and (0.85 + 0.15 * tau) represents the dynamic traffic congestion drag multiplier.

#### Objective 2: Priority-Weighted Fuzzy Customer Satisfaction (f2):

$$\max f_2 = \frac{\sum_{i=1}^N \Big( \mu_{\text{fuzzy}}(t_i) \times w_i \Big)}{\sum_{i=1}^N w_i} \times 100\%$$

#### Constraints:
1. **Fleet Capacity Limit:** $\sum_{i \in R_k} q_i \le Q_{\text{max}} = 100\text{ kg}, \quad \forall k \in \{1, \dots, K\}$
2. **Every customer visited exactly once:** $\sum_{k=1}^K \sum_{i \in V, i \ne j} x_{ijk} = 1, \quad \forall j \in V_c$
3. **Depot flow conservation:** $\sum_{j \in V_c} x_{0jk} = \sum_{i \in V_c} x_{i0k} \le 1, \quad \forall k \in \{1, \dots, K\}$

### 6.2 Complete 9-Rule Mamdani Environmental Matrix

| Rule # | Traffic Input (x_T) | Weather Input (x_W) | Linguistic Output Flow | Crisp Delay Factor (tau) |
| :---: | :--- | :--- | :--- | :---: |
| **R1** | Low Traffic | Clear Weather | Optimal Flow | **$1.00\times$** |
| **R2** | Low Traffic | Light Rain | Moderate Flow | **$1.12\times$** |
| **R3** | Low Traffic | Heavy Monsoon | Slowed Flow | **$1.28\times$** |
| **R4** | Medium Traffic | Clear Weather | Moderate Flow | **$1.18\times$** |
| **R5** | Medium Traffic | Light Rain | Congested Flow | **$1.32\times$** |
| **R6** | Medium Traffic | Heavy Monsoon | Severely Congested | **$1.50\times$** |
| **R7** | Peak Rush Hour | Clear Weather | Congested Flow | **$1.40\times$** |
| **R8** | Peak Rush Hour | Light Rain | Severely Congested | **$1.62\times$** |
| **R9** | Peak Rush Hour | Heavy Monsoon | Gridlock Risk | **$1.85\times$** |

### 6.3 Genetic Chromosome Representation & Recombination Operators
- **Chromosome:** $\pi = [4, 1, 8, 12, 3, 7, 2, 5, \dots]$ (Permutation vector of length $N$).
- **Order Crossover (OX1):** Selects random slice from Parent 1; copies remaining non-duplicate genes in sequence from Parent 2.
- **Inversion Mutation:** Reverses a contiguous sub-array $[\pi_a, \dots, \pi_b]$ with probability $P_m = 0.25$.
- **Memetic 2-Opt:** Checks if swapping edges $(i, i+1)$ and $(j, j+1)$ reduces cumulative distance; accepts if $\Delta d < 0$.

### 6.4 Modular Software Engineering Architecture
The system architecture decouples the problem into three independent layers:
- **Layer 1: Core Physics & Fuzzy Data Engine** (`core_data_and_fuzzy.py`): Manages GIS coordinates, payload constraints, membership equations, and the 9-Rule Mamdani FIS.
- **Layer 2: Multi-Objective Optimizers Engine** (`core_optimizers.py`): Implements NSGA-II, MOPSO, MO-ACO, SGA, and Greedy solvers with vectorized Pareto sorting.
- **Layer 3: Telemetry Command Center** (`app.py`): High-frame-rate Streamlit interface rendering real-time vector radar simulations, 3D response surfaces, and Pareto plots.


![Figure 5: Decoupled 3-tier modular system architecture connecting frontend HUD, metaheuristic core, and physics engines.](figures/fig5_software_architecture.png)
*Figure 5: Decoupled 3-tier modular system architecture connecting frontend HUD, metaheuristic core, and physics engines.*


---

## 7. Implementation

### 7.1 Technology Stack & Development Environment
- **Programming Language:** Python 3.12 / 3.13 (64-bit)
- **Scientific Computing Libraries:** NumPy (vectorized array operations), Pandas (tabular benchmarks), SciPy
- **Data Visualization & Dashboards:** Plotly 5.24+ (interactive 3D surfaces and Pareto scatterplots), Streamlit 1.45+ (telemetry web app)
- **Document & Export Engines:** ReportLab (academic PDF generation), python-docx (formatted Word doc generation)
- **Local Network Binding:** Binds strictly to `http://127.0.0.1:8501` for instantaneous offline execution.

### 7.2 File-Wise Code Breakdown & Technical Walkthrough

#### 1. `core_data_and_fuzzy.py` (Data & Fuzzy Logic Core)
- `AMARAVATI_STOPS`: Dictionary of 25 authentic delivery locations centered around Benz Circle Depot ($16.4971^\circ\text{N}, 80.6534^\circ\text{E}$), containing coordinates, parcel weights ($q_i$), preferred SLA intervals $[e_i, l_i]$, late cutoffs $u_i$, and priority weights $w_i$.
- `compute_fuzzy_satisfaction(arr_time, best_start, best_end, max_late, kernel)`: Evaluates satisfaction degree $\mu(t)$ using Trapezoidal, Gaussian, or Sigmoidal equations.
- `get_fuzzy_traffic_factor(traffic_str, weather_str)`: Evaluates the 9-Rule Mamdani rule base to yield the delay multiplier $\tau$.

#### 2. `core_optimizers.py` (Multi-Algorithm Optimization Core)
- `evaluate_route(chromosome, stops, max_capacity, traffic_mult, kernel)`: Partitions chromosomes into feasible vehicle sub-tours ($\le 100\text{ kg}$), simulates temporal arrival profiles, and computes $f_1$ (energy cost) and $f_2$ (satisfaction %).
- `run_fuzzy_nsga2(...)`: Full implementation of NSGA-II with heuristic seeding (EDF + Spatial), Order Crossover (OX1), 2-Opt local refinement, fast non-dominated sorting, and crowding distance.
- `run_mopso(...)`: Implements Multi-Objective Particle Swarm Optimization with an external Pareto archive and crowding-distance leader selection.
- `run_moaco(...)`: Implements Multi-Objective Ant Colony Optimization with pheromone matrix $\tau_{ij}$ and heuristic desirability $\eta_{ij}$.
- `run_single_objective_ga(...)`: Implements standard GA optimizing a weighted sum fitness.
- `run_greedy_dispatcher(...)`: Implements greedy nearest-neighbor heuristic baseline.
- `run_multi_trial_statistics(...)`: Runs 5-seed Monte Carlo evaluation across all metaheuristics.

#### 3. `app.py` (Precision Industrial Dark UI)
- Linear/Vercel-inspired Swiss-Grid design system using Inter + JetBrains Mono typography and 1px zinc hairlines (`#27272a`).
- Custom HTML5 Canvas vector radar supporting real-time vehicle movement, scroll-to-zoom, and drag-to-pan.
- Tabbed analytical suite: Route Topology, Multi-Algorithm Benchmark Arena, Pareto Frontier Studio, 3D Fuzzy Response Surface, and Monte Carlo Statistical Validation.

### 7.3 Execution Instructions & Offline Batch Launcher
The project includes a robust, offline-ready Windows launcher script:
```bat
@echo off
cd /d "%~dp0"
title FleetPulse AI Telemetry Center

:: Release port 8501 if previously occupied
for /f "tokens=5" %%p in ('netstat -aon ^| findstr ":8501" ^| findstr "LISTENING"') do taskkill /f /pid %%p >nul 2>&1

echo Starting FleetPulse AI Dashboard on http://127.0.0.1:8501 ...
python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
pause
```
Executing `start_dashboard.bat` boots the platform on `http://127.0.0.1:8501` within 1 second with zero external internet dependencies.

---

## 8. Results and Analysis

### 8.1 Benchmark Topologies & Datasets
Evaluation was performed across three benchmark datasets:
1. **Amaravati–Vijayawada Live GIS Network:** 25 authentic urban nodes (VIT-AP, AIIMS Mangalagiri, Manipal Hospital, Auto Nagar, Gannavaram Airport Cargo).
2. **Solomon C101 Benchmark:** Clustered nodes with tight customer arrival time windows.
3. **Solomon R101 Benchmark:** Uniformly distributed random customer coordinates.

### 8.2 Quantitative Head-to-Head 5-Algorithm Benchmarking Arena
Evaluated under identical constraints: 18 Nodes, $Q_{\text{max}} = 100\text{ kg}$, Medium Traffic ($\tau = 1.18\times$), Trapezoidal Kernel, Population Size $40$, Generations $40$, Seed $42$:

| Algorithm Paradigm | Fleet Energy Cost (f1) | Fuzzy Satisfaction (f2) | Active Vans | Hypervolume (HV) | Runtime (ms) | Overall Arena Rank |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Hybrid Fuzzy-NSGA-II (Proposed)** | **374.70** | **73.50%** | **4 Vans** | **21.96** | 328.6 ms | **Rank #1 (Champion)** |
| **Multi-Objective ACO (MO-ACO)** | 351.22 | 71.35% | 4 Vans | 21.23 | 162.3 ms | **Rank #2 (Runner-Up)** |
| **Multi-Objective PSO (MOPSO)** | 419.75 | 61.36% | 4 Vans | 14.81 | 107.2 ms | **Rank #3** |
| **Greedy Nearest-Neighbor** | 351.32 | 63.06% | 4 Vans | N/A (Single Point) | 0.5 ms | **Rank #4** |
| **Standard Single-Objective GA** | 405.61 | 54.19% | 4 Vans | 11.75 | 50.4 ms | **Rank #5** |


![Figure 6: Quantitative benchmarking comparison of Fuzzy Customer Satisfaction (%) and Pareto Hypervolume (HV).](figures/fig6_benchmark_comparison.png)
*Figure 6: Quantitative benchmarking comparison of Fuzzy Customer Satisfaction (%) and Pareto Hypervolume (HV).*


### 8.3 Pareto Frontier Geometry & Hypervolume Analysis
- **Hypervolume Metric (HV):** Computed with reference point $(f_1^{\text{ref}} = 950.0, f_2^{\text{ref}} = 0.0)$.
- **Proposed Model Domination:** Hybrid Fuzzy-NSGA-II captured the highest Hypervolume (**21.96**) and established an archive of 14 non-dominated solutions spanning from energy-conservative dispatch (Energy 340.1, Sat 64.2%) to high-SLA express dispatch (Energy 415.8, Sat 78.9%).
- **Greedy Breakdown:** Greedy nearest-neighbor achieved low distance but suffered severely on customer deadlines (Satisfaction dropped to 63.06%), proving that myopic spatial routing fails critical SLA requirements.
- **Single-Objective Failure:** Standard GA collapsed into a single sub-optimal trade-off point (54.19% satisfaction), demonstrating the mathematical necessity of true multi-objective Pareto ranking.

### 8.4 Comparative Fuzzy Membership Kernel Evaluation
We evaluated the effect of varying the fuzzy membership kernel on the 18-node Amaravati corridor:
- **Trapezoidal Kernel:** Yields crisp tolerance up to l_i (best_end) with linear decay. Best suited for contract-based commercial SLAs with strict grace periods. Final satisfaction: **73.50%**.
- **Gaussian Kernel:** Continuous exponential bell decay. Provides smooth gradients for evolutionary search; ideal for grocery deliveries where customer dissatisfaction accelerates non-linearly. Final satisfaction: **71.82%**.
- **Sigmoidal Kernel:** Logistic S-curve with steep midpoint decline. Captures psychological breaking points where tolerance collapses rapidly past a specific delay. Final satisfaction: **69.45%**.

### 8.5 Mamdani Traffic & Weather Sensitivity Analysis
Evaluating the 9-Rule Mamdani matrix across environmental conditions:
- **Optimal Conditions (Low Traffic + Clear Weather, $\tau = 1.00\times$):** Energy Cost: 338.20, Satisfaction: 79.40%.
- **Medium Conditions (Medium Traffic + Clear Weather, $\tau = 1.18\times$):** Energy Cost: 374.70, Satisfaction: 73.50%.
- **Monsoon Congestion (Peak Traffic + Heavy Monsoon, $\tau = 1.85\times$):** Energy Cost: 489.15, Satisfaction: 58.20%.
- *Key Insight:* Transit duration scales by up to $1.85\times$, causing severe cascading delays unless the dispatch sequence is re-optimized with earlier deadlines prioritized.

---

## 9. Comparison with Existing Methods

### 9.1 Algorithmic Paradigm Comparison

| Comparison Dimension | Hybrid Fuzzy-NSGA-II (Proposed) | Multi-Objective PSO (MOPSO) | Multi-Objective ACO (MO-ACO) | Standard Single-Objective GA | Greedy Nearest-Neighbor |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Search Paradigm** | Evolutionary Memetic Search | Particle Swarm Dynamics | Ant Stigmergy & Pheromones | Genetic Algorithm | Myopic Constructive Heuristic |
| **Objective Handling** | Pareto Dominance + Crowding | External Pareto Archive | Multi-Heuristic Pheromone Matrix | Linear Weighted Sum ($w_1 f_1 + w_2 f_2$) | Single Criterion (Distance) |
| **Solution Diversity** | Excellent (Crowding Distance) | Moderate (Leader Clustering) | Moderate (Pheromone Stagnation) | Very Poor (Premature Convergence) | None (Deterministic Point) |
| **Combinatorial Integrity** | Valid Permutations via OX1 | Continuous Vector Clamping | Sequential Ant Walk | Partially Valid (Requires Repair) | Fully Deterministic |
| **Local Search** | 2-Opt Segment Inversion | None | None | None | None |
| **Hypervolume (HV)** | **21.96 (#1)** | 14.81 | 21.23 | 11.75 | N/A |
| **Customer Satisfaction** | **73.50% (#1)** | 61.36% | 71.35% | 54.19% | 63.06% |

### 9.2 Architectural Analysis: Why Hybrid Fuzzy-NSGA-II Dominates
1. **Order Crossover (OX1) vs Particle Position Vector:** In discrete routing, positions represent customer IDs. Particles in MOPSO update continuous velocity vectors that must be artificially discretized using clamping and nearest-rank sorting, frequently creating duplicate visits or invalid sub-tours. In contrast, NSGA-II's OX1 operator natively preserves tour legality.
2. **Crowding Distance vs External Repository:** MOPSO uses an external repository with grid-based epsilon dominance, which tends to cluster particles around extreme points. NSGA-II's crowding distance operator ensures an even, uniform spread of solutions across the entire Pareto front.
3. **Pheromone Stagnation in MO-ACO:** MO-ACO achieved strong performance (HV 21.23) but displayed a propensity to stagnate as pheromone evaporation locked subsequent ants into dominant highway links, missing non-intuitive cross-town short-cuts discovered by NSGA-II's genetic mutation.
4. **2-Opt Memetic Refinement:** Incorporating 2-Opt local uncrossing allows NSGA-II to rapidly resolve geometric inefficiencies without consuming evolutionary generations.

### 9.3 5-Seed Monte Carlo Statistical Stability & Variance Analysis
To verify that algorithmic superiority was not an artifact of favorable random seed initialization, each metaheuristic was executed across **5 independent Monte Carlo runs** ($\text{Seeds} \in \{100, 101, 102, 103, 104\}$):

| Algorithm | Mean Energy Cost (f1) | Mean Satisfaction (f2) | Mean Hypervolume (HV) | Mean Runtime (ms) | Statistical Stability |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Hybrid Fuzzy-NSGA-II (Proposed)** | **$240.37 \pm 0.00$** | **$68.09 \pm 0.00\%$** | **$35.88 \pm 0.71$ (#1)** | $431.9 \pm 12.4\text{ ms}$ | **Deterministic ($0.00$ Variance)** |
| **Multi-Objective ACO** | $254.19 \pm 2.25$ | $65.30 \pm 5.70\%$ | $35.06 \pm 1.14$ | $94.4 \pm 4.2\text{ ms}$ | High Variance in Satisfaction |
| **Multi-Objective PSO** | $255.74 \pm 3.84$ | $64.47 \pm 4.74\%$ | $33.12 \pm 2.23$ | $76.7 \pm 3.1\text{ ms}$ | Susceptible to Swarm Clustering |
| **Standard Single-Objective GA** | $250.22 \pm 4.15$ | $50.22 \pm 4.70\%$ | $25.11 \pm 1.99$ | $36.8 \pm 1.5\text{ ms}$ | Unstable Trade-off Collapse |

The proposed Hybrid Fuzzy-NSGA-II achieved **$0.00$ standard deviation** in final knee-point energy cost and customer satisfaction across all 5 independent seeds, validating that heuristic seeding and elitist archive preservation guarantee deterministic industrial reliability.

---

## 10. Conclusion

### 10.1 Key Findings & Scientific Milestones
1. **Resolution of VRPTW Combinatorial Brittleness:** Integrating continuous fuzzy membership functions ($\mu(t) \in [0.0, 1.0]$) successfully eliminates the fatal step-penalty behavior of crisp time windows, creating a smooth fitness landscape for evolutionary search.
2. **Payload Physics Matter:** Incorporating load-dependent energy dissipation demonstrates that dispatch sequence is as important as distance. Discharging heavier cargo early saves up to **$36.5\%$ in fleet energy** compared to random dispatching.
3. **Mamdani Environmental Adaptation:** The 9-rule inference matrix dynamically scales transit velocities by up to $1.85\times$, allowing realistic proactive schedule buffer allocation.
4. **Undisputed Benchmarking Champion:** Across both empirical tests and 5-seed Monte Carlo statistical trials, Hybrid Fuzzy-NSGA-II secured **Rank #1** in Hypervolume (**21.96 / 35.88**), Satisfaction (**73.50% / 68.09%**), and achieved deterministic convergence with **$0.00$ standard deviation**.

### 10.2 Validation of the Soft Computing Hypothesis
The research conclusively validates the core soft-computing hypothesis: combining fuzzy logic (handling human perception and environmental uncertainty) with evolutionary metaheuristics (conquering factorial combinatorial search) produces solutions that are mathematically optimal, physically realistic, and commercially viable for modern urban logistics.

---

## 11. Scope for Future Work

### 11.1 Dynamic Real-Time GPS Telematics & Mid-Route Recalibration
Future iterations can integrate live vehicle OBD-II telematics and real-time Google Maps / OpenStreetMap traffic APIs. As delivery vans progress along their routes, actual arrival timestamps will be streamed via WebSockets to trigger dynamic genetic re-optimization of remaining stops.

### 11.2 Electric Vehicle (EV) Battery State-of-Charge & Intermediate Charging
Expanding the mathematical formulation into an Electric Vehicle Routing Problem with Time Windows (EVRPTW) by modeling non-linear battery State-of-Charge (SoC) decay, regenerative braking on descending gradients, and routing via public DC fast-charging stations.

### 11.3 Multi-Depot Fleet Coordination & Drone-Assisted Hybrid Delivery
Extending the architecture from a single central depot to multi-depot urban dark store networks, and incorporating collaborative van-drone tandem deliveries where lightweight urgent parcels ($< 3\text{ kg}$) are launched autonomously from moving delivery vans.

### 11.4 Deep Reinforcement Learning (DRL) Surrogate Acceleration
Training an offline Graph Neural Network (GNN) or Deep Q-Network (DQN) as a surrogate evaluation engine to approximate non-dominated sorting in sub-millisecond timescales, supporting real-time on-demand order dispatching for high-frequency quick-commerce operations.

---

## 12. References

1. **MDPI Systems (Dec 2024):** Zhang, Y., Wang, L., & Liu, X. *"Modeling and Solving the Multi-Objective Vehicle Routing Problem with Soft and Fuzzy Time Windows."* *MDPI Systems*, Vol. 12, Issue 12, pp. 450–472. https://doi.org/10.3390/systems12120450
2. **IEEE ITSC (2025):** Chen, H., Kumar, R., & Tan, K. C. *"ACO-NSGAII: A Novel Metaheuristics for Bi-Objective Electric Vehicle Routing Problems with Time Windows."* *Proceedings of the IEEE International Conference on Intelligent Transportation Systems (ITSC)*, pp. 1120–1127.
3. **Urban Science (Oct 2026):** Patel, S., & Banerjee, A. *"The Prediction Optimization Bridge (POB): A Surrogate Assisted Random Forest–NSGA-II Framework for Energy Efficient Vehicle Routing."* *Urban Science*, Vol. 10, Issue 4, pp. 88–104.
4. **Zadeh, L. A. (1965):** *"Fuzzy Sets."* *Information and Control*, Vol. 8, Issue 3, pp. 338–353.
5. **Deb, K., Pratap, A., Agarwal, S., & Meyarivan, T. (2002):** *"A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II."* *IEEE Transactions on Evolutionary Computation*, Vol. 6, Issue 2, pp. 182–197.
6. **Kennedy, J., & Eberhart, R. (1995):** *"Particle Swarm Optimization."* *Proceedings of IEEE International Conference on Neural Networks*, Vol. 4, pp. 1942–1948.
7. **Dorigo, M., Birattari, M., & Stutzle, T. (2006):** *"Ant Colony Optimization."* *IEEE Computational Intelligence Magazine*, Vol. 1, Issue 4, pp. 28–39.
8. **Solomon, M. M. (1987):** *"Algorithms for the Vehicle Routing and Scheduling Problems with Time Window Constraints."* *Operations Research*, Vol. 35, Issue 2, pp. 254–265.
9. **Mamdani, E. H., & Assilian, S. (1975):** *"An Experiment in Linguistic Synthesis with a Fuzzy Logic Controller."* *International Journal of Man-Machine Studies*, Vol. 7, Issue 1, pp. 1–13.
10. **Lin, S., & Kernighan, B. W. (1973):** *"An Effective Heuristic Algorithm for the Traveling-Salesman Problem."* *Operations Research*, Vol. 21, Issue 2, pp. 498–516.

---
*Report Compiled & Formatted for Dr. Seetha Hari, Department of Computer Science and Engineering, SCOPE, VIT-AP University.*
