import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import json
from io import StringIO
import random
import time

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="MindScape (The Complex Equation Simulator)", 
                   page_icon="🧠", layout="wide")

# ------------------------------
# Futuristic / Cyberpunk Styling
# ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

body {font-family:'Orbitron', monospace; color: #00ffff; background: linear-gradient(135deg,#0a0a0a,#111122);}

@keyframes fadeIn {from {opacity:0; transform:translateY(-10px);} to {opacity:1; transform:translateY(0);} }
@keyframes pulse {0% {text-shadow:0 0 5px cyan,0 0 10px magenta;} 50% {text-shadow:0 0 15px cyan,0 0 25px magenta;} 100% {text-shadow:0 0 5px cyan,0 0 10px magenta;}}

.welcome-box {animation: fadeIn 1.5s ease-out forwards; padding:30px; border-radius:15px; background:rgba(0,0,0,0.7); backdrop-filter:blur(10px); box-shadow:0 0 30px rgba(0,255,255,0.5); color:#00ffff; text-align:center; margin-bottom:30px;}
.launch-btn {background: linear-gradient(90deg, cyan, magenta); border:none; padding:15px 30px; border-radius:25px; color:black; font-size:1.3em; font-weight:bold; cursor:pointer; transition:all 0.3s ease;}
.launch-btn:hover { transform: scale(1.05); box-shadow: 0 0 25px cyan, 0 0 25px magenta; }

.slider-label {color:#00ffff; font-weight:bold;}
.metric-display {animation: pulse 2s infinite; font-size:1.8em; color:#00ffff; text-shadow:0 0 10px #00ffff, 0 0 20px #ff00ff;}
.tab-header {font-size:2em; color:#00ffff; font-weight:bold; margin-top:10px; text-shadow:0 0 10px #00ffff,0 0 20px #ff00ff;}
.possibility {margin:10px 0; padding:10px; border-radius:10px; background: rgba(0,0,0,0.5); border:1px solid #00ffff; box-shadow:0 0 15px #ff00ff;}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Welcome Section
# ------------------------------
st.markdown("""
<div class="welcome-box">
    <div style="font-size:2.8em; font-weight:bold;">🚀 MindScape</div>
    <div style="margin-top:10px; font-size:1.3em;">
        A simulation creator by <b>Sam Andrews Rodriguez II</b>.<br>
        Explore consciousness, creativity, dimensionality, and AI-driven scenarios.
    </div>
    <hr style="border:0.5px solid #00ffff; margin:15px 0;">
    <button class="launch-btn" onclick="window.scrollTo({top: 500, behavior: 'smooth'});">🔥 Launch Simulation</button>
</div>
""", unsafe_allow_html=True)

# ------------------------------
# Sidebar Parameters
# ------------------------------
st.sidebar.header("Adjust Parameters / Generate Scenarios")
variables = ["R","alpha","theta","S","Q","A","E","M","Dn","beta","C"]
default_values = {"R":5.0,"alpha":1.0,"theta":1.0,"S":5.0,"Q":5.0,"A":5.0,"E":5.0,"M":5.0,"Dn":5.0,"beta":1.0}

if "sliders" not in st.session_state:
    st.session_state.sliders = default_values.copy()
if "history" not in st.session_state:
    st.session_state.history = []

demo_values = {"R":7.0,"alpha":1.2,"theta":1.0,"S":8.0,"Q":7.0,"A":9.0,"E":6.0,"M":8.0,"Dn":2.0,"beta":1.0}

# ------------------------------
# Functions
# ------------------------------
def generate_random_scenario():
    return {k: round(random.uniform(0.1,10.0),1) for k in st.session_state.sliders.keys()}

def animate_sliders(target_values, steps=15, delay=0.03):
    for i in range(1, steps + 1):
        for key in st.session_state.sliders:
            current = st.session_state.sliders[key]
            st.session_state.sliders[key] = current + (target_values[key] - current) * (i / steps)
        time.sleep(delay)
    st.experimental_rerun()

def compute_consciousness(R, alpha, theta, S, Q, A, E, M, Dn, beta):
    return (R*(alpha**theta)*S*Q*(1.3*A)*E*(1.6*M)) / (Dn*(beta**theta))

def compute_creativity(R, D3):
    return R / (D3**3)

def ai_suggestions(current_values):
    suggestions = []
    balanced = {k:5.0 for k in current_values.keys()}
    suggestions.append(("Balanced", balanced))
    high_c = {k: round(random.uniform(7.5,10.0),1) for k in current_values.keys()}
    suggestions.append(("High Consciousness", high_c))
    creative = {k: round(random.uniform(0.5,10.0),1) for k in current_values.keys()}
    suggestions.append(("Creative AI Insight", creative))
    return suggestions

# ------------------------------
# Scenario Buttons
# ------------------------------
if st.sidebar.button("📈 Load Demo Scenario", key="demo_button"):
    animate_sliders(demo_values)
if st.sidebar.button("🎲 Generate Random Scenario", key="random_button"):
    animate_sliders(generate_random_scenario())

target_variable = st.sidebar.selectbox("Select variable to solve for:", variables, index=variables.index("C"), key="target_var")

# Display sliders with unique keys
slider_values = {}
for var in default_values.keys():
    slider_values[var] = st.sidebar.slider(
        f"{var}",
        0.1, 10.0,
        st.session_state.sliders.get(var, default_values[var]),
        0.1,
        key=f"slider_{var}"
    )

# AIBuddy Suggestions
ai_tab = st.sidebar.expander("🤖 AIBuddy Suggestions")
ai_choices = ai_suggestions(slider_values)
for idx, (name, vals) in enumerate(ai_choices):
    if ai_tab.button(f"💡 {name}", key=f"aibuddy_{idx}"):
        animate_sliders(vals)

# Compute main target variable
C_complex = compute_consciousness(**slider_values)
st.session_state.sliders.update(slider_values)
st.session_state.history.append({**slider_values,"C":C_complex})

# ------------------------------
# Tabs
# ------------------------------
tabs = st.tabs(["Simulation","Beginner Equation","3D Simulator","Possibilities","History","About"])

# -------- Simulation Tab --------
with tabs[0]:
    st.markdown("<div class='tab-header'>📊 Consciousness Simulation</div>", unsafe_allow_html=True)
    influences = {k:slider_values[k] for k in ["R","A","S","Q","E","M"]}
    most_influential = max(influences.items(), key=lambda x:x[1])[0]
    st.info(f"Currently, **{most_influential}** has the largest impact on {target_variable}")
    st.markdown(f"<div class='metric-display'>{target_variable} = {C_complex:.4f}</div>", unsafe_allow_html=True)

# -------- Beginner Equation Tab --------
with tabs[1]:
    st.markdown("<div class='tab-header'>🌐 Beginner Creativity Landscape</div>", unsafe_allow_html=True)
    R_val = st.slider("Reality (R)", 0.1, 10.0, 5.0, 0.1, key="R_dynamic")
    D3_val = st.slider("Dimensionality (D³)", 0.1, 10.0, 2.0, 0.1, key="D3_dynamic")
    C_grid = np.array([[compute_creativity(r,d) for d in np.linspace(0.1,10,30)] for r in np.linspace(0.1,10,30)])
    fig_dynamic = go.Figure(data=[go.Surface(z=C_grid)])
    st.plotly_chart(fig_dynamic, use_container_width=True)
    st.markdown(f"<div class='metric-display'>Creativity (C) = {compute_creativity(R_val, D3_val):.4f}</div>", unsafe_allow_html=True)

# -------- 3D Simulator Tab --------
with tabs[2]:
    st.markdown("<div class='tab-header'>🌌 3D Variable Interaction</div>", unsafe_allow_html=True)
    all_vars = list(slider_values.keys())
    col1, col2, col3 = st.columns(3)
    with col1:
        x_var = st.selectbox("X-axis variable:", all_vars, index=all_vars.index("S"), key="x_var")
    with col2:
        y_var = st.selectbox("Y-axis variable:", all_vars, index=all_vars.index("A"), key="y_var")
    with col3:
        z_var = st.selectbox("Color by variable:", all_vars, index=all_vars.index("C"), key="z_var")

    X = np.linspace(0.1,10,30)
    Y = np.linspace(0.1,10,30)
    Z = np.zeros((len(X), len(Y)))
    for i,xv in enumerate(X):
        for j,yv in enumerate(Y):
            vals = slider_values.copy()
            vals[x_var] = xv
            vals[y_var] = yv
            Z[i,j] = vals[z_var] if z_var != "C" else compute_consciousness(**vals)
    fig3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
    fig3d.update_layout(scene=dict(xaxis_title=x_var, yaxis_title=y_var, zaxis_title=z_var), template="plotly_dark", height=600)
    st.plotly_chart(fig3d, use_container_width=True)

# -------- Possibilities Tab --------
with tabs[3]:
    st.markdown("<div class='tab-header'>✨ Possibilities</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='possibility'>
    MindScape can simulate consciousness dynamics, creativity landscapes, and interactions between human, AI, and virtual dimensions.
    </div>
    """, unsafe_allow_html=True)

# -------- History Tab --------
with tabs[4]:
    st.markdown("<div class='tab-header'>📋 Scenario History / Comparison</div>", unsafe_allow_html=True)
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df)
    data = {**st.session_state.sliders,"C":C_complex}
    df = pd.DataFrame([data])
    csv_buffer = StringIO()
    df.to_csv(csv_buffer,index=False)
    st.download_button("Download Result as CSV",csv_buffer.getvalue(),"mindscape_result.csv","text/csv")
    st.download_button("Download Result as JSON",json.dumps(data,indent=4),"mindscape_result.json","application/json")

# -------- About Tab --------
with tabs[5]:
    st.markdown("<div class='tab-header'>📖 About MindScape</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='possibility'>
    <b>The Complex Equation:</b><br>
    C = (R × α^θ × S × Q × (1.3 × A) × E × (1.6 × M)) / (Dₙ × β^θ)<br>
    This equation captures the relationships between:
    <ul>
        <li>Consciousness (C): The level of consciousness.</li>
        <li>Sensory processing (R): The level of sensory processing.</li>
        <li>Attention (A): The level of attention.</li>
        <li>Memory (M): The level of memory.</li>
        <li>Emotional state (E): The emotional state.</li>
        <li>Quality of information (Q): The quality of information.</li>
        <li>Neural complexity (Dₙ): The level of neural complexity.</li>
        <li>α and β: Parameters that influence the relationships between variables.</li>
        <li>θ: A parameter that influences the non-linearity of the relationships.</li>
    </ul>
    MindScape was created by <b>Sam Andrews Rodriguez II, 2025</b>.
    </div>
    """, unsafe_allow_html=True)
