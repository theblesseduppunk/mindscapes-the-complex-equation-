import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import json
from io import StringIO
import time

from utils import compute_consciousness, compute_creativity, generate_random_scenario, ai_suggestions

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="MindScape (The Complex Equation Simulator)", 
                   page_icon="🧠", layout="wide")

# ------------------------------
# Cyberpunk / Futuristic Styling
# ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');

body { font-family:'Orbitron', monospace; color:#00ffff; background:#0a0a0a; }
.welcome-box {padding:30px; border-radius:15px; background:rgba(0,0,0,0.7); box-shadow:0 0 30px cyan; text-align:center; margin-bottom:30px; animation: fadeIn 1.5s;}
.launch-btn {background: linear-gradient(90deg, cyan, magenta); border:none; padding:15px 30px; border-radius:25px; font-size:1.3em; font-weight:bold; cursor:pointer;}
.launch-btn:hover { transform: scale(1.05); box-shadow:0 0 25px cyan, 0 0 25px magenta; }
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
        A simulation creator, the first of its kind, by <b>Sam Andrews Rodriguez II</b>.<br>
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
# Helper Functions
# ------------------------------
def animate_sliders(target_values, steps=15, delay=0.03):
    for i in range(1, steps+1):
        for key in st.session_state.sliders:
            current = st.session_state.sliders[key]
            st.session_state.sliders[key] = current + (target_values[key]-current)*(i/steps)
        time.sleep(delay)
        st.experimental_rerun()

# ------------------------------
# Scenario Buttons
# ------------------------------
if st.sidebar.button("📈 Load Demo Scenario"):
    animate_sliders(demo_values)
if st.sidebar.button("🎲 Generate Random Scenario"):
    scenario = generate_random_scenario(list(default_values.keys()))
    animate_sliders(scenario)

target_variable = st.sidebar.selectbox("Select variable to solve for:", variables, index=variables.index("C"))

# Unique slider keys
slider_values = {}
for i, var in enumerate(default_values.keys()):
    slider_values[var] = st.sidebar.slider(f"{var}",0.1,10.0,st.session_state.sliders[var],0.1, key=f"{var}_slider")

# AI Buddy
ai_tab = st.sidebar.expander("🤖 AIBuddy Suggestions")
ai_choices = ai_suggestions(slider_values)
for name, vals in ai_choices:
    if ai_tab.button(f"💡 {name}"):
        animate_sliders(vals)

# Compute main variable
C_complex = compute_consciousness(**slider_values)
st.session_state.sliders.update(slider_values)
st.session_state.history.append({**slider_values,"C":C_complex})

# ------------------------------
# Main Tabs
# ------------------------------
tabs = st.tabs(["Simulation","Beginner Equation","3D Simulator","Possibilities","History","About"])

# -------- Simulation Tab --------
with tabs[0]:
    st.markdown("<div class='tab-header'>📊 Consciousness Simulation</div>", unsafe_allow_html=True)
    influences = {k:slider_values[k] for k in ["R","A","S","Q","E","M"]}
    most_influential = max(influences.items(), key=lambda x:x[1])[0]
    st.info(f"Currently, **{most_influential}** has the largest impact on {target_variable}")
    
    st.markdown(f"<div class='metric-display'>{target_variable} = {C_complex:.4f}</div>", unsafe_allow_html=True)

# -------- 3D Simulator Tab --------
with tabs[2]:
    st.markdown("<div class='tab-header'>🌐 3D Variable Interaction Map</div>", unsafe_allow_html=True)
    all_vars = list(slider_values.keys())
    col1, col2, col3 = st.columns(3)
    with col1: x_var = st.selectbox("X-axis variable:", all_vars, index=all_vars.index("S"))
    with col2: y_var = st.selectbox("Y-axis variable:", all_vars, index=all_vars.index("A"))
    with col3: z_var = st.selectbox("Color by variable:", all_vars, index=all_vars.index("C"))
    
    X = np.linspace(0.1,10,30)
    Y = np.linspace(0.1,10,30)
    Z = np.zeros((len(X), len(Y)))
    for i, xv in enumerate(X):
        for j, yv in enumerate(Y):
            vals = slider_values.copy()
            vals[x_var] = xv
            vals[y_var] = yv
            Z[i,j] = compute_consciousness(**vals)
    
    fig3d = go.Figure(data=[go.Surface(z=Z,x=X,y=Y,colorscale='Viridis')])
    fig3d.update_layout(scene=dict(xaxis_title=x_var, yaxis_title=y_var, zaxis_title="C"), template="plotly_dark", height=600)
    st.plotly_chart(fig3d,use_container_width=True)

# -------- About Tab --------
with tabs[5]:
    st.markdown("<div class='tab-header'>📖 About MindScape</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='possibility'>
    <b>The Complex Equation:</b><br>
    C = (R × α^θ × S × Q × (1.3 × A) × E × (1.6 × M)) / (Dₙ × β^θ)<br>
    This equation captures the relationships between:
    <ul>
        <li><b>Consciousness (C):</b> The level of consciousness.</li>
        <li><b>Sensory processing (R):</b> The level of sensory processing.</li>
        <li><b>Attention (A):</b> The level of attention.</li>
        <li><b>Memory (M):</b> The level of memory.</li>
        <li><b>Emotional state (E):</b> The emotional state.</li>
        <li><b>Quality of information (Q):</b> The quality of information.</li>
        <li><b>Neural complexity (Dₙ):</b> The level of neural complexity.</li>
        <li><b>α and β:</b> Parameters influencing relationships between variables.</li>
        <li><b>θ:</b> A parameter influencing non-linearity of relationships.</li>
    </ul>
    
    <b>Beginner Equation:</b><br>
    C = R / D³<br><br>
    
    MindScape was created by <b>Sam Andrews Rodriguez II, 2025</b>.<br>
    It allows exploration of human and AI interactions, creativity landscapes, immersive experiences, and cognitive simulations.<br>
    AI Buddy provides guided scenario suggestions for balanced, high-consciousness, or creative states.
    </div>
    """, unsafe_allow_html=True)
