import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64

st.set_page_config(
    page_title="Crypto Volatility Visualizer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .main {
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        }
        
        .stApp {
            background-color: #0f0f1a;
        }
        
        h1, h2, h3 {
            color: #ffffff;
            font-weight: 600;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
            margin: 10px 0;
        }
        
        .logo-container {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            margin-bottom: 20px;
        }
        
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #1a1a2e 0%, #0f0f1a 100%);
        }
        
        .stSlider > label {
            color: #ffffff;
            font-weight: 500;
        }
        
        .stSelectbox > label {
            color: #ffffff;
            font-weight: 500;
        }
        
        .stCheckbox > label {
            color: #ffffff;
            font-weight: 500;
        }
        
        .stRadio > label {
            color: #ffffff;
            font-weight: 500;
        }
        
        .plotly-graph-div {
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        
        div[data-testid="stMetricValue"] {
            color: #ffffff;
            font-weight: 600;
        }
        
        div[data-testid="stMetricLabel"] {
            color: #ffffff;
            font-weight: 400;
        }
    </style>
    """, unsafe_allow_html=True)

load_css()


def display_logo():
    st.markdown("""
<div class="logo-container">
    <h1 style="margin: 10px 0;">📈 Crypto Volatility Visualizer</h1>
    <p style="color: rgba(255,255,255,0.8); margin: 0;">
        Interactive dashboard to explore real crypto volatility and simulate market swings
    </p>
</div>
""", unsafe_allow_html=True)

st.image("mascot.png", width=180)
display_logo()

def generate_crypto_data(days=365):
    np.random.seed(42)
    base_price = 45000
    dates = pd.date_range(end=datetime.now(), periods=days)
    
    
    returns = np.random.normal(0.02, 0.05, days)
    price = base_price * (1 + returns).cumprod()
    
 
    volatility = np.random.uniform(0.02, 0.08, days)
    
    df = pd.DataFrame({
        'Timestamp': dates,
        'Open': price * (1 - np.random.uniform(0.01, 0.03, days)),
        'High': price * (1 + np.random.uniform(0.01, 0.03, days)),
        'Low': price * (1 - np.random.uniform(0.01, 0.03, days)),
        'Close': price,
        'Volume': np.random.uniform(1000000, 50000000, days)
    })
    
    return df

try:
    
    DATA_FILE = btcusd_1-min_data.csv.crdownload
    df = pd.read_csv(DATA_FILE)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="s")
except:

    df = generate_crypto_data(days=500)

df = df.sort_values("Timestamp").reset_index(drop=True)


st.sidebar.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; margin-bottom: 20px;">
    <h2 style="color: white; margin: 0;">Sidebar controls</h2>
</div>
""", unsafe_allow_html=True)


time_range = st.sidebar.selectbox(
    "📅 Select Time Range",
    ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Full Dataset"],
    index=1,
    help="Choose the time period to analyze"
)

def filter_data(df, time_range):
    latest_date = df["Timestamp"].max()

    if time_range == "Last 7 Days":
        start_date = latest_date - timedelta(days=7)

    elif time_range == "Last 30 Days":
        start_date = latest_date - timedelta(days=30)

    elif time_range == "Last 90 Days":
        start_date = latest_date - timedelta(days=90)

    else:
        return df

    return df[df["Timestamp"] >= start_date]

df_filtered = filter_data(df, time_range)
time_range_title = time_range.replace("Last", "").strip()

st.sidebar.markdown("---")
st.sidebar.subheader("🎛Simulation Controls")

pattern = st.sidebar.selectbox(
    "🌊 Simulation Pattern",
    ["Sine Wave", "Cosine Wave", "Random Noise", "Combined"],
    help="Choose the mathematical pattern for simulation"
)

preset = st.sidebar.radio(
    "⚡ Volatility Presets",
    ["Custom", "Stable", "Medium Risk", "High Risk"],
    help="Quick volatility presets"
)

if preset == "Stable":
    amplitude, frequency = 5, 1
elif preset == "Medium Risk":
    amplitude, frequency = 15, 3
elif preset == "High Risk":
    amplitude, frequency = 30, 6
else: 
    amplitude, frequency = 10, 2

amplitude = st.sidebar.slider(
    "📏 Amplitude (Swing Size)", 
    1, 50, amplitude,
    help="How large the price swings will be"
)

frequency = st.sidebar.slider(
    "⏱️ Frequency (Swing Speed)", 
    1, 10, frequency,
    help="How fast the price swings occur"
)

drift = st.sidebar.slider(
    "📈 Drift (Long-Term Trend)", 
    -5, 5, 0,
    help="Long-term price trend direction"
)

shock_toggle = st.sidebar.checkbox(
    "💥 Add Market Shock",
    help="Simulate sudden market disruptions"
)

compare_mode = st.sidebar.checkbox(
    "🔁 Comparison Mode",
    help="Show stable vs volatile comparison"
)

if st.sidebar.button("🔄 Reset Settings", use_container_width=True):
    st.rerun()

st.markdown("---")

st.markdown("""
<div style="background: rgba(102, 126, 234, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <h2 style="margin: 0;">📊 Real Crypto Market Trends - {}</h2>
</div>
""".format(time_range_title), unsafe_allow_html=True)

col1, col2 = st.columns(2)


fig_close = go.Figure()
fig_close.add_trace(go.Scatter(
    x=df_filtered["Timestamp"],
    y=df_filtered["Close"],
    mode='lines',
    name='Close Price',
    line=dict(color='#667eea', width=2),
    fill='tozeroy',
    fillcolor='rgba(102, 126, 234, 0.1)'
))
fig_close.update_layout(
    title=f"Close Price Over Time ({time_range_title})",
    template="plotly_dark",
    hovermode='x unified',
    height=400,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#ffffff')
)
col1.plotly_chart(fig_close, use_container_width=True)


fig_vol = go.Figure()
fig_vol.add_trace(go.Bar(
    x=df_filtered["Timestamp"],
    y=df_filtered["Volume"],
    name='Volume',
    marker=dict(
        color=df_filtered["Volume"],
        colorscale='Viridis',
        showscale=False
    )
))
fig_vol.update_layout(
    title=f"Trading Volume ({time_range_title})",
    template="plotly_dark",
    hovermode='x unified',
    height=400,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#ffffff')
)
col2.plotly_chart(fig_vol, use_container_width=True)


st.markdown("---")
st.markdown("""
<div style="background: rgba(118, 75, 162, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <h2 style="margin: 0;">📉 Daily Volatility Range - {}</h2>
</div>
""".format(time_range_title), unsafe_allow_html=True)

fig_hl = go.Figure()
fig_hl.add_trace(go.Scatter(
    x=df_filtered["Timestamp"],
    y=df_filtered["High"],
    mode='lines',
    name='High Price',
    line=dict(color='#00ff88', width=2)
))
fig_hl.add_trace(go.Scatter(
    x=df_filtered["Timestamp"],
    y=df_filtered["Low"],
    mode='lines',
    name='Low Price',
    line=dict(color='#ff4444', width=2)
))
fig_hl.update_layout(
    title=f"High vs Low Price Comparison ({time_range_title})",
    template="plotly_dark",
    hovermode='x unified',
    height=400,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#ffffff')
)
st.plotly_chart(fig_hl, use_container_width=True)


df_filtered["Volatility_Index"] = df_filtered["High"] - df_filtered["Low"]

st.markdown("---")
st.markdown("""
<div style="background: rgba(255, 68, 68, 0.1); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <h2 style="margin: 0;">⚡ Volatility Index</h2>
</div>
""", unsafe_allow_html=True)

fig_volatility = go.Figure()
fig_volatility.add_trace(go.Scatter(
    x=df_filtered["Timestamp"],
    y=df_filtered["Volatility_Index"],
    mode='lines',
    name='Volatility Index',
    line=dict(color='#ff6b6b', width=2),
    fill='tozeroy',
    fillcolor='rgba(255, 107, 107, 0.1)'
))
fig_volatility.update_layout(
    title=f"Volatility Index ({time_range_title})",
    template="plotly_dark",
    hovermode='x unified',
    height=400,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#ffffff')
)
st.plotly_chart(fig_volatility, use_container_width=True)

st.markdown("---")
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <h2 style="margin: 0;">🎛️ Volatility Simulation Playground</h2>
</div>
""", unsafe_allow_html=True)

def simulate_price(pattern, amp, freq, drift_val, shock=False):
    t = np.linspace(0, 10, 300)
    
    if pattern == "Sine Wave":
        price = amp * np.sin(freq * t)
    elif pattern == "Cosine Wave":
        price = amp * np.cos(freq * t)
    elif pattern == "Random Noise":
        price = amp * np.random.randn(len(t))
    else:  
        price = amp * (np.sin(freq * t) + 0.5 * np.cos(2 * freq * t))
    
    price = price + drift_val * t
    
    if shock:
        shock_indices = np.random.choice(len(t), size=int(len(t) * 0.1), replace=False)
        price[shock_indices] += np.random.normal(0, amp / 2, len(shock_indices))
    
    return t, price

t, sim_price = simulate_price(pattern, amplitude, frequency, drift, shock_toggle)


volatility_color = '#00ff88' if amplitude < 10 else '#ffaa00' if amplitude < 25 else '#ff4444'

fig_sim = go.Figure()
fig_sim.add_trace(go.Scatter(
    x=t,
    y=sim_price,
    mode='lines',
    name='Simulated Price',
    line=dict(color=volatility_color, width=2),
    fill='tozeroy',
    fillcolor=f'rgba({int(volatility_color[1:3], 16)}, {int(volatility_color[3:5], 16)}, {int(volatility_color[5:7], 16)}, 0.1)'
))
fig_sim.update_layout(
    title=f"Simulated Market Swing Pattern - {pattern} (Amp: {amplitude}, Freq: {frequency}, Drift: {drift})",
    xaxis_title="Time",
    yaxis_title="Simulated Price",
    template="plotly_dark",
    hovermode='x unified',
    height=400,
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#ffffff')
)
st.plotly_chart(fig_sim, use_container_width=True)


st.markdown("---")
st.markdown("""
<div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
    <h2 style="margin: 0;">📌 Key Metrics</h2>
</div>
""", unsafe_allow_html=True)

volatility_value = np.std(sim_price)

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("💰 Average Price", f"{np.mean(sim_price):.2f}", delta=f"±{np.std(sim_price):.2f}")
col_m2.metric("⚡ Volatility Index", f"{volatility_value:.2f}", delta_color="normal")
col_m3.metric("📈 Drift Value", f"{drift}", delta="Trend")


if compare_mode:
    st.markdown("---")
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(0, 255, 136, 0.2) 0%, rgba(255, 68, 68, 0.2) 100%); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="margin: 0;">🔁 Stable vs Volatile Comparison</h2>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    t1, stable = simulate_price("Sine Wave", 5, 1, 0)
    t2, volatile = simulate_price("Sine Wave", 30, 5, 0, shock=True)

    fig_stable = go.Figure()
    fig_stable.add_trace(go.Scatter(
        x=t1, y=stable,
        mode='lines',
        name='Stable Coin',
        line=dict(color='#00ff88', width=2)
    ))
    fig_stable.update_layout(
        title="Stable Coin (Low Volatility)",
        template="plotly_dark",
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff')
    )
    c1.plotly_chart(fig_stable, use_container_width=True)

    fig_volatile = go.Figure()
    fig_volatile.add_trace(go.Scatter(
        x=t2, y=volatile,
        mode='lines',
        name='Volatile Coin',
        line=dict(color='#ff4444', width=2)
    ))
    fig_volatile.update_layout(
        title="Volatile Coin (High Volatility)",
        template="plotly_dark",
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff')
    )
    c2.plotly_chart(fig_volatile, use_container_width=True)


