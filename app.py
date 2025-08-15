import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import json
from io import StringIO
import time
from utils import generate_random_scenario, compute_consciousness, compute_creativity, ai_suggestions

# ------------------------------
# Page Setup
# ------------------------------
st.set_page_config(page_title="MindScape", page_icon="🧠", layout="wide")

# ------------------------------
# Styling (Futuristic)
# ------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
body {font-family:'Orbitron', monospace; color:#00ffff; background:#0a0a0a;}
.welcome-box {padding:30px; border-radius:15px; background: rgba(0,0,0,0.7); text-align:center;}
.launch-btn {background: linear-gradient(90deg, cyan, magenta); border:none; padding:15px 30px; border-radius:25px; cursor:pointer;}
.metric-display {font-size:1.8em; color:#00ffff;}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Session state
# ------------------------------
variables = ["R","alpha","theta","S","Q","A","E","M","Dn","beta","C"]
default_values = {"R":5.0,"alpha":1.0,"theta":1.0,"S":5.0,"Q":5.0,"A":5.0,"E":5.0,"M":5.0,"Dn":5.0,"beta":1.0}

if "sliders" not in st.session_state:
    st.session_state.sliders = default_values.copy()
if "history" not in st.session_state:
    st.session_state.history = []

demo_values = {"R":7.0,"alpha":1.2,"theta":1.0,"S":8.0,"Q":7.0,"A":9.0,"E":6.0,"M":8.0,"Dn":2.0,"beta":1.0}

# ------------------------------
# Welcome
# ------------------------------
st.markdown("""
<div class="welcome-box">
    <div style="font-size:2.8em; font-weight:bold;">🚀 MindScape</div>
    <div style="margin-top:10px; font-size:1.3em;">
        A simulation creator by <b>Sam Andrews Rodriguez II</b>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------
# Sidebar
# ------------------------------
st.sidebar.header("Parameters / Scenario Generation")

target_variable = st.sidebar.selectbox("Select variable to solve for:", variables, index=variables.index("C"))

slider_values = {}
for var in default_values.keys():
    slider_values[var] = st.sidebar.slider(var, 0.1, 10.0, st.session_state.sliders[var], 0.1, key=f"slider_{var}")

# Scenario buttons
if st.sidebar.button("📈 Load Demo Scenario"):
    for k,v in demo_values.items(): st.session_state.sliders[k] = v
    st.experimental_rerun()
if st.sidebar.button("🎲 Generate Random Scenario"):
    random_vals = generate_random_scenario(slider_values.keys())
    for k,v in random_vals.items(): st.session_state.sliders[k] = v
    st.experimental_rerun()

# AI Buddy
ai_tab = st.sidebar.expander("🤖 AIBuddy Suggestions")
ai_choices = ai_suggestions(slider_values)
for name, vals in ai_choices:
    if ai_tab.button(f"💡 {name}"):
        for k,v in vals.items(): st.session_state.sliders[k] = v
        st.experimental_rerun()

# Compute C
C_value = compute_consciousness(**slider_values)
st.session_state.sliders.update(slider_values)
st.session_state.history.append({**slider_values,"C":C_value})

# ------------------------------
# Tabs
# ------------------------------
tabs = st.tabs(["Simulation","Beginner Equation","3D Simulator","History","About"])

# ---- Simulation Tab ----
with tabs[0]:
    st.markdown(f"<div class='metric-display'>{target_variable} = {C_value:.4f}</div>", unsafe_allow_html=True)

# ---- Beginner Equation ----
with tabs[1]:
    R_val = st.slider("Reality (R)", 0.1, 10.0, 5.0, 0.1, key="R_dynamic")
    D_val = st.slider("Dimensionality (D³)", 0.1, 10.0, 2.0, 0.1, key="D3_dynamic")
    C_grid_val = compute_creativity(R_val, D_val)
    st.markdown(f"<div class='metric-display'>Creativity (C) = {C_grid_val:.4f}</div>", unsafe_allow_html=True)

# ---- 3D Simulator ----
with tabs[2]:
    st.subheader("🌐 3D Variable Interaction Map")
    col1, col2, col3 = st.columns(3)
    all_vars = list(slider_values.keys())
    default_x, default_y, default_z = "S","A","C"
    if default_x not in all_vars: default_x = all_vars[0]
    if default_y not in all_vars: default_y = all_vars[0]
    if default_z not in all_vars: default_z = all_vars[0]

    with col1: x_var = st.selectbox("X-axis:", all_vars, index=all_vars.index(default_x))
    with col2: y_var = st.selectbox("Y-axis:", all_vars, index=all_vars.index(default_y))
    with col3: z_var = st.selectbox("Color by:", all_vars, index=all_vars.index(default_z))

    X = np.linspace(0.1, 10, 30)
    Y = np.linspace(0.1, 10, 30)
    Z = np.zeros((len(X), len(Y)))
    for i, xv in enumerate(X):
        for j, yv in enumerate(Y):
            vals = slider_values.copy()
            vals[x_var] = xv
            vals[y_var] = yv
            Z[i,j] = compute_consciousness(**vals) if z_var=="C" else vals[z_var]

    fig3d = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])
    fig3d.update_layout(scene=dict(xaxis_title=x_var, yaxis_title=y_var, zaxis_title=z_var), template="plotly_dark", height=600)
    st.plotly_chart(fig3d, use_container_width=True)

# ---- History ----
with tabs[3]:
    st.dataframe(pd.DataFrame(st.session_state.history))
    data = {**st.session_state.sliders,"C":C_value}
    df = pd.DataFrame([data])
    csv_buffer = StringIO()
    df.to_csv(csv_buffer,index=False)
    st.download_button("Download CSV", csv_buffer.getvalue(),"mindscape_result.csv","text/csv")
    st.download_button("Download JSON", json.dumps(data,indent=4),"mindscape_result.json","application/json")

# ---- About ----
with tabs[4]:
    st.markdown("""
    ### About MindScape
    **Complex Equation:**
    C = (R × α^θ × S × Q × (1.3 × A) × E × (1.6 × M)) / (Dₙ × β^θ)

    This equation captures the relationships between:

    - Consciousness (C): The level of consciousness.
    - Sensory processing (R): The level of sensory processing.
    - Attention (A): The level of attention.
    - Memory (M): The level of memory.
    - Emotional state (E): The emotional state.
    - Quality of information (Q): The quality of information.
    - Neural complexity (Dₙ): The level of neural complexity.
    - α and β: Parameters that influence the relationships between variables.
    - θ: A parameter that influences the non-linearity of the relationships.

    MindScape was created by Sam Andrews Rodriguez II, 2025.
    """)
