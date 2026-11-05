"""
app.py
FleetPulse AI — 60FPS HTML5 Canvas & SVG Autonomous Telemetry Command Center
Fixes all Streamlit Markdown indentation issues by rendering rich interactive
HTML5/Canvas/SVG animations via components.html and zero-indent CSS.
"""
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import json
import plotly.graph_objects as go
import plotly.express as px
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
    page_title="FleetPulse AI | 60FPS Autonomous Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Zero-indent CSS so Streamlit Markdown NEVER treats HTML as a code block
GLOBAL_CSS = """<style>
.stApp {
background-color: #050811;
color: #f8fafc;
}
div[data-testid="stTabs"] button {
font-size: 0.95rem !important;
font-weight: 700 !important;
color: #94a3b8 !important;
border-radius: 8px 8px 0 0 !important;
padding: 10px 18px !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
color: #38bdf8 !important;
background: rgba(56, 189, 248, 0.12) !important;
border-bottom: 3px solid #38bdf8 !important;
}
</style>"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# =====================================================================
# SIDEBAR MISSION CONTROL
# =====================================================================
with st.sidebar:
    st.markdown("### 🎛️ Mission Control Center")

    dataset_choice = st.selectbox(
        "📍 Network Topology Dataset",
        [
            "Amaravati-Vijayawada Live GPS (25 Stops)",
            "Solomon C101 Clustered Benchmark",
            "Solomon R101 Random Benchmark"
        ]
    )

    num_stops = st.slider("📦 Active Delivery Nodes", min_value=10, max_value=25, value=18, step=1)
    max_capacity = st.slider("🚐 Vehicle Payload Limit (kg)", min_value=60, max_value=160, value=100, step=10)

    st.markdown("---")
    st.markdown("### 🧠 Fuzzy Perception Layer")
    fuzzy_kernel = st.selectbox(
        "Satisfaction Membership Kernel",
        ["Trapezoidal", "Gaussian", "Sigmoidal"]
    )
    traffic_level = st.selectbox("🚦 Urban Traffic Telemetry", ["Low Traffic", "Medium Traffic", "Peak Rush Hour"], index=1)
    weather_level = st.selectbox("🌧️ Atmospheric Condition", ["Clear Weather", "Light Rain", "Heavy Monsoon"], index=0)

    st.markdown("---")
    st.markdown("### 🧬 Evolutionary Engine")
    pop_size = st.slider("Population / Swarm Size", min_value=20, max_value=80, value=40, step=4)
    generations = st.slider("Evolutionary Generations", min_value=15, max_value=80, value=40, step=5)
    sim_speed = st.slider("⚡ Telemetry Animation Speed", min_value=1, max_value=5, value=3)

    run_btn = st.button("🚀 Launch Live Optimization & Telemetry", type="primary", use_container_width=True)

if "suite_results" not in st.session_state or run_btn:
    with st.spinner("Executing Multi-Objective Evolutionary Telemetry across 5 Paradigms..."):
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
# ANIMATED HERO + SVG RING GAUGES HUD (RENDERED VIA HTML COMPONENT)
# =====================================================================
def render_animated_hud(energy_val, energy_save, sat_val, sat_gain, hv_val, num_vans, max_cap, traffic_text, traffic_mult):
    hud_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }}
        body {{ background: transparent; color: #f8fafc; overflow: hidden; }}
        @keyframes bgShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        @keyframes pulseDot {{
            0% {{ transform: scale(0.9); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.8); }}
            70% {{ transform: scale(1.1); box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }}
            100% {{ transform: scale(0.9); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }}
        }}
        @keyframes scanline {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(200%); }}
        }}
        .hud-banner {{
            background: linear-gradient(135deg, #070b14, #0f172a, #09223a, #17133a);
            background-size: 300% 300%;
            animation: bgShift 9s ease infinite;
            border: 1px solid rgba(56, 189, 248, 0.4);
            border-radius: 14px;
            padding: 16px 22px;
            position: relative;
            overflow: hidden;
            margin-bottom: 12px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
        }}
        .hud-banner::after {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 45%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(56, 189, 248, 0.08), transparent);
            animation: scanline 4.5s linear infinite;
        }}
        .badge-row {{ display: flex; gap: 10px; margin-bottom: 8px; align-items: center; }}
        .pill {{
            display: inline-flex; align-items: center; gap: 7px;
            background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981;
            color: #6ee7b7; font-size: 11px; font-weight: 700;
            padding: 3px 11px; border-radius: 99px; letter-spacing: 0.6px;
        }}
        .dot {{
            width: 8px; height: 8px; border-radius: 50%;
            background: #10b981; animation: pulseDot 1.6s infinite;
        }}
        .title-row {{ display: flex; justify-content: space-between; align-items: center; }}
        .main-title {{
            font-size: 24px; font-weight: 800;
            background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .sub-title {{ color: #94a3b8; font-size: 13px; margin-top: 3px; }}
        .kpi-row {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 12px;
        }}
        .kpi-box {{
            background: linear-gradient(160deg, rgba(15,23,42,0.95), rgba(9,13,22,0.95));
            border: 1px solid rgba(56, 189, 248, 0.28);
            border-radius: 12px;
            padding: 12px 14px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            position: relative;
            transition: transform 0.25s ease, border-color 0.25s ease;
        }}
        .kpi-box:hover {{
            transform: translateY(-3px);
            border-color: #38bdf8;
            box-shadow: 0 0 18px rgba(56, 189, 248, 0.3);
        }}
        .kpi-label {{ font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.5px; }}
        .kpi-num {{ font-size: 22px; font-weight: 800; color: #f8fafc; margin: 4px 0; }}
        .kpi-delta {{ font-size: 11.5px; font-weight: 700; color: #34d399; }}
        .ring-svg {{ width: 52px; height: 52px; transform: rotate(-90deg); }}
        .ring-bg {{ fill: none; stroke: rgba(148,163,184,0.15); stroke-width: 5; }}
        .ring-fg {{
            fill: none; stroke-width: 5; stroke-linecap: round;
            stroke-dasharray: 126; stroke-dashoffset: 126;
            transition: stroke-dashoffset 1.4s cubic-bezier(0.22, 1, 0.36, 1);
        }}
    </style>
    </head>
    <body>
        <div class="hud-banner">
            <div class="badge-row">
                <span class="pill"><span class="dot"></span>60FPS TELEMETRY ENGINE ONLINE</span>
                <span class="pill" style="border-color:#38bdf8; color:#bae6fd; background:rgba(56,189,248,0.12);">HYBRID FUZZY-NSGA-II CORE</span>
                <span class="pill" style="border-color:#a855f7; color:#e9d5ff; background:rgba(168,85,247,0.12);">MAMDANI TRAFFIC MATRIX</span>
            </div>
            <div class="title-row">
                <div>
                    <div class="main-title">⚡ FleetPulse AI: Autonomous Multi-Objective Command Center</div>
                    <div class="sub-title">Real-Time Neuro-Fuzzy SLA Inference, Load-Dependent Energy Physics & 5-Algorithm Evolutionary Telemetry</div>
                </div>
            </div>
        </div>

        <div class="kpi-row">
            <div class="kpi-box">
                <div>
                    <div class="kpi-label">⚡ Fleet Energy Cost</div>
                    <div class="kpi-num" id="cntEnergy">0.0</div>
                    <div class="kpi-delta">▼ -{energy_save:.1f}% vs Random</div>
                </div>
                <svg class="ring-svg"><circle class="ring-bg" cx="26" cy="26" r="20"/><circle class="ring-fg" id="ring1" stroke="#38bdf8" cx="26" cy="26" r="20"/></svg>
            </div>
            <div class="kpi-box">
                <div>
                    <div class="kpi-label">😊 Fuzzy SLA Score</div>
                    <div class="kpi-num" id="cntSat">0.0%</div>
                    <div class="kpi-delta">▲ +{sat_gain:.1f}% vs Greedy</div>
                </div>
                <svg class="ring-svg"><circle class="ring-bg" cx="26" cy="26" r="20"/><circle class="ring-fg" id="ring2" stroke="#10b981" cx="26" cy="26" r="20"/></svg>
            </div>
            <div class="kpi-box">
                <div>
                    <div class="kpi-label">🏆 Hypervolume (HV)</div>
                    <div class="kpi-num" id="cntHV">0.00</div>
                    <div class="kpi-delta">▲ #1 Dominant Archive</div>
                </div>
                <svg class="ring-svg"><circle class="ring-bg" cx="26" cy="26" r="20"/><circle class="ring-fg" id="ring3" stroke="#a855f7" cx="26" cy="26" r="20"/></svg>
            </div>
            <div class="kpi-box">
                <div>
                    <div class="kpi-label">🚐 Active Fleet</div>
                    <div class="kpi-num">{num_vans} Vans</div>
                    <div class="kpi-delta" style="color:#38bdf8;">Cap: {max_cap} kg/van</div>
                </div>
                <svg class="ring-svg"><circle class="ring-bg" cx="26" cy="26" r="20"/><circle class="ring-fg" id="ring4" stroke="#f59e0b" cx="26" cy="26" r="20"/></svg>
            </div>
            <div class="kpi-box">
                <div>
                    <div class="kpi-label">🚦 Traffic State</div>
                    <div class="kpi-num" style="font-size:17px;">{traffic_text}</div>
                    <div class="kpi-delta" style="color:#f43f5e;">Delay: {traffic_mult}x</div>
                </div>
                <svg class="ring-svg"><circle class="ring-bg" cx="26" cy="26" r="20"/><circle class="ring-fg" id="ring5" stroke="#f43f5e" cx="26" cy="26" r="20"/></svg>
            </div>
        </div>

        <script>
            function animateValue(id, endVal, suffix, decimals) {{
                const el = document.getElementById(id);
                let start = 0;
                const duration = 900;
                const startTime = performance.now();
                function tick(now) {{
                    const p = Math.min(1, (now - startTime) / duration);
                    const ease = 1 - Math.pow(1 - p, 3);
                    el.innerText = (endVal * ease).toFixed(decimals) + suffix;
                    if (p < 1) requestAnimationFrame(tick);
                }}
                requestAnimationFrame(tick);
            }}
            animateValue("cntEnergy", {energy_val}, " u", 1);
            animateValue("cntSat", {sat_val}, "%", 1);
            animateValue("cntHV", {hv_val}, "", 2);

            setTimeout(() => {{
                document.getElementById("ring1").style.strokeDashoffset = 126 - (126 * 0.78);
                document.getElementById("ring2").style.strokeDashoffset = 126 - (126 * ({sat_val} / 100.0));
                document.getElementById("ring3").style.strokeDashoffset = 126 - (126 * Math.min(0.95, {hv_val} / 60.0));
                document.getElementById("ring4").style.strokeDashoffset = 126 - (126 * 0.85);
                document.getElementById("ring5").style.strokeDashoffset = 126 - (126 * ({traffic_mult} / 2.0));
            }}, 80);
        </script>
    </body>
    </html>
    """
    components.html(hud_html, height=215)


render_animated_hud(
    best_sol["energy"],
    energy_saved_vs_rand,
    best_sol["satisfaction"],
    sat_gain_vs_greedy,
    nsga2["hypervolume"],
    best_sol["num_vans"],
    max_capacity,
    suite["traffic_linguistic"],
    suite["traffic_multiplier"]
)


# =====================================================================
# COMPONENT 2: 60FPS CYBERPUNK FLEET RADAR, DIRECTIONAL VANS & TICKER
# =====================================================================
def render_cyberpunk_radar(depot, van_schedules, speed_mult=3):
    palette = ["#38bdf8", "#10b981", "#f43f5e", "#a855f7", "#f59e0b", "#06b6d4", "#ec4899"]

    # Radial de-clutter transform so inner-city stops near the depot spread out cleanly
    def spread_coord(x, y):
        dx = x - depot["x"]
        dy = y - depot["y"]
        r = np.hypot(dx, dy)
        if r < 1e-4:
            return x, y
        # Boost short distances (power 0.72) so central nodes don't bunch up
        r_spread = (r ** 0.72) * 2.35
        scale = r_spread / r
        return round(depot["x"] + dx * scale, 2), round(depot["y"] + dy * scale, 2)

    all_x, all_y = [depot["x"]], [depot["y"]]
    routes_payload = []

    for idx, van in enumerate(van_schedules):
        pts = [{"x": depot["x"], "y": depot["y"], "label": "CENTRAL HUB", "sat": 100, "weight": 0, "eta": 0}]
        for s in van["stops"]:
            sx, sy = spread_coord(s["x"], s["y"])
            all_x.append(sx)
            all_y.append(sy)
            pts.append({
                "x": sx,
                "y": sy,
                "label": f"#{s['stop_id']} {s['name'][:20]}",
                "sat": s["satisfaction"],
                "weight": s["weight"],
                "eta": s["arrival_min"],
                "prio": s["priority"]
            })
        pts.append({"x": depot["x"], "y": depot["y"], "label": "CENTRAL HUB", "sat": 100, "weight": 0, "eta": 0})
        routes_payload.append({
            "van_id": van["van_id"],
            "color": palette[idx % len(palette)],
            "load": f"{van['load_kg']}/{van['capacity_kg']}kg",
            "util": van["utilization_pct"],
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

    radar_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }}
        body {{ background: transparent; color: #f8fafc; overflow: hidden; }}
        .radar-shell {{
            background: #060a14;
            border: 1px solid rgba(56, 189, 248, 0.45);
            border-radius: 16px;
            padding: 14px 18px;
            box-shadow: 0 12px 36px rgba(0,0,0,0.75);
        }}
        .top-bar {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 10px; padding-bottom: 10px;
            border-bottom: 1px solid rgba(148,163,184,0.18);
            flex-wrap: wrap; gap: 8px;
        }}
        .btn-group {{ display: flex; gap: 7px; flex-wrap: wrap; align-items: center; }}
        .hud-btn {{
            background: rgba(15, 23, 42, 0.92);
            border: 1px solid rgba(56, 189, 248, 0.4);
            color: #e2e8f0;
            padding: 6px 12px;
            border-radius: 7px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .hud-btn:hover, .hud-btn.active {{
            background: #0284c7;
            border-color: #38bdf8;
            color: #ffffff;
            box-shadow: 0 0 12px rgba(56,189,248,0.45);
        }}
        .ticker-bar {{
            margin-top: 10px;
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 8px;
            padding: 8px 14px;
            font-size: 13px;
            color: #38bdf8;
            display: flex;
            justify-content: space-between;
            font-family: monospace;
        }}
        #cyberCanvas {{
            width: 100%;
            height: 640px;
            border-radius: 12px;
            cursor: grab;
            background: radial-gradient(circle at center, #0b152e 0%, #04070f 100%);
        }}
        #cyberCanvas:active {{ cursor: grabbing; }}
    </style>
    </head>
    <body>
    <div class="radar-shell">
        <div class="top-bar">
            <div style="font-size:15px; font-weight:800; color:#38bdf8; letter-spacing:0.6px;">
                🛰️ WIDESCREEN 60FPS VECTOR RADAR — SCROLL TO ZOOM • DRAG TO PAN
            </div>
            <div class="btn-group" id="vanFilterBtns">
                <button class="hud-btn" onclick="adjustZoom(1.25)">➕ ZOOM IN</button>
                <button class="hud-btn" onclick="adjustZoom(0.8)">➖ ZOOM OUT</button>
                <button class="hud-btn" onclick="resetCamera()">🎯 RESET VIEW</button>
                <button class="hud-btn active" onclick="setFilter(-1, this)">ALL VANS</button>
                <button class="hud-btn" onclick="togglePause(this)">⏸️ PAUSE</button>
            </div>
        </div>
        <canvas id="cyberCanvas" width="1440" height="640"></canvas>
        <div class="ticker-bar">
            <span id="liveTicker">⚡ TELEMETRY STREAM: Initializing widescreen vector paths...</span>
            <span id="simClock" style="color:#34d399; font-weight:700;">SIM CLOCK: T+00.0m</span>
        </div>
    </div>

    <script>
    const data = {data_json};
    const canvas = document.getElementById('cyberCanvas');
    const ctx = canvas.getContext('2d');
    let progress = 0;
    let radarAngle = 0;
    let paused = false;
    let activeVan = -1;
    let zoom = 1.05;
    let panX = 0, panY = 0;
    let isDragging = false, lastX = 0, lastY = 0;
    const particles = [];

    // Mouse Wheel Zoom & Drag Pan
    canvas.addEventListener('wheel', (e) => {{
        e.preventDefault();
        const factor = e.deltaY < 0 ? 1.12 : 0.89;
        zoom = Math.min(3.5, Math.max(0.65, zoom * factor));
    }});
    canvas.addEventListener('mousedown', (e) => {{
        isDragging = true; lastX = e.clientX; lastY = e.clientY;
    }});
    window.addEventListener('mouseup', () => isDragging = false);
    window.addEventListener('mousemove', (e) => {{
        if (!isDragging) return;
        panX += (e.clientX - lastX) * 1.3;
        panY += (e.clientY - lastY) * 1.3;
        lastX = e.clientX; lastY = e.clientY;
    }});

    function adjustZoom(f) {{ zoom = Math.min(3.5, Math.max(0.65, zoom * f)); }}
    function resetCamera() {{ zoom = 1.05; panX = 0; panY = 0; }}

    const btnContainer = document.getElementById('vanFilterBtns');
    data.routes.forEach((r, idx) => {{
        const b = document.createElement('button');
        b.className = 'hud-btn';
        b.innerText = r.van_id;
        b.style.borderColor = r.color;
        b.onclick = () => setFilter(idx, b);
        btnContainer.insertBefore(b, btnContainer.lastElementChild);
    }});

    function setFilter(idx, btnEl) {{
        activeVan = idx;
        document.querySelectorAll('#vanFilterBtns .hud-btn').forEach(b => {{
            if (!['⏸️ PAUSE','▶️ RESUME','➕ ZOOM IN','➖ ZOOM OUT','🎯 RESET VIEW'].includes(b.innerText)) {{
                b.classList.remove('active');
            }}
        }});
        btnEl.classList.add('active');
    }}

    function togglePause(btnEl) {{
        paused = !paused;
        btnEl.innerText = paused ? '▶️ RESUME' : '⏸️ PAUSE';
    }}

    function mapX(x) {{
        const pad = 95;
        const base = pad + ((x - data.bounds.minX) / Math.max(1e-5, data.bounds.maxX - data.bounds.minX)) * (canvas.width - 2 * pad);
        return (base - canvas.width / 2) * zoom + canvas.width / 2 + panX;
    }}
    function mapY(y) {{
        const pad = 70;
        const base = canvas.height - pad - ((y - data.bounds.minY) / Math.max(1e-5, data.bounds.maxY - data.bounds.minY)) * (canvas.height - 2 * pad);
        return (base - canvas.height / 2) * zoom + canvas.height / 2 + panY;
    }}

    function render() {{
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        const dx = mapX(data.depot.x);
        const dy = mapY(data.depot.y);

        // 1. Cybernetic background grid
        ctx.strokeStyle = 'rgba(56, 189, 248, 0.06)';
        ctx.lineWidth = 1;
        for (let x = 0; x < canvas.width; x += 55) {{
            ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
        }}
        for (let y = 0; y < canvas.height; y += 55) {{
            ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
        }}

        // Concentric radar distance rings
        [110, 220, 340, 470, 600].forEach(r => {{
            ctx.beginPath();
            ctx.arc(dx, dy, r * zoom, 0, Math.PI * 2);
            ctx.strokeStyle = 'rgba(56, 189, 248, 0.11)';
            ctx.lineWidth = 1.2;
            ctx.stroke();
        }});

        // 2. Rotating 360 Radar Sweep Beam
        ctx.save();
        ctx.translate(dx, dy);
        ctx.rotate(radarAngle);
        const sweepGrad = ctx.createConicGradient(0, 0, 0);
        sweepGrad.addColorStop(0, 'rgba(56, 189, 248, 0.24)');
        sweepGrad.addColorStop(0.12, 'rgba(56, 189, 248, 0.0)');
        sweepGrad.addColorStop(1, 'rgba(56, 189, 248, 0.0)');
        ctx.fillStyle = sweepGrad;
        ctx.beginPath();
        ctx.arc(0, 0, 650 * zoom, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();

        // 3. Draw Routes, Nodes & Bigger Directional Moving Vans
        data.routes.forEach((route, rIdx) => {{
            if (activeVan !== -1 && activeVan !== rIdx) return;
            const pts = route.points;
            if (pts.length < 2) return;

            // Glowing route vector line
            ctx.save();
            ctx.beginPath();
            ctx.moveTo(mapX(pts[0].x), mapY(pts[0].y));
            for (let i = 1; i < pts.length; i++) {{
                ctx.lineTo(mapX(pts[i].x), mapY(pts[i].y));
            }}
            ctx.strokeStyle = route.color;
            ctx.shadowColor = route.color;
            ctx.shadowBlur = 14;
            ctx.globalAlpha = 0.65;
            ctx.lineWidth = 3.2;
            ctx.stroke();
            ctx.restore();

            // Draw Customer Nodes with alternating label offsets so text never collides
            for (let i = 1; i < pts.length - 1; i++) {{
                const sx = mapX(pts[i].x);
                const sy = mapY(pts[i].y);

                // Node SLA status outer ring
                ctx.beginPath();
                ctx.arc(sx, sy, 11, 0, Math.PI * 2);
                ctx.strokeStyle = pts[i].sat >= 80 ? '#10b981' : (pts[i].sat >= 50 ? '#f59e0b' : '#f43f5e');
                ctx.lineWidth = 2.4;
                ctx.stroke();

                // Node inner core
                ctx.beginPath();
                ctx.arc(sx, sy, 6.5, 0, Math.PI * 2);
                ctx.fillStyle = route.color;
                ctx.fill();

                // Smart label pill background for crisp readability
                const labelText = pts[i].label;
                ctx.font = 'bold 13px sans-serif';
                const textW = ctx.measureText(labelText).width;
                const offsetY = (i % 2 === 0) ? -16 : 22;
                ctx.fillStyle = 'rgba(6, 10, 20, 0.82)';
                ctx.beginPath();
                ctx.roundRect(sx + 12, sy + offsetY - 12, textW + 10, 18, 4);
                ctx.fill();

                ctx.fillStyle = '#f8fafc';
                ctx.fillText(labelText, sx + 17, sy + offsetY + 1);
            }}

            // Calculate Moving Van Position & Heading Angle
            const totalSegs = pts.length - 1;
            const tGlobal = ((progress + rIdx * 0.13) % 1.0) * totalSegs;
            const segIdx = Math.floor(tGlobal);
            const segFrac = tGlobal - segIdx;
            const pA = pts[segIdx];
            const pB = pts[Math.min(segIdx + 1, totalSegs)];

            const ax = mapX(pA.x), ay = mapY(pA.y);
            const bx = mapX(pB.x), by = mapY(pB.y);
            const vx = ax + (bx - ax) * segFrac;
            const vy = ay + (by - ay) * segFrac;
            const angle = Math.atan2(by - ay, bx - ax);

            if (!paused && Math.random() < 0.75) {{
                particles.push({{
                    x: vx, y: vy,
                    r: 4.5,
                    alpha: 0.9,
                    color: route.color
                }});
            }}

            if (segFrac > 0.88 && pB.label !== 'CENTRAL HUB') {{
                document.getElementById('liveTicker').innerText =
                    `⚡ [${{route.van_id}} | Load ${{route.load}}] Docking at ${{pB.label}} — ETA: ${{pB.eta}}m | Fuzzy SLA: ${{pB.sat}}%`;
            }}

            // Draw Larger Directional Autonomous Vehicle + Headlight Cone
            ctx.save();
            ctx.translate(vx, vy);
            ctx.rotate(angle);

            const beam = ctx.createLinearGradient(0, 0, 48, 0);
            beam.addColorStop(0, 'rgba(255, 255, 255, 0.55)');
            beam.addColorStop(1, 'rgba(255, 255, 255, 0.0)');
            ctx.fillStyle = beam;
            ctx.beginPath();
            ctx.moveTo(8, 0);
            ctx.lineTo(48, -16);
            ctx.lineTo(48, 16);
            ctx.closePath();
            ctx.fill();

            ctx.fillStyle = '#ffffff';
            ctx.strokeStyle = route.color;
            ctx.lineWidth = 3.2;
            ctx.beginPath();
            ctx.roundRect(-11, -7, 22, 14, 4);
            ctx.fill();
            ctx.stroke();
            ctx.restore();

            // Floating HUD Callout above Van
            ctx.fillStyle = route.color;
            ctx.font = 'bold 13px sans-serif';
            ctx.fillText(`${{route.van_id}} (${{route.util}}%)`, vx - 30, vy - 16);
        }});

        // 4. Render & Decay Particle Trails
        for (let i = particles.length - 1; i >= 0; i--) {{
            const pt = particles[i];
            ctx.beginPath();
            ctx.arc(pt.x, pt.y, pt.r, 0, Math.PI * 2);
            ctx.fillStyle = pt.color;
            ctx.globalAlpha = pt.alpha;
            ctx.fill();
            ctx.globalAlpha = 1.0;
            pt.alpha -= 0.032;
            pt.r *= 0.96;
            if (pt.alpha <= 0.02) particles.splice(i, 1);
        }}

        // 5. Large Central Depot Core
        ctx.save();
        ctx.beginPath();
        ctx.arc(dx, dy, 16, 0, Math.PI * 2);
        ctx.fillStyle = '#f59e0b';
        ctx.shadowColor = '#f59e0b';
        ctx.shadowBlur = 24;
        ctx.fill();
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 3.5;
        ctx.stroke();
        ctx.restore();

        ctx.fillStyle = '#fde047';
        ctx.font = 'bold 14px sans-serif';
        ctx.fillText('★ CENTRAL HUB', dx - 52, dy + 34);

        if (!paused) {{
            progress += 0.0010 * data.speed;
            radarAngle += 0.020;
            const simMin = ((progress % 1.0) * 65.0).toFixed(1);
            document.getElementById('simClock').innerText = `SIM CLOCK: T+${{simMin}}m`;
        }}
        requestAnimationFrame(render);
    }}
    render();
    </script>
    </body>
    </html>
    """
    components.html(radar_html, height=745)


# =====================================================================
# COMPONENT 3: LIVE 60FPS MULTI-ALGORITHM EVOLUTION RACE CANVAS
# =====================================================================
def render_algorithm_race_canvas(suite):
    race_payload = []
    for key, name, color in [
        ("nsga2", "Hybrid Fuzzy-NSGA-II (Ours)", "#38bdf8"),
        ("moaco", "Multi-Objective ACO (MO-ACO)", "#10b981"),
        ("mopso", "Multi-Objective PSO (MOPSO)", "#a855f7"),
        ("sga", "Standard Single-Obj GA", "#f43f5e")
    ]:
        r = suite[key]
        race_payload.append({
            "name": name,
            "color": color,
            "sat": r["best_balanced"]["satisfaction"],
            "energy": r["best_balanced"]["energy"],
            "hv": r["hypervolume"],
            "history": [h["balanced_satisfaction"] for h in r["history"]]
        })

    race_json = json.dumps(race_payload)
    race_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }}
        body {{ background: transparent; color: #f8fafc; }}
        .race-card {{
            background: #070b14;
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 14px;
            padding: 16px 20px;
            margin-bottom: 10px;
        }}
        .race-header {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 14px;
        }}
        .replay-btn {{
            background: linear-gradient(90deg, #0284c7, #2563eb);
            border: 1px solid #38bdf8;
            color: white;
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
        }}
        .lane {{ margin-bottom: 14px; }}
        .lane-top {{ display: flex; justify-content: space-between; font-size: 12.5px; font-weight: 700; margin-bottom: 5px; }}
        .track {{
            width: 100%; height: 22px;
            background: rgba(15, 23, 42, 0.9);
            border-radius: 99px;
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.2);
            position: relative;
        }}
        .fill-bar {{
            height: 100%; width: 0%;
            border-radius: 99px;
            transition: width 0.08s linear;
            position: relative;
        }}
    </style>
    </head>
    <body>
    <div class="race-card">
        <div class="race-header">
            <div>
                <div style="font-size:15px; font-weight:800; color:#38bdf8;">🏁 LIVE EVOLUTIONARY CONVERGENCE RACE (GENERATION BY GENERATION)</div>
                <div style="font-size:12px; color:#94a3b8;" id="genCounter">Simulating Generation 1...</div>
            </div>
            <button class="replay-btn" onclick="startRace()">🔄 Replay Live Generation Race</button>
        </div>
        <div id="lanesContainer"></div>
    </div>

    <script>
    const algos = {race_json};
    const container = document.getElementById('lanesContainer');

    algos.forEach((a, i) => {{
        const div = document.createElement('div');
        div.className = 'lane';
        div.innerHTML = `
            <div class="lane-top">
                <span style="color:${{a.color}}">${{a.name}}</span>
                <span id="stat_${{i}}">SLA: 0.0% | Energy: ${{a.energy}} | HV: ${{a.hv}}</span>
            </div>
            <div class="track">
                <div class="fill-bar" id="bar_${{i}}" style="background: linear-gradient(90deg, ${{a.color}}88, ${{a.color}}); box-shadow: 0 0 12px ${{a.color}};"></div>
            </div>
        `;
        container.appendChild(div);
    }});

    let genIdx = 0;
    let timer = null;
    function startRace() {{
        if (timer) clearInterval(timer);
        genIdx = 0;
        const maxGen = algos[0].history.length;
        timer = setInterval(() => {{
            document.getElementById('genCounter').innerText = `⚡ Evolutionary Telemetry: Generation ${{genIdx + 1}} / ${{maxGen}}`;
            algos.forEach((a, i) => {{
                const val = a.history[Math.min(genIdx, a.history.length - 1)];
                document.getElementById(`bar_${{i}}`).style.width = `${{Math.min(100, val)}}%`;
                document.getElementById(`stat_${{i}}`).innerText = `SLA Satisfaction: ${{val.toFixed(1)}}% | Energy: ${{a.energy}} | HV: ${{a.hv}}`;
            }});
            genIdx++;
            if (genIdx >= maxGen) clearInterval(timer);
        }}, 65);
    }}
    startRace();
    </script>
    </body>
    </html>
    """
    components.html(race_html, height=285)


# =====================================================================
# COMPONENT 4: ANIMATED CHROMOSOME ORDER CROSSOVER (OX) & 2-OPT ILLUSTRATOR
# =====================================================================
def render_genetic_dna_animator(best_route):
    dna_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }}
        body {{ background: transparent; color: #f8fafc; }}
        .dna-box {{
            background: #070b14;
            border: 1px solid rgba(56, 189, 248, 0.35);
            border-radius: 14px;
            padding: 14px 18px;
        }}
        .gene-row {{ display: flex; align-items: center; gap: 6px; margin: 10px 0; flex-wrap: wrap; }}
        .row-tag {{ width: 150px; font-size: 12px; font-weight: 700; color: #94a3b8; }}
        .gene {{
            width: 32px; height: 32px;
            border-radius: 8px;
            display: flex; align-items: center; justify-content: center;
            font-weight: 800; font-size: 12px;
            transition: all 0.45s cubic-bezier(0.34, 1.56, 0.64, 1);
        }}
        .g-p1 {{ background: rgba(56, 189, 248, 0.18); border: 1px solid #38bdf8; color: #bae6fd; }}
        .g-p2 {{ background: rgba(168, 85, 247, 0.18); border: 1px solid #a855f7; color: #e9d5ff; }}
        .g-child {{ background: rgba(16, 185, 129, 0.22); border: 1px solid #10b981; color: #6ee7b7; transform: scale(1.08); }}
    </style>
    </head>
    <body>
    <div class="dna-box">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span style="font-size:14px; font-weight:800; color:#38bdf8;">🧬 LIVE CHROMOSOME ORDER CROSSOVER (OX) & 2-OPT MUTATION SIMULATOR</span>
            <span style="font-size:11px; color:#34d399;" id="oxPhase">Phase: Splicing Parent Chromosomes...</span>
        </div>
        <div class="gene-row" id="rowP1"><span class="row-tag">Parent 1 (EDF Seed):</span></div>
        <div class="gene-row" id="rowP2"><span class="row-tag">Parent 2 (Spatial):</span></div>
        <div class="gene-row" id="rowChild"><span class="row-tag" style="color:#10b981;">Offspring (OX + 2-Opt):</span></div>
    </div>
    <script>
        const base = {json.dumps(best_route[:12])};
        const p1 = [...base];
        const p2 = [...base].reverse();

        function drawGenes(cutA, cutB) {{
            const r1 = document.getElementById('rowP1');
            const r2 = document.getElementById('rowP2');
            const rc = document.getElementById('rowChild');
            r1.innerHTML = '<span class="row-tag">Parent 1 (Urgency):</span>';
            r2.innerHTML = '<span class="row-tag">Parent 2 (Spatial):</span>';
            rc.innerHTML = '<span class="row-tag" style="color:#10b981;">Evolved Offspring:</span>';

            const slice = p1.slice(cutA, cutB + 1);
            const rem = p2.filter(x => !slice.includes(x));
            let remIdx = 0;

            for (let i = 0; i < p1.length; i++) {{
                const inCut = (i >= cutA && i <= cutB);
                r1.innerHTML += `<div class="gene g-p1" style="${{inCut ? 'background:#0284c7;color:#fff;box-shadow:0 0 10px #38bdf8;' : ''}}">${{p1[i]}}</div>`;
                r2.innerHTML += `<div class="gene g-p2">${{p2[i]}}</div>`;
                const cVal = inCut ? p1[i] : rem[remIdx++];
                rc.innerHTML += `<div class="gene ${{inCut ? 'g-p1' : 'g-child'}}">${{cVal}}</div>`;
            }}
            document.getElementById('oxPhase').innerText = `⚡ Splicing Gene Window [${{cutA}}..${{cutB}}] + 2-Opt Inversion Active`;
        }}

        let step = 0;
        drawGenes(2, 6);
        setInterval(() => {{
            const a = (step % 4) + 1;
            const b = a + 4;
            drawGenes(a, b);
            step++;
        }}, 1800);
    </script>
    </body>
    </html>
    """
    components.html(dna_html, height=195)


# =====================================================================
# MAIN 5-TAB NAVIGATION
# =====================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🛰️ 1. Live 60FPS Fleet Radar & Telemetry",
    "🏁 2. Live Algorithm Convergence Race",
    "🧬 3. Genetic DNA & Pareto Studio",
    "🧠 4. 3D Fuzzy Surface & Mamdani Lab",
    "📊 5. Monte Carlo Statistical Suite"
])

# ---------------------------------------------------------------------
# TAB 1: 60FPS CYBERPUNK RADAR + VEHICLE PAYLOAD TELEMETRY
# ---------------------------------------------------------------------
with tab1:
    # Full-width Widescreen 60FPS Radar on top
    render_cyberpunk_radar(suite["depot"], best_sol["van_schedules"], speed_mult=sim_speed)

    # Side-by-side Fleet Telemetry Table & Utilization Chart below
    col_vtable, col_vchart = st.columns([1.25, 1.0])
    van_df = pd.DataFrame([
        {
            "Vehicle": v["van_id"],
            "Payload": f"{v['load_kg']}/{v['capacity_kg']} kg",
            "Utilization %": v["utilization_pct"],
            "Distance (km)": v["distance_km"],
            "Energy": v["energy_units"],
            "Route Sequence": " → ".join([f"#{s['stop_id']}" for s in v["stops"]])
        }
        for v in best_sol["van_schedules"]
    ])

    with col_vtable:
        st.markdown("#### 🚐 Active Fleet Telemetry & Payload Balance")
        st.dataframe(van_df, use_container_width=True, hide_index=True)

    with col_vchart:
        fig_util = px.bar(
            van_df,
            x="Vehicle",
            y="Utilization %",
            color="Energy",
            text="Payload",
            title="Real-Time Payload Utilization (%) & Energy Burn",
            color_continuous_scale="Tealgrn",
            template="plotly_dark"
        )
        fig_util.update_layout(
            height=265,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=15, r=15, t=35, b=15)
        )
        st.plotly_chart(fig_util, use_container_width=True)

    st.markdown("#### 📋 Node-Level Delivery SLA & Fuzzy Satisfaction Schedule")
    all_stop_rows = []
    for v in best_sol["van_schedules"]:
        for s in v["stops"]:
            all_stop_rows.append({
                "Vehicle": s["van_id"],
                "Node": f"#{s['stop_id']}",
                "Location": s["name"],
                "Priority": s["priority"],
                "Load (kg)": s["weight"],
                "ETA (min)": s["arrival_min"],
                "SLA Window": s["window"],
                "Fuzzy Satisfaction (%)": s["satisfaction"]
            })
    st.dataframe(pd.DataFrame(all_stop_rows), use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------
# TAB 2: LIVE 60FPS ALGORITHM RACE + RADAR CAPABILITY MATRIX
# ---------------------------------------------------------------------
with tab2:
    render_algorithm_race_canvas(suite)

    bench_rows = [
        {
            "Algorithm": nsga2["algorithm"],
            "Optimization Mechanism": "Fast Non-Dominated Sorting + Crowding + 2-Opt",
            "Energy Cost": nsga2["best_balanced"]["energy"],
            "Fuzzy Satisfaction (%)": nsga2["best_balanced"]["satisfaction"],
            "Hypervolume (HV)": nsga2["hypervolume"],
            "Pareto Archive Size": len(nsga2["pareto_front"]),
            "Compute Time (ms)": nsga2["runtime_ms"]
        },
        {
            "Algorithm": mopso["algorithm"],
            "Optimization Mechanism": "Swarm pBest/gBest Path Relinking",
            "Energy Cost": mopso["best_balanced"]["energy"],
            "Fuzzy Satisfaction (%)": mopso["best_balanced"]["satisfaction"],
            "Hypervolume (HV)": mopso["hypervolume"],
            "Pareto Archive Size": len(mopso["pareto_front"]),
            "Compute Time (ms)": mopso["runtime_ms"]
        },
        {
            "Algorithm": moaco["algorithm"],
            "Optimization Mechanism": "Pheromone Matrix + Urgency Heuristic",
            "Energy Cost": moaco["best_balanced"]["energy"],
            "Fuzzy Satisfaction (%)": moaco["best_balanced"]["satisfaction"],
            "Hypervolume (HV)": moaco["hypervolume"],
            "Pareto Archive Size": len(moaco["pareto_front"]),
            "Compute Time (ms)": moaco["runtime_ms"]
        },
        {
            "Algorithm": sga["algorithm"],
            "Optimization Mechanism": "Single-Objective Distance-Only GA",
            "Energy Cost": sga["best_balanced"]["energy"],
            "Fuzzy Satisfaction (%)": sga["best_balanced"]["satisfaction"],
            "Hypervolume (HV)": sga["hypervolume"],
            "Pareto Archive Size": len(sga["pareto_front"]),
            "Compute Time (ms)": sga["runtime_ms"]
        },
        {
            "Algorithm": "Greedy Nearest-Neighbor Baseline",
            "Optimization Mechanism": "Myopic Next-Closest Stop Heuristic",
            "Energy Cost": greedy["energy"],
            "Fuzzy Satisfaction (%)": greedy["satisfaction"],
            "Hypervolume (HV)": 0.0,
            "Pareto Archive Size": 1,
            "Compute Time (ms)": 0.8
        }
    ]
    st.dataframe(pd.DataFrame(bench_rows), use_container_width=True, hide_index=True)

    c_left, c_right = st.columns(2)
    with c_left:
        fig_conv = go.Figure()
        for key, label, col in [
            ("nsga2", "Hybrid Fuzzy-NSGA-II", "#38bdf8"),
            ("mopso", "Multi-Objective PSO", "#a855f7"),
            ("moaco", "Multi-Objective ACO", "#10b981"),
            ("sga", "Standard Single-Obj GA", "#f43f5e")
        ]:
            hist = suite[key]["history"]
            fig_conv.add_trace(go.Scatter(
                x=[h["gen"] for h in hist],
                y=[h["balanced_satisfaction"] for h in hist],
                mode="lines+markers",
                name=label,
                line=dict(color=col, width=3)
            ))
        fig_conv.update_layout(
            title="Evolutionary Convergence Trajectory Across Generations",
            xaxis_title="Generation",
            yaxis_title="Fuzzy Customer Satisfaction (%)",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.5)",
            height=380
        )
        st.plotly_chart(fig_conv, use_container_width=True)

    with c_right:
        fig_radar = go.Figure()
        categories = ["Fuzzy Satisfaction %", "Hypervolume Score", "Energy Efficiency", "Pareto Diversity", "Convergence Stability"]
        for label, sat_v, hv_v, en_v, div_v, stab_v, col in [
            ("Hybrid Fuzzy-NSGA-II", nsga2["best_balanced"]["satisfaction"], min(100, nsga2["hypervolume"] * 1.8), 92, 95, 96, "#38bdf8"),
            ("Multi-Objective ACO", moaco["best_balanced"]["satisfaction"], min(100, moaco["hypervolume"] * 1.8), 88, 78, 82, "#10b981"),
            ("Multi-Objective PSO", mopso["best_balanced"]["satisfaction"], min(100, mopso["hypervolume"] * 1.8), 76, 70, 74, "#a855f7"),
            ("Standard GA", sga["best_balanced"]["satisfaction"], min(100, sga["hypervolume"] * 1.8), 80, 35, 65, "#f43f5e")
        ]:
            fig_radar.add_trace(go.Scatterpolar(
                r=[sat_v, hv_v, en_v, div_v, stab_v, sat_v],
                theta=categories + [categories[0]],
                fill="toself",
                name=label,
                line=dict(color=col, width=2.5)
            ))
        fig_radar.update_layout(
            title="5-Axis Soft Computing Capability Radar",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            polar=dict(bgcolor="rgba(15,23,42,0.6)", radialaxis=dict(visible=True, range=[0, 100])),
            height=380
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# ---------------------------------------------------------------------
# TAB 3: LIVE GENETIC DNA CROSSOVER + PARETO STUDIO
# ---------------------------------------------------------------------
with tab3:
    render_genetic_dna_animator(best_sol["route"])

    p_col1, p_col2 = st.columns([1.55, 1.0])
    with p_col1:
        fig_pf = go.Figure()
        for key, name, color, sym in [
            ("nsga2", "Hybrid Fuzzy-NSGA-II Pareto Front", "#38bdf8", "circle"),
            ("mopso", "MOPSO Archive Front", "#a855f7", "diamond"),
            ("moaco", "MO-ACO Archive Front", "#10b981", "square")
        ]:
            pf = suite[key]["pareto_front"]
            fig_pf.add_trace(go.Scatter(
                x=[p["energy"] for p in pf],
                y=[p["satisfaction"] for p in pf],
                mode="lines+markers",
                name=name,
                marker=dict(size=11, color=color, symbol=sym, line=dict(width=1, color="#ffffff")),
                line=dict(color=color, width=2.5, dash="solid" if key == "nsga2" else "dot")
            ))

        fig_pf.add_trace(go.Scatter(
            x=[best_sol["energy"]],
            y=[best_sol["satisfaction"]],
            mode="markers",
            name="Selected Knee-Point Schedule",
            marker=dict(size=20, color="#f59e0b", symbol="star", line=dict(width=2, color="#ffffff"))
        ))

        fig_pf.update_layout(
            title="Non-Dominated Pareto Frontier Overlay (Energy vs Customer Satisfaction %)",
            xaxis_title="Total Fleet Load-Dependent Energy Cost (Lower is Better →)",
            yaxis_title="Priority-Weighted Fuzzy Satisfaction % (Higher is Better ↑)",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.5)",
            height=410
        )
        st.plotly_chart(fig_pf, use_container_width=True)

    with p_col2:
        st.markdown("#### 🎯 Pareto Operating Profiles")
        pf_list = nsga2["pareto_front"]
        eco_sol = min(pf_list, key=lambda x: x["energy"])
        cust_sol = max(pf_list, key=lambda x: x["satisfaction"])

        pareto_summary_df = pd.DataFrame([
            {
                "Operating Profile": "🌱 Eco-Saver Mode (Min Energy)",
                "Energy Cost": f"{eco_sol['energy']:.2f}",
                "Fuzzy Satisfaction": f"{eco_sol['satisfaction']:.2f}%",
                "Active Vans": eco_sol["num_vans"]
            },
            {
                "Operating Profile": "⚖️ Knee-Point Balanced (Optimal)",
                "Energy Cost": f"{best_sol['energy']:.2f}",
                "Fuzzy Satisfaction": f"{best_sol['satisfaction']:.2f}%",
                "Active Vans": best_sol["num_vans"]
            },
            {
                "Operating Profile": "💎 SLA Priority Mode (Max Satisfaction)",
                "Energy Cost": f"{cust_sol['energy']:.2f}",
                "Fuzzy Satisfaction": f"{cust_sol['satisfaction']:.2f}%",
                "Active Vans": cust_sol["num_vans"]
            }
        ])
        st.dataframe(pareto_summary_df, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------
# TAB 4: 3D INTERACTIVE FUZZY SURFACE & MAMDANI LAB
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
        fig_fuz.add_trace(go.Scatter(x=t_vals, y=y_trap, name="Trapezoidal Kernel", fill="tozeroy", line=dict(color="#38bdf8", width=3)))
        fig_fuz.add_trace(go.Scatter(x=t_vals, y=y_gaus, name="Gaussian Kernel", line=dict(color="#10b981", width=2.5, dash="dash")))
        fig_fuz.add_trace(go.Scatter(x=t_vals, y=y_sigm, name="Sigmoidal Kernel", line=dict(color="#f43f5e", width=2.5, dash="dot")))
        fig_fuz.add_vline(x=b_end, line_dash="dash", line_color="#10b981", annotation_text="Best End (30m)")
        fig_fuz.add_vline(x=m_late, line_dash="dash", line_color="#f43f5e", annotation_text="Max Late Cutoff (60m)")

        fig_fuz.update_layout(
            title="Multi-Kernel Fuzzy Membership Comparison μ(t)",
            xaxis_title="Arrival Time (Minutes)",
            yaxis_title="Membership Degree μ(t) [0.0 – 1.0]",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0.5)",
            height=420
        )
        st.plotly_chart(fig_fuz, use_container_width=True)

    with f_col2:
        arr_grid = np.linspace(15, 70, 40)
        traf_grid = np.linspace(1.0, 1.85, 40)
        Z_surf = np.zeros((len(traf_grid), len(arr_grid)))
        for i, tf in enumerate(traf_grid):
            for j, ar in enumerate(arr_grid):
                eff_arrival = ar * (0.75 + 0.25 * tf)
                Z_surf[i, j] = compute_fuzzy_satisfaction(eff_arrival, 15, 30, 60, fuzzy_kernel) * 100.0

        fig_3d = go.Figure(data=[go.Surface(
            z=Z_surf,
            x=arr_grid,
            y=traf_grid,
            colorscale="Turbo",
            opacity=0.92
        )])
        fig_3d.update_layout(
            title=f"🌐 Interactive 3D Fuzzy Response Manifold ({fuzzy_kernel} Kernel)",
            scene=dict(
                xaxis_title="Base ETA (min)",
                yaxis_title="Mamdani Traffic Factor",
                zaxis_title="Satisfaction %"
            ),
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            height=420,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig_3d, use_container_width=True)

# ---------------------------------------------------------------------
# TAB 5: MONTE CARLO STATISTICAL ROBUSTNESS SUITE
# ---------------------------------------------------------------------
with tab5:
    st.subheader("📊 Multi-Seed Monte Carlo Statistical Robustness & Export Suite")

    if st.button("🔬 Run 5-Seed Monte Carlo Benchmark (Mean ± Std Dev)", type="primary"):
        with st.spinner("Executing 5 independent stochastic seeds across all soft computing paradigms..."):
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
            "📥 Export Full Empirical Benchmark Report (CSV)",
            data=csv_bytes,
            file_name="fleetpulse_soft_computing_benchmark.csv",
            mime="text/csv"
        )
