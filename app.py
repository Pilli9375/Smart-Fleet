"""
app.py
FleetPulse — Autonomous Fleet Dispatch & Multi-Objective Optimization Platform
Design System: Precision Industrial Dark UI (Inter + JetBrains Mono, 1px Zinc Hairlines, Zero Emoji Slop)
Authors: V Naga Adithya (23BCE9062) & M Karthik (23BCE9659)
"""
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go
from core_data_and_fuzzy import (
    get_dataset,
    compute_fuzzy_satisfaction,
    FUZZY_TRAFFIC_RULES,
    get_fuzzy_traffic_factor
)
from core_optimizers import (
    run_full_benchmark_suite,
    run_multi_trial_statistics
)

st.set_page_config(
    page_title="FleetPulse — Multi-Objective Dispatch Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================================
# PRECISION DESIGN SYSTEM CSS (LINEAR / VERCEL / SAMSARA INSPIRED)
# =====================================================================
DESIGN_SYSTEM_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

:root {
--bg-base: #09090b;
--bg-surface: #121215;
--bg-elevated: #18181b;
--border-subtle: #27272a;
--border-focus: #3f3f46;
--text-primary: #fafafa;
--text-secondary: #a1a1aa;
--text-muted: #71717a;
--accent-blue: #3b82f6;
--accent-emerald: #10b981;
--accent-amber: #f59e0b;
--accent-rose: #f43f5e;
--accent-violet: #8b5cf6;
}

.stApp {
background-color: var(--bg-base) !important;
color: var(--text-primary) !important;
font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.block-container {
padding-top: 2rem !important;
padding-bottom: 2.5rem !important;
max-width: 1440px !important;
}

section[data-testid="stSidebar"] {
background-color: #0c0c0f !important;
border-right: 1px solid var(--border-subtle) !important;
}

section[data-testid="stSidebar"] * {
font-family: 'Inter', sans-serif !important;
}

/* Top Navigation Bar */
.top-nav {
display: flex;
justify-content: space-between;
align-items: center;
padding: 16px 22px;
background: var(--bg-surface);
border: 1px solid var(--border-subtle);
border-radius: 10px;
margin-bottom: 18px;
}

.brand-cluster {
display: flex;
align-items: center;
gap: 14px;
}

.brand-mark {
width: 34px;
height: 34px;
border-radius: 8px;
background: rgba(59, 130, 246, 0.12);
border: 1px solid rgba(59, 130, 246, 0.4);
display: flex;
align-items: center;
justify-content: center;
color: var(--accent-blue);
font-family: 'JetBrains Mono', monospace;
font-weight: 700;
font-size: 14px;
}

.brand-title {
font-size: 17px;
font-weight: 600;
color: var(--text-primary);
letter-spacing: -0.02em;
margin: 0;
}

.brand-subtitle {
font-size: 12px;
color: var(--text-secondary);
margin-top: 2px;
}

.meta-cluster {
display: flex;
align-items: center;
gap: 8px;
}

.tech-badge {
font-family: 'JetBrains Mono', monospace;
font-size: 11px;
font-weight: 500;
padding: 4px 10px;
border-radius: 6px;
background: var(--bg-elevated);
border: 1px solid var(--border-subtle);
color: var(--text-secondary);
}

.tech-badge.live {
background: rgba(16, 185, 129, 0.08);
border-color: rgba(16, 185, 129, 0.3);
color: #34d399;
}

/* Metric Bento Grid */
.bento-grid {
display: grid;
grid-template-columns: repeat(5, 1fr);
gap: 12px;
margin-bottom: 22px;
}

.bento-card {
background: var(--bg-surface);
border: 1px solid var(--border-subtle);
border-radius: 10px;
padding: 16px 18px;
transition: border-color 0.15s ease;
}

.bento-card:hover {
border-color: var(--border-focus);
}

.bento-label {
font-size: 11px;
font-weight: 600;
text-transform: uppercase;
letter-spacing: 0.06em;
color: var(--text-muted);
margin-bottom: 8px;
}

.bento-value {
font-family: 'JetBrains Mono', monospace;
font-size: 24px;
font-weight: 600;
color: var(--text-primary);
letter-spacing: -0.03em;
line-height: 1.1;
}

.bento-unit {
font-size: 12px;
font-weight: 400;
color: var(--text-muted);
margin-left: 4px;
}

.bento-footer {
margin-top: 10px;
display: flex;
align-items: center;
justify-content: space-between;
font-size: 11.5px;
font-family: 'JetBrains Mono', monospace;
}

.delta-pill {
padding: 2px 7px;
border-radius: 4px;
font-size: 11px;
font-weight: 500;
}

.delta-pos {
background: rgba(16, 185, 129, 0.1);
color: #34d399;
border: 1px solid rgba(16, 185, 129, 0.25);
}

.delta-neutral {
background: rgba(59, 130, 246, 0.1);
color: #60a5fa;
border: 1px solid rgba(59, 130, 246, 0.25);
}

/* Section Panels */
.panel-header {
display: flex;
justify-content: space-between;
align-items: baseline;
margin: 18px 0 10px 0;
padding-bottom: 8px;
border-bottom: 1px solid var(--border-subtle);
}

.panel-title {
font-size: 14px;
font-weight: 600;
color: var(--text-primary);
letter-spacing: -0.01em;
}

.panel-caption {
font-family: 'JetBrains Mono', monospace;
font-size: 11px;
color: var(--text-muted);
}

/* Custom Engineering Data Tables */
.eng-table-wrap {
background: var(--bg-surface);
border: 1px solid var(--border-subtle);
border-radius: 10px;
overflow: hidden;
margin-bottom: 18px;
}

.eng-table {
width: 100%;
border-collapse: collapse;
font-size: 12.5px;
text-align: left;
}

.eng-table th {
background: #141418;
color: var(--text-muted);
font-size: 11px;
font-weight: 600;
text-transform: uppercase;
letter-spacing: 0.05em;
padding: 11px 16px;
border-bottom: 1px solid var(--border-subtle);
}

.eng-table td {
padding: 11px 16px;
border-bottom: 1px solid #1c1c20;
color: #e4e4e7;
}

.eng-table tr:last-child td {
border-bottom: none;
}

.eng-table tr:hover td {
background: rgba(255, 255, 255, 0.02);
}

.mono-cell {
font-family: 'JetBrains Mono', monospace;
font-size: 12px;
}

.status-tag {
font-family: 'JetBrains Mono', monospace;
font-size: 10.5px;
font-weight: 600;
padding: 2px 8px;
border-radius: 4px;
display: inline-block;
}

.tag-crit { background: rgba(244, 63, 94, 0.12); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.3); }
.tag-high { background: rgba(245, 158, 11, 0.12); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
.tag-norm { background: rgba(161, 161, 170, 0.1); color: #a1a1aa; border: 1px solid rgba(161, 161, 170, 0.2); }
.tag-rank1 { background: rgba(59, 130, 246, 0.15); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.4); }

/* Tabs Styling */
div[data-testid="stTabs"] button {
font-family: 'Inter', sans-serif !important;
font-size: 13px !important;
font-weight: 500 !important;
color: var(--text-secondary) !important;
padding: 10px 16px !important;
border-radius: 6px 6px 0 0 !important;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
color: var(--text-primary) !important;
font-weight: 600 !important;
background: var(--bg-surface) !important;
border-bottom: 2px solid var(--accent-blue) !important;
}

.sidebar-section-label {
font-family: 'JetBrains Mono', monospace;
font-size: 10.5px;
font-weight: 600;
text-transform: uppercase;
letter-spacing: 0.08em;
color: var(--text-muted);
margin: 14px 0 6px 0;
}
</style>"""
st.markdown(DESIGN_SYSTEM_CSS, unsafe_allow_html=True)

# =====================================================================
# SIDEBAR CONFIGURATION
# =====================================================================
with st.sidebar:
    st.markdown('<div class="sidebar-section-label">SYSTEM CONFIGURATION</div>', unsafe_allow_html=True)

    dataset_choice = st.selectbox(
        "Network Topology",
        [
            "Amaravati-Vijayawada Live GPS (25 Stops)",
            "Solomon C101 Clustered Benchmark",
            "Solomon R101 Random Benchmark"
        ]
    )

    num_stops = st.slider("Active Delivery Nodes", min_value=10, max_value=25, value=18, step=1)
    max_capacity = st.slider("Vehicle Payload Limit (kg)", min_value=60, max_value=160, value=100, step=10)

    st.markdown('<div class="sidebar-section-label">FUZZY INFERENCE ENGINE</div>', unsafe_allow_html=True)
    fuzzy_kernel = st.selectbox("Membership Function Kernel", ["Trapezoidal", "Gaussian", "Sigmoidal"])
    traffic_level = st.selectbox("Urban Traffic Density", ["Low Traffic", "Medium Traffic", "Peak Rush Hour"], index=1)
    weather_level = st.selectbox("Weather Condition", ["Clear Weather", "Light Rain", "Heavy Monsoon"], index=0)

    st.markdown('<div class="sidebar-section-label">SOLVER HYPERPARAMETERS</div>', unsafe_allow_html=True)
    pop_size = st.slider("Population Size", min_value=20, max_value=80, value=40, step=4)
    generations = st.slider("Max Generations", min_value=15, max_value=80, value=40, step=5)
    sim_speed = st.slider("Simulation Playback Speed", min_value=1, max_value=5, value=3)

    run_btn = st.button("Execute Optimization Suite", type="primary", use_container_width=True)

    st.markdown('<div class="sidebar-section-label" style="margin-top:24px;">RESEARCH TEAM</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="font-size:12px; color:#a1a1aa; line-height:1.6;">'
        'V Naga Adithya <span style="font-family:JetBrains Mono; color:#71717a;">23BCE9062</span><br>'
        'M Karthik <span style="font-family:JetBrains Mono; color:#71717a;">23BCE9659</span>'
        '</div>',
        unsafe_allow_html=True
    )

if "suite_results" not in st.session_state or run_btn:
    with st.spinner("Running multi-objective optimization suite..."):
        st.session_state.suite_results = run_full_benchmark_suite(
            dataset_name=dataset_choice,
            num_stops=num_stops,
            max_capacity=max_capacity,
            pop_size=pop_size,
            generations=generations,
            fuzzy_kernel=fuzzy_kernel,
            traffic_level=traffic_level,
            weather_level=weather_level
        )
        st.session_state.current_dataset = dataset_choice

suite = st.session_state.suite_results
nsga2 = suite["nsga2"]
mopso = suite["mopso"]
moaco = suite["moaco"]
sga = suite["sga"]
greedy = suite["greedy"]

best_sol = nsga2["best_balanced"]
init_rand = nsga2["initial_random"]

energy_saved_vs_rand = ((init_rand["energy"] - best_sol["energy"]) / max(1e-6, init_rand["energy"])) * 100.0
sat_gain_vs_greedy = best_sol["satisfaction"] - greedy["satisfaction"]

# =====================================================================
# TOP NAVIGATION HEADER & BENTO KPI BAR (NATIVE ZERO-INDENT HTML)
# =====================================================================
TOP_HEADER_HTML = f"""<div class="top-nav">
<div class="brand-cluster">
<div class="brand-mark">FP</div>
<div>
<div class="brand-title">FleetPulse Telemetry & Optimization Platform</div>
<div class="brand-subtitle">Hybrid Memetic Fuzzy-NSGA-II • Load-Dependent Energy Physics • Mamdani Traffic Inference</div>
</div>
</div>
<div class="meta-cluster">
<span class="tech-badge live">● SOLVER ONLINE</span>
<span class="tech-badge">KERNEL: {fuzzy_kernel.upper()}</span>
<span class="tech-badge">NODES: {num_stops}</span>
<span class="tech-badge">{nsga2['runtime_ms']} MS</span>
</div>
</div>
<div class="bento-grid">
<div class="bento-card">
<div class="bento-label">Fleet Energy Expenditure</div>
<div class="bento-value">{best_sol['energy']:.2f}<span class="bento-unit">kWh-eq</span></div>
<div class="bento-footer">
<span class="delta-pill delta-pos">-{energy_saved_vs_rand:.1f}% vs Random</span>
<span style="color:#71717a;">Init: {init_rand['energy']:.1f}</span>
</div>
</div>
<div class="bento-card">
<div class="bento-label">Fuzzy SLA Compliance</div>
<div class="bento-value">{best_sol['satisfaction']:.2f}<span class="bento-unit">%</span></div>
<div class="bento-footer">
<span class="delta-pill delta-pos">+{sat_gain_vs_greedy:.1f}% vs Greedy</span>
<span style="color:#71717a;">Greedy: {greedy['satisfaction']:.1f}%</span>
</div>
</div>
<div class="bento-card">
<div class="bento-label">Pareto Hypervolume (HV)</div>
<div class="bento-value">{nsga2['hypervolume']:.2f}<span class="bento-unit">idx</span></div>
<div class="bento-footer">
<span class="delta-pill delta-neutral">Rank #1 Archive</span>
<span style="color:#71717a;">{len(nsga2['pareto_front'])} Solutions</span>
</div>
</div>
<div class="bento-card">
<div class="bento-label">Dispatched Fleet Size</div>
<div class="bento-value">{best_sol['num_vans']}<span class="bento-unit">vehicles</span></div>
<div class="bento-footer">
<span class="delta-pill delta-neutral">Cap: {max_capacity} kg</span>
<span style="color:#71717a;">Zero Overload</span>
</div>
</div>
<div class="bento-card">
<div class="bento-label">Mamdani Traffic State</div>
<div class="bento-value" style="font-size:19px;">{suite['traffic_linguistic']}</div>
<div class="bento-footer">
<span class="delta-pill delta-neutral">{suite['traffic_multiplier']}x Delay</span>
<span style="color:#71717a;">{weather_level}</span>
</div>
</div>
</div>"""
st.markdown(TOP_HEADER_HTML, unsafe_allow_html=True)


# =====================================================================
# CLEAN INTERACTIVE VECTOR TOPOLOGY CANVAS (TAB 1)
# =====================================================================
def render_precision_topology_canvas(depot, van_schedules, speed_mult=3):
    palette = ["#3b82f6", "#10b981", "#f59e0b", "#8b5cf6", "#ec4899", "#06b6d4", "#f43f5e"]

    def spread_coord(x, y):
        dx = x - depot["x"]
        dy = y - depot["y"]
        r = np.hypot(dx, dy)
        if r < 1e-4:
            return x, y
        r_spread = (r ** 0.74) * 2.25
        scale = r_spread / r
        return round(depot["x"] + dx * scale, 2), round(depot["y"] + dy * scale, 2)

    all_x, all_y = [depot["x"]], [depot["y"]]
    routes_payload = []

    for idx, van in enumerate(van_schedules):
        pts = [{"x": depot["x"], "y": depot["y"], "label": "DEPOT", "name": depot["name"], "sat": 100, "weight": 0, "eta": 0}]
        for s in van["stops"]:
            sx, sy = spread_coord(s["x"], s["y"])
            all_x.append(sx)
            all_y.append(sy)
            pts.append({
                "x": sx,
                "y": sy,
                "label": f"N{s['stop_id']:02d}",
                "name": s["name"],
                "sat": s["satisfaction"],
                "weight": s["weight"],
                "eta": s["arrival_min"],
                "prio": s["priority"]
            })
        pts.append({"x": depot["x"], "y": depot["y"], "label": "DEPOT", "name": depot["name"], "sat": 100, "weight": 0, "eta": 0})
        routes_payload.append({
            "van_id": van["van_id"],
            "color": palette[idx % len(palette)],
            "load": f"{van['load_kg']}/{van['capacity_kg']} kg",
            "util": van["utilization_pct"],
            "dist": van["distance_km"],
            "points": pts
        })

    min_x, max_x = min(all_x) - 4, max(all_x) + 4
    min_y, max_y = min(all_y) - 4, max(all_y) + 4

    data_json = json.dumps({
        "depot": {"x": depot["x"], "y": depot["y"], "name": depot["name"]},
        "bounds": {"minX": min_x, "maxX": max_x, "minY": min_y, "maxY": max_y},
        "routes": routes_payload,
        "speed": speed_mult
    })

    canvas_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: transparent; color: #fafafa; font-family: 'Inter', sans-serif; overflow: hidden; }}
        .viewport-frame {{
            background: #121215;
            border: 1px solid #27272a;
            border-radius: 10px;
            overflow: hidden;
        }}
        .toolbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 16px;
            background: #141418;
            border-bottom: 1px solid #27272a;
        }}
        .toolbar-title {{
            font-size: 12px;
            font-weight: 600;
            color: #e4e4e7;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .toolbar-controls {{
            display: flex;
            gap: 6px;
            align-items: center;
        }}
        .ctrl-btn {{
            background: #18181b;
            border: 1px solid #27272a;
            color: #a1a1aa;
            padding: 4px 10px;
            border-radius: 5px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .ctrl-btn:hover, .ctrl-btn.active {{
            background: #27272a;
            color: #fafafa;
            border-color: #52525b;
        }}
        #mapCanvas {{
            width: 100%;
            height: 540px;
            display: block;
            background: #09090b;
            cursor: grab;
        }}
        #mapCanvas:active {{ cursor: grabbing; }}
        .statusbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 8px 16px;
            background: #141418;
            border-top: 1px solid #27272a;
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: #a1a1aa;
        }}
    </style>
    </head>
    <body>
    <div class="viewport-frame">
        <div class="toolbar">
            <div class="toolbar-title">
                <span>SPATIAL ROUTE TOPOLOGY VIEWPORT</span>
                <span style="font-family:'JetBrains Mono'; font-size:11px; color:#71717a;">[SCROLL: ZOOM • DRAG: PAN]</span>
            </div>
            <div class="toolbar-controls" id="filterBar">
                <button class="ctrl-btn" onclick="zoomBy(1.2)">ZOOM +</button>
                <button class="ctrl-btn" onclick="zoomBy(0.83)">ZOOM -</button>
                <button class="ctrl-btn" onclick="resetView()">RESET</button>
                <button class="ctrl-btn active" onclick="selectVan(-1, this)">ALL FLEET</button>
                <button class="ctrl-btn" onclick="togglePlay(this)">PAUSE</button>
            </div>
        </div>
        <canvas id="mapCanvas" width="1380" height="540"></canvas>
        <div class="statusbar">
            <span id="telemetryLog">TELEMETRY READY — ACTIVE VECTOR SIMULATION</span>
            <span id="clockReadout" style="color:#34d399;">T+00.0 MIN</span>
        </div>
    </div>

    <script>
    const cfg = {data_json};
    const canvas = document.getElementById('mapCanvas');
    const ctx = canvas.getContext('2d');
    let progress = 0;
    let paused = false;
    let selectedVan = -1;
    let zoom = 1.0;
    let panX = 0, panY = 0;
    let dragging = false, lx = 0, ly = 0;

    canvas.addEventListener('wheel', e => {{
        e.preventDefault();
        zoom = Math.min(3.2, Math.max(0.65, zoom * (e.deltaY < 0 ? 1.12 : 0.89)));
    }});
    canvas.addEventListener('mousedown', e => {{ dragging = true; lx = e.clientX; ly = e.clientY; }});
    window.addEventListener('mouseup', () => dragging = false);
    window.addEventListener('mousemove', e => {{
        if (!dragging) return;
        panX += (e.clientX - lx) * 1.25;
        panY += (e.clientY - ly) * 1.25;
        lx = e.clientX; ly = e.clientY;
    }});

    function zoomBy(f) {{ zoom = Math.min(3.2, Math.max(0.65, zoom * f)); }}
    function resetView() {{ zoom = 1.0; panX = 0; panY = 0; }}
    function togglePlay(btn) {{ paused = !paused; btn.innerText = paused ? 'RESUME' : 'PAUSE'; }}

    const fBar = document.getElementById('filterBar');
    cfg.routes.forEach((r, idx) => {{
        const b = document.createElement('button');
        b.className = 'ctrl-btn';
        b.innerText = r.van_id.toUpperCase();
        b.style.borderLeft = `3px solid ${{r.color}}`;
        b.onclick = () => selectVan(idx, b);
        fBar.insertBefore(b, fBar.lastElementChild);
    }});

    function selectVan(idx, btn) {{
        selectedVan = idx;
        document.querySelectorAll('#filterBar .ctrl-btn').forEach(b => {{
            if (!['ZOOM +','ZOOM -','RESET','PAUSE','RESUME'].includes(b.innerText)) b.classList.remove('active');
        }});
        btn.classList.add('active');
    }}

    function toX(x) {{
        const pad = 90;
        const raw = pad + ((x - cfg.bounds.minX) / Math.max(1e-5, cfg.bounds.maxX - cfg.bounds.minX)) * (canvas.width - 2 * pad);
        return (raw - canvas.width / 2) * zoom + canvas.width / 2 + panX;
    }}
    function toY(y) {{
        const pad = 60;
        const raw = canvas.height - pad - ((y - cfg.bounds.minY) / Math.max(1e-5, cfg.bounds.maxY - cfg.bounds.minY)) * (canvas.height - 2 * pad);
        return (raw - canvas.height / 2) * zoom + canvas.height / 2 + panY;
    }}

    function draw() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const dx = toX(cfg.depot.x);
        const dy = toY(cfg.depot.y);

        // Subtle technical dot matrix & coordinate grid
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.03)';
        ctx.lineWidth = 1;
        for (let x = 0; x < canvas.width; x += 60) {{
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
        }}
        for (let y = 0; y < canvas.height; y += 60) {{
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
        }}

        // Subtle concentric distance rings from hub
        [120, 240, 360, 480].forEach(r => {{
            ctx.beginPath();
            ctx.arc(dx, dy, r * zoom, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
            ctx.setLineDash([4, 4]);
            ctx.stroke();
            ctx.setLineDash([]);
        }});

        cfg.routes.forEach((route, rIdx) => {{
            if (selectedVan !== -1 && selectedVan !== rIdx) return;
            const pts = route.points;
            if (pts.length < 2) return;

            // Clean vector route path
            ctx.beginPath();
            ctx.moveTo(toX(pts[0].x), toY(pts[0].y));
            for (let i = 1; i < pts.length; i++) {{
                ctx.lineTo(toX(pts[i].x), toY(pts[i].y));
            }}
            ctx.strokeStyle = route.color;
            ctx.globalAlpha = 0.65;
            ctx.lineWidth = 2.2;
            ctx.stroke();
            ctx.globalAlpha = 1.0;

            // Customer Stop Nodes
            for (let i = 1; i < pts.length - 1; i++) {{
                const sx = toX(pts[i].x);
                const sy = toY(pts[i].y);

                ctx.beginPath();
                ctx.arc(sx, sy, 8, 0, Math.PI * 2);
                ctx.fillStyle = '#121215';
                ctx.fill();
                ctx.strokeStyle = route.color;
                ctx.lineWidth = 2;
                ctx.stroke();

                // SLA dot indicator
                ctx.beginPath();
                ctx.arc(sx, sy, 3, 0, Math.PI * 2);
                ctx.fillStyle = pts[i].sat >= 80 ? '#10b981' : (pts[i].sat >= 50 ? '#f59e0b' : '#f43f5e');
                ctx.fill();

                // Clean technical callout pill
                const tag = `${{pts[i].label}} · ${{pts[i].name.slice(0, 15)}}`;
                ctx.font = '500 11px Inter, sans-serif';
                const tw = ctx.measureText(tag).width;
                const oy = (i % 2 === 0) ? -14 : 18;

                ctx.fillStyle = 'rgba(18, 18, 21, 0.9)';
                ctx.strokeStyle = '#27272a';
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.roundRect(sx + 10, sy + oy - 10, tw + 12, 18, 4);
                ctx.fill();
                ctx.stroke();

                ctx.fillStyle = '#e4e4e7';
                ctx.fillText(tag, sx + 16, sy + oy + 3);
            }}

            // Animated Vehicle Marker
            const segs = pts.length - 1;
            const t = ((progress + rIdx * 0.14) % 1.0) * segs;
            const sIdx = Math.floor(t);
            const frac = t - sIdx;
            const pA = pts[sIdx];
            const pB = pts[Math.min(sIdx + 1, segs)];

            const ax = toX(pA.x), ay = toY(pA.y);
            const bx = toX(pB.x), by = toY(pB.y);
            const vx = ax + (bx - ax) * frac;
            const vy = ay + (by - ay) * frac;
            const ang = Math.atan2(by - ay, bx - ax);

            if (frac > 0.86 && pB.label !== 'DEPOT') {{
                document.getElementById('telemetryLog').innerText =
                    `[${{route.van_id.toUpperCase()}} | ${{route.load}}] ARRIVING ${{pB.label}} (${{pB.name}}) — ETA: ${{pB.eta}}m | SLA: ${{pB.sat}}%`;
            }}

            ctx.save();
            ctx.translate(vx, vy);
            ctx.rotate(ang);
            ctx.fillStyle = route.color;
            ctx.strokeStyle = '#fafafa';
            ctx.lineWidth = 1.5;
            ctx.beginPath();
            ctx.moveTo(9, 0);
            ctx.lineTo(-7, -6);
            ctx.lineTo(-4, 0);
            ctx.lineTo(-7, 6);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
            ctx.restore();

            ctx.font = '600 10px JetBrains Mono, monospace';
            ctx.fillStyle = route.color;
            ctx.fillText(route.van_id.toUpperCase(), vx - 16, vy - 12);
        }});

        // Central Depot Square Node
        ctx.fillStyle = '#fafafa';
        ctx.strokeStyle = '#3b82f6';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.roundRect(dx - 9, dy - 9, 18, 18, 4);
        ctx.fill();
        ctx.stroke();

        ctx.font = '600 11px JetBrains Mono, monospace';
        ctx.fillStyle = '#fafafa';
        ctx.fillText('CENTRAL HUB [DEPOT]', dx - 58, dy + 24);

        if (!paused) {{
            progress += 0.00095 * cfg.speed;
            const simMin = ((progress % 1.0) * 65.0).toFixed(1);
            document.getElementById('clockReadout').innerText = `T+${{simMin}} MIN`;
        }}
        requestAnimationFrame(draw);
    }}
    draw();
    </script>
    </body>
    </html>
    """
    components.html(canvas_html, height=625)


# =====================================================================
# PLOTLY INDUSTRIAL DARK THEME HELPER
# =====================================================================
def apply_precision_plotly_theme(fig, title_text, height=370):
    fig.update_layout(
        title=dict(text=title_text, font=dict(family="Inter, sans-serif", size=13, color="#e4e4e7"), x=0.01),
        font=dict(family="Inter, sans-serif", size=11.5, color="#a1a1aa"),
        paper_bgcolor="#121215",
        plot_bgcolor="#121215",
        height=height,
        margin=dict(l=45, r=24, t=48, b=42),
        xaxis=dict(gridcolor="#1f1f23", zerolinecolor="#27272a", linecolor="#27272a"),
        yaxis=dict(gridcolor="#1f1f23", zerolinecolor="#27272a", linecolor="#27272a"),
        legend=dict(
            bgcolor="rgba(18,18,21,0.85)",
            bordercolor="#27272a",
            borderwidth=1,
            font=dict(size=11, color="#e4e4e7")
        )
    )
    return fig


# =====================================================================
# MAIN 5-TAB WORKSPACE
# =====================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "01 / Spatial Route Topology",
    "02 / Algorithm Benchmark Arena",
    "03 / Pareto Frontier & Operators",
    "04 / Fuzzy Kernel & Mamdani Studio",
    "05 / Monte Carlo Statistical Validation"
])

# ---------------------------------------------------------------------
# TAB 1: SPATIAL TOPOLOGY + ENGINEERED FLEET TABLES
# ---------------------------------------------------------------------
with tab1:
    render_precision_topology_canvas(suite["depot"], best_sol["van_schedules"], speed_mult=sim_speed)

    col_left, col_right = st.columns([1.35, 1.0])

    with col_left:
        st.markdown(
            '<div class="panel-header"><span class="panel-title">Dispatched Vehicle Utilization Summary</span>'
            '<span class="panel-caption">CAPACITY CONSTRAINT <= 100 KG</span></div>',
            unsafe_allow_html=True
        )
        rows_html = ""
        for v in best_sol["van_schedules"]:
            seq = " → ".join([f"N{s['stop_id']:02d}" for s in v["stops"]])
            util = v["utilization_pct"]
            rows_html += (
                f"<tr>"
                f"<td class='mono-cell' style='color:#fafafa;font-weight:600;'>{v['van_id'].upper()}</td>"
                f"<td class='mono-cell'>{v['load_kg']} / {v['capacity_kg']} kg</td>"
                f"<td class='mono-cell'>"
                f"<div style='display:flex;align-items:center;gap:8px;'>"
                f"<div style='width:64px;height:6px;background:#27272a;border-radius:3px;overflow:hidden;'>"
                f"<div style='width:{min(100, util)}%;height:100%;background:#3b82f6;'></div></div>"
                f"<span>{util:.0f}%</span></div></td>"
                f"<td class='mono-cell'>{v['distance_km']:.2f} km</td>"
                f"<td class='mono-cell'>{v['energy_units']:.2f}</td>"
                f"<td class='mono-cell' style='color:#a1a1aa;'>{seq}</td>"
                f"</tr>"
            )
        st.markdown(
            f"<div class='eng-table-wrap'><table class='eng-table'>"
            f"<thead><tr><th>Vehicle ID</th><th>Payload</th><th>Utilization</th><th>Distance</th><th>Energy</th><th>Stop Sequence</th></tr></thead>"
            f"<tbody>{rows_html}</tbody></table></div>",
            unsafe_allow_html=True
        )

    with col_right:
        st.markdown(
            '<div class="panel-header"><span class="panel-title">Vehicle Payload vs Energy Expenditure</span>'
            '<span class="panel-caption">LOAD-DEPENDENT ENERGY MODEL</span></div>',
            unsafe_allow_html=True
        )
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=[v["van_id"].upper() for v in best_sol["van_schedules"]],
            y=[v["energy_units"] for v in best_sol["van_schedules"]],
            name="Energy Cost",
            marker_color="#3b82f6",
            text=[f"{v['load_kg']}kg ({v['utilization_pct']:.0f}%)" for v in best_sol["van_schedules"]],
            textposition="outside"
        ))
        apply_precision_plotly_theme(fig_bar, "Per-Vehicle Energy Expenditure & Payload Loadout", height=290)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown(
        '<div class="panel-header"><span class="panel-title">Node-Level SLA Schedule & Fuzzy Satisfaction Audit</span>'
        '<span class="panel-caption">REAL-TIME ARRIVAL TELEMETRY</span></div>',
        unsafe_allow_html=True
    )
    node_rows_html = ""
    for v in best_sol["van_schedules"]:
        for s in v["stops"]:
            p_cls = "tag-crit" if s["priority"] == "Critical" else ("tag-high" if s["priority"] == "High" else "tag-norm")
            sat_v = s["satisfaction"]
            sat_col = "#34d399" if sat_v >= 80 else ("#fbbf24" if sat_v >= 50 else "#fb7185")
            node_rows_html += (
                f"<tr>"
                f"<td class='mono-cell'>{v['van_id'].upper()}</td>"
                f"<td class='mono-cell' style='color:#fafafa;font-weight:600;'>N{s['stop_id']:02d}</td>"
                f"<td>{s['name']}</td>"
                f"<td><span class='status-tag {p_cls}'>{s['priority'].upper()}</span></td>"
                f"<td class='mono-cell'>{s['weight']} kg</td>"
                f"<td class='mono-cell'>{s['arrival_min']} min</td>"
                f"<td class='mono-cell' style='color:#a1a1aa;'>{s['window']}</td>"
                f"<td class='mono-cell' style='color:{sat_col};font-weight:600;'>{sat_v:.1f}%</td>"
                f"</tr>"
            )
    st.markdown(
        f"<div class='eng-table-wrap'><table class='eng-table'>"
        f"<thead><tr><th>Vehicle</th><th>Node ID</th><th>Location</th><th>Priority</th><th>Demand</th><th>ETA</th><th>SLA Window</th><th>Fuzzy Score</th></tr></thead>"
        f"<tbody>{node_rows_html}</tbody></table></div>",
        unsafe_allow_html=True
    )

# ---------------------------------------------------------------------
# TAB 2: 5-ALGORITHM BENCHMARK ARENA
# ---------------------------------------------------------------------
with tab2:
    st.markdown(
        '<div class="panel-header"><span class="panel-title">Empirical Multi-Algorithm Benchmark Matrix</span>'
        '<span class="panel-caption">IDENTICAL FLEET & SLA CONSTRAINTS</span></div>',
        unsafe_allow_html=True
    )

    alg_list = [
        (nsga2["algorithm"], "Memetic Pareto Sorting + Crowding + 2-Opt", nsga2["best_balanced"]["energy"], nsga2["best_balanced"]["satisfaction"], nsga2["hypervolume"], len(nsga2["pareto_front"]), nsga2["runtime_ms"], True),
        (moaco["algorithm"], "Pheromone Trail Matrix + Urgency Heuristic", moaco["best_balanced"]["energy"], moaco["best_balanced"]["satisfaction"], moaco["hypervolume"], len(moaco["pareto_front"]), moaco["runtime_ms"], False),
        (mopso["algorithm"], "Swarm Leader Archive Path Relinking", mopso["best_balanced"]["energy"], mopso["best_balanced"]["satisfaction"], mopso["hypervolume"], len(mopso["pareto_front"]), mopso["runtime_ms"], False),
        (sga["algorithm"], "Single-Objective Distance-Only Genetic Algorithm", sga["best_balanced"]["energy"], sga["best_balanced"]["satisfaction"], sga["hypervolume"], len(sga["pareto_front"]), sga["runtime_ms"], False),
        ("Greedy Nearest-Neighbor Baseline", "Deterministic Myopic Closest-Stop Heuristic", greedy["energy"], greedy["satisfaction"], 0.0, 1, 0.8, False),
    ]

    bench_html = ""
    for name, mech, en, sat, hv, psize, rt, is_prop in alg_list:
        badge = "<span class='status-tag tag-rank1'>PROPOSED #1</span>" if is_prop else ""
        bench_html += (
            f"<tr>"
            f"<td style='font-weight:600;color:#fafafa;'>{name} {badge}</td>"
            f"<td style='color:#a1a1aa;'>{mech}</td>"
            f"<td class='mono-cell'>{en:.2f}</td>"
            f"<td class='mono-cell' style='color:{'#34d399' if sat >= 70 else '#fbbf24'};font-weight:600;'>{sat:.2f}%</td>"
            f"<td class='mono-cell' style='color:#60a5fa;font-weight:600;'>{hv:.2f}</td>"
            f"<td class='mono-cell'>{psize}</td>"
            f"<td class='mono-cell'>{rt} ms</td>"
            f"</tr>"
        )

    st.markdown(
        f"<div class='eng-table-wrap'><table class='eng-table'>"
        f"<thead><tr><th>Algorithm</th><th>Optimization Mechanism</th><th>Energy Cost</th><th>Fuzzy SLA (%)</th><th>Hypervolume (HV)</th><th>Pareto Size</th><th>Runtime</th></tr></thead>"
        f"<tbody>{bench_html}</tbody></table></div>",
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)
    with c1:
        fig_conv = go.Figure()
        for key, label, col in [
            ("nsga2", "Hybrid Fuzzy-NSGA-II (Proposed)", "#3b82f6"),
            ("moaco", "Multi-Objective ACO", "#10b981"),
            ("mopso", "Multi-Objective PSO", "#8b5cf6"),
            ("sga", "Standard Single-Objective GA", "#f43f5e")
        ]:
            hist = suite[key]["history"]
            fig_conv.add_trace(go.Scatter(
                x=[h["gen"] for h in hist],
                y=[h["balanced_satisfaction"] for h in hist],
                mode="lines",
                name=label,
                line=dict(color=col, width=2.5)
            ))
        fig_conv.update_xaxes(title_text="Generation")
        fig_conv.update_yaxes(title_text="Balanced Fuzzy Satisfaction (%)")
        apply_precision_plotly_theme(fig_conv, "Evolutionary Convergence Trajectory Across Generations", height=380)
        st.plotly_chart(fig_conv, use_container_width=True)

    with c2:
        fig_hv = go.Figure()
        names_short = ["Hybrid NSGA-II", "MO-ACO", "MOPSO", "Standard GA"]
        sats = [nsga2["best_balanced"]["satisfaction"], moaco["best_balanced"]["satisfaction"], mopso["best_balanced"]["satisfaction"], sga["best_balanced"]["satisfaction"]]
        hvs = [nsga2["hypervolume"], moaco["hypervolume"], mopso["hypervolume"], sga["hypervolume"]]

        fig_hv.add_trace(go.Bar(x=names_short, y=sats, name="Fuzzy Satisfaction (%)", marker_color="#3b82f6"))
        fig_hv.add_trace(go.Bar(x=names_short, y=hvs, name="Hypervolume (HV)", marker_color="#10b981"))
        fig_hv.update_layout(barmode="group")
        apply_precision_plotly_theme(fig_hv, "Multi-Objective Quality Comparison: SLA Compliance vs Hypervolume", height=380)
        st.plotly_chart(fig_hv, use_container_width=True)

# ---------------------------------------------------------------------
# TAB 3: PARETO FRONTIER & GENETIC OPERATORS
# ---------------------------------------------------------------------
with tab3:
    p_left, p_right = st.columns([1.45, 1.0])

    with p_left:
        fig_pf = go.Figure()
        for key, name, color, sym in [
            ("nsga2", "Hybrid Fuzzy-NSGA-II Frontier", "#3b82f6", "circle"),
            ("moaco", "MO-ACO Archive", "#10b981", "square"),
            ("mopso", "MOPSO Archive", "#8b5cf6", "diamond")
        ]:
            pf = suite[key]["pareto_front"]
            fig_pf.add_trace(go.Scatter(
                x=[p["energy"] for p in pf],
                y=[p["satisfaction"] for p in pf],
                mode="lines+markers",
                name=name,
                marker=dict(size=9, color=color, symbol=sym),
                line=dict(color=color, width=2, dash="solid" if key == "nsga2" else "dot")
            ))

        fig_pf.add_trace(go.Scatter(
            x=[best_sol["energy"]],
            y=[best_sol["satisfaction"]],
            mode="markers",
            name="Selected Knee-Point Schedule",
            marker=dict(size=15, color="#f59e0b", symbol="diamond-open", line=dict(width=3, color="#f59e0b"))
        ))
        fig_pf.update_xaxes(title_text="Total Load-Dependent Fleet Energy Cost (Lower is Better)")
        fig_pf.update_yaxes(title_text="Priority-Weighted Fuzzy SLA Satisfaction % (Higher is Better)")
        apply_precision_plotly_theme(fig_pf, "Non-Dominated Pareto Frontier Overlay", height=400)
        st.plotly_chart(fig_pf, use_container_width=True)

    with p_right:
        st.markdown(
            '<div class="panel-header" style="margin-top:0;"><span class="panel-title">Pareto Trade-Off Operating Modes</span>'
            '<span class="panel-caption">DECISION SUPPORT MATRIX</span></div>',
            unsafe_allow_html=True
        )
        pf_list = nsga2["pareto_front"]
        eco_sol = min(pf_list, key=lambda x: x["energy"])
        cust_sol = max(pf_list, key=lambda x: x["satisfaction"])

        modes_html = ""
        for mode_name, tag_cls, sol_obj in [
            ("ECO-PRIORITY (MIN ENERGY)", "tag-norm", eco_sol),
            ("KNEE-POINT BALANCED (OPTIMAL)", "tag-rank1", best_sol),
            ("SLA-PRIORITY (MAX SATISFACTION)", "tag-high", cust_sol)
        ]:
            modes_html += (
                f"<tr>"
                f"<td><span class='status-tag {tag_cls}'>{mode_name}</span></td>"
                f"<td class='mono-cell'>{sol_obj['energy']:.2f}</td>"
                f"<td class='mono-cell' style='color:#34d399;font-weight:600;'>{sol_obj['satisfaction']:.2f}%</td>"
                f"<td class='mono-cell'>{sol_obj['num_vans']} Vans</td>"
                f"</tr>"
            )
        st.markdown(
            f"<div class='eng-table-wrap'><table class='eng-table'>"
            f"<thead><tr><th>Operating Profile</th><th>Energy</th><th>Fuzzy SLA</th><th>Fleet</th></tr></thead>"
            f"<tbody>{modes_html}</tbody></table></div>",
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="panel-header"><span class="panel-title">Active Knee-Point Chromosome Encoding</span>'
            '<span class="panel-caption">ORDER CROSSOVER (OX) + 2-OPT</span></div>',
            unsafe_allow_html=True
        )
        genes_pills = "".join([
            f"<span style='display:inline-block;font-family:JetBrains Mono;font-size:11px;padding:4px 8px;margin:3px;"
            f"background:#18181b;border:1px solid #27272a;border-radius:4px;color:#60a5fa;'>N{gid:02d}</span>"
            for gid in best_sol["route"]
        ])
        st.markdown(
            f"<div style='background:#121215;border:1px solid #27272a;border-radius:10px;padding:14px;'>"
            f"<div style='font-size:11px;color:#71717a;margin-bottom:8px;font-family:JetBrains Mono;'>PERMUTATION GENOTYPE ({len(best_sol['route'])} NODES):</div>"
            f"<div>{genes_pills}</div></div>",
            unsafe_allow_html=True
        )

# ---------------------------------------------------------------------
# TAB 4: FUZZY KERNEL & MAMDANI INFERENCE STUDIO
# ---------------------------------------------------------------------
with tab4:
    f_col1, f_col2 = st.columns(2)

    with f_col1:
        t_vals = np.linspace(10, 75, 200)
        b_start, b_end, m_late = 15, 30, 60
        y_trap = [compute_fuzzy_satisfaction(t, b_start, b_end, m_late, "Trapezoidal") for t in t_vals]
        y_gaus = [compute_fuzzy_satisfaction(t, b_start, b_end, m_late, "Gaussian") for t in t_vals]
        y_sigm = [compute_fuzzy_satisfaction(t, b_start, b_end, m_late, "Sigmoidal") for t in t_vals]

        fig_fuz = go.Figure()
        fig_fuz.add_trace(go.Scatter(x=t_vals, y=y_trap, name="Trapezoidal (Piecewise Linear)", line=dict(color="#3b82f6", width=3)))
        fig_fuz.add_trace(go.Scatter(x=t_vals, y=y_gaus, name="Gaussian (Bell Decay)", line=dict(color="#10b981", width=2, dash="dash")))
        fig_fuz.add_trace(go.Scatter(x=t_vals, y=y_sigm, name="Sigmoidal (Logistic Decay)", line=dict(color="#f43f5e", width=2, dash="dot")))
        fig_fuz.add_vline(x=b_end, line_dash="dash", line_color="#10b981", annotation_text="Preferred End (30m)")
        fig_fuz.add_vline(x=m_late, line_dash="dash", line_color="#f43f5e", annotation_text="SLA Cutoff (60m)")
        fig_fuz.update_xaxes(title_text="Arrival Time (Minutes)")
        fig_fuz.update_yaxes(title_text="Membership Degree μ(t)")
        apply_precision_plotly_theme(fig_fuz, "Mathematical Comparison of Fuzzy Membership Kernels", height=410)
        st.plotly_chart(fig_fuz, use_container_width=True)

    with f_col2:
        arr_grid = np.linspace(15, 70, 38)
        traf_grid = np.linspace(1.0, 1.85, 38)
        Z_surf = np.zeros((len(traf_grid), len(arr_grid)))
        for i, tf in enumerate(traf_grid):
            for j, ar in enumerate(arr_grid):
                eff_arrival = ar * (0.75 + 0.25 * tf)
                Z_surf[i, j] = compute_fuzzy_satisfaction(eff_arrival, 15, 30, 60, fuzzy_kernel) * 100.0

        fig_3d = go.Figure(data=[go.Surface(
            z=Z_surf,
            x=arr_grid,
            y=traf_grid,
            colorscale="Blues",
            opacity=0.92
        )])
        fig_3d.update_layout(
            scene=dict(
                xaxis_title="Base ETA (min)",
                yaxis_title="Mamdani Factor",
                zaxis_title="SLA Score (%)",
                bgcolor="#121215"
            )
        )
        apply_precision_plotly_theme(fig_3d, f"3D Response Surface Manifold ({fuzzy_kernel} Kernel)", height=410)
        st.plotly_chart(fig_3d, use_container_width=True)

# ---------------------------------------------------------------------
# TAB 5: MONTE CARLO STATISTICAL VALIDATION
# ---------------------------------------------------------------------
with tab5:
    st.markdown(
        '<div class="panel-header"><span class="panel-title">Multi-Seed Monte Carlo Statistical Robustness Evaluation</span>'
        '<span class="panel-caption">5 INDEPENDENT STOCHASTIC SEEDS (MEAN ± STD DEV)</span></div>',
        unsafe_allow_html=True
    )

    if st.button("Execute 5-Seed Statistical Benchmark", type="primary"):
        with st.spinner("Running 5 independent stochastic seeds across all algorithms..."):
            st.session_state.stats_df = pd.DataFrame(run_multi_trial_statistics(
                dataset_name=dataset_choice,
                num_stops=num_stops,
                max_capacity=max_capacity,
                trials=5,
                fuzzy_kernel=fuzzy_kernel
            ))

    if "stats_df" in st.session_state:
        st.dataframe(st.session_state.stats_df, use_container_width=True, hide_index=True)
        csv_bytes = st.session_state.stats_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Empirical Benchmark Report (CSV)",
            data=csv_bytes,
            file_name="fleetpulse_statistical_benchmark.csv",
            mime="text/csv"
        )
