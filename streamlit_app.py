import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random

# Page Configuration
st.set_page_config(
    page_title="TankVision Kenya - Inventory Dashboard",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Industrial Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }

    .stApp {
        background: #0f172a;
    }

    /* Headers */
    h1, h2, h3 { color: #f8fafc !important; font-weight: 700 !important; }
    h4, h5, h6 { color: #e2e8f0 !important; font-weight: 600 !important; }

    /* Kenyan Flag Colors Accents */
    .kenya-accent {
        background: linear-gradient(90deg, #000000 0%, #ff0000 33%, #006600 66%, #ffffff 100%);
        height: 4px;
        border-radius: 2px;
        margin-bottom: 1rem;
    }

    /* Cards */
    .css-1r6slb0, .css-1l269bu {
        background: rgba(30, 41, 59, 0.7) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }

    /* Sidebar - Darker and More Legible */
    .css-1d391kg, .css-1l02z9j, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a0f1a 0%, #050810 100%) !important;
        border-right: 2px solid rgba(0, 102, 0, 0.3) !important;
        box-shadow: 4px 0 15px rgba(0, 0, 0, 0.5) !important;
    }

    /* Sidebar text - brighter for legibility */
    [data-testid="stSidebar"] .css-1y4p8pa, 
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: #e2e8f0 !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }

    /* Radio buttons in sidebar */
    [data-testid="stSidebar"] .stRadio > label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        font-size: 11px !important;
        margin-bottom: 8px !important;
    }

    /* Radio options - more visible */
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label {
        background: rgba(30, 41, 59, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        margin-bottom: 6px !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label:hover {
        background: rgba(0, 102, 0, 0.2) !important;
        border-color: rgba(0, 102, 0, 0.5) !important;
        transform: translateX(4px);
    }

    /* Selected radio option */
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label[data-checked="true"] {
        background: rgba(0, 102, 0, 0.3) !important;
        border: 1px solid #10b981 !important;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.3) !important;
    }

    /* Radio button circle */
    [data-testid="stSidebar"] .stRadio input[type="radio"] {
        accent-color: #10b981 !important;
    }

    /* Sidebar headers */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f8fafc !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5) !important;
    }

    /* Divider in sidebar */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.15) !important;
        margin: 20px 0 !important;
    }

    /* Status indicator in sidebar */
    [data-testid="stSidebar"] .status-online,
    [data-testid="stSidebar"] .status-warning,
    [data-testid="stSidebar"] .status-critical {
        width: 10px !important;
        height: 10px !important;
        box-shadow: 0 0 8px currentColor !important;
    }

    /* Buttons */
    .stButton>button {
        background: rgba(0, 102, 0, 0.2) !important;
        color: #10b981 !important;
        border: 1px solid rgba(0, 102, 0, 0.5) !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.3s !important;
    }

    .stButton>button:hover {
        background: rgba(0, 102, 0, 0.4) !important;
        transform: translateY(-2px);
    }

    /* Metric Cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.875rem !important;
    }

    /* Status Indicators */
    .status-online { 
        display: inline-block; 
        width: 8px; 
        height: 8px; 
        background: #10b981; 
        border-radius: 50%; 
        box-shadow: 0 0 10px #10b981;
        animation: pulse 2s infinite;
    }

    .status-warning { 
        display: inline-block; 
        width: 8px; 
        height: 8px; 
        background: #f59e0b; 
        border-radius: 50%; 
        box-shadow: 0 0 10px #f59e0b;
    }

    .status-critical { 
        display: inline-block; 
        width: 8px; 
        height: 8px; 
        background: #ef4444; 
        border-radius: 50%; 
        box-shadow: 0 0 10px #ef4444;
        animation: blink 1s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.3; }
    }

    /* Alert Box */
    .alert-box {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.5rem;
    }

    .alert-warning {
        background: rgba(245, 158, 11, 0.1);
        border-left: 4px solid #f59e0b;
    }

    /* Tank Visualization */
    .tank-container {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border: 2px solid #334155;
        border-radius: 12px;
        height: 200px;
        position: relative;
        overflow: hidden;
        margin-bottom: 1rem;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(30, 41, 59, 0.7) !important;
        border-radius: 8px !important;
        color: #f8fafc !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #f8fafc !important;
    }

    /* Text */
    p, span { color: #cbd5e1 !important; }

    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.1) !important;
    }

    /* Kenyan Flag Badge */
    .ke-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(0, 102, 0, 0.2);
        border: 1px solid rgba(0, 102, 0, 0.5);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        color: #10b981;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State with Kenyan Data
if 'tanks' not in st.session_state:
    st.session_state.tanks = {
        'Mombasa Terminal': [
            {'id': 'M-101', 'name': 'Tank M-101', 'product': 'Super Petrol', 'level': 78.0, 'volume': 46800, 'temp': 28.5, 'capacity': 60000, 'status': 'normal', 'ullage': 13200},
            {'id': 'M-102', 'name': 'Tank M-102', 'product': 'Diesel', 'level': 45.0, 'volume': 27000, 'temp': 29.2, 'capacity': 60000, 'status': 'warning', 'ullage': 33000},
            {'id': 'M-103', 'name': 'Tank M-103', 'product': 'Kerosene', 'level': 92.0, 'volume': 55200, 'temp': 27.8, 'capacity': 60000, 'status': 'normal', 'ullage': 4800},
            {'id': 'M-104', 'name': 'Tank M-104', 'product': 'Jet A-1', 'level': 23.0, 'volume': 13800, 'temp': 26.5, 'capacity': 60000, 'status': 'critical', 'ullage': 46200},
        ],
        'Nairobi Storage': [
            {'id': 'N-201', 'name': 'Tank N-201', 'product': 'Super Petrol', 'level': 65.0, 'volume': 97500, 'temp': 22.3, 'capacity': 150000, 'status': 'normal', 'ullage': 52500},
            {'id': 'N-202', 'name': 'Tank N-202', 'product': 'Diesel', 'level': 82.0, 'volume': 123000, 'temp': 21.8, 'capacity': 150000, 'status': 'normal', 'ullage': 27000},
            {'id': 'N-203', 'name': 'Tank N-203', 'product': 'Kerosene', 'level': 56.0, 'volume': 33600, 'temp': 22.1, 'capacity': 60000, 'status': 'normal', 'ullage': 26400},
            {'id': 'N-204', 'name': 'Tank N-204', 'product': 'Premium Petrol', 'level': 71.0, 'volume': 42600, 'temp': 22.5, 'capacity': 60000, 'status': 'normal', 'ullage': 17400},
        ],
        'Kisumu Depot': [
            {'id': 'K-301', 'name': 'Tank K-301', 'product': 'Diesel', 'level': 34.0, 'volume': 20400, 'temp': 25.6, 'capacity': 60000, 'status': 'warning', 'ullage': 39600},
            {'id': 'K-302', 'name': 'Tank K-302', 'product': 'Super Petrol', 'level': 89.0, 'volume': 53400, 'temp': 26.2, 'capacity': 60000, 'status': 'normal', 'ullage': 6600},
            {'id': 'K-303', 'name': 'Tank K-303', 'product': 'Kerosene', 'level': 12.0, 'volume': 7200, 'temp': 25.9, 'capacity': 60000, 'status': 'critical', 'ullage': 52800},
        ],
        'Nakuru Hub': [
            {'id': 'NK-401', 'name': 'Tank NK-401', 'product': 'Diesel', 'level': 67.0, 'volume': 40200, 'temp': 20.5, 'capacity': 60000, 'status': 'normal', 'ullage': 19800},
            {'id': 'NK-402', 'name': 'Tank NK-402', 'product': 'Super Petrol', 'level': 54.0, 'volume': 32400, 'temp': 20.8, 'capacity': 60000, 'status': 'normal', 'ullage': 27600},
        ]
    }

if 'alerts' not in st.session_state:
    st.session_state.alerts = [
        {'id': 1, 'tank': 'M-104', 'site': 'Mombasa Terminal', 'type': 'critical', 'message': 'Low Jet A-1 inventory (23%) - KAA delivery required', 'time': '5 min ago'},
        {'id': 2, 'tank': 'K-303', 'site': 'Kisumu Depot', 'type': 'critical', 'message': 'Critical kerosene level (12%) - Rural supply at risk', 'time': '12 min ago'},
        {'id': 3, 'tank': 'M-102', 'site': 'Mombasa Terminal', 'type': 'warning', 'message': 'Diesel below reorder point (45%)', 'time': '1 hour ago'},
        {'id': 4, 'tank': 'K-301', 'site': 'Kisumu Depot', 'type': 'warning', 'message': 'Western Kenya diesel stocks low (34%)', 'time': '2 hours ago'},
    ]

if 'history' not in st.session_state:
    st.session_state.history = {}
    for site, tanks in st.session_state.tanks.items():
        for tank in tanks:
            st.session_state.history[tank['id']] = {
                'timestamps': [(datetime.now() - timedelta(hours=i)).strftime('%H:%M') for i in range(24, 0, -1)],
                'levels': [tank['level'] + random.uniform(-5, 5) for _ in range(24)]
            }

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 2rem;">
        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #006600, #000000); 
                    border-radius: 8px; display: flex; align-items: center; justify-content: center;
                    border: 2px solid #ff0000;">
            <span style="color: white; font-size: 20px;">🛢️</span>
        </div>
        <div>
            <h3 style="margin: 0; color: #f8fafc;">TankVision KE</h3>
            <p style="margin: 0; color: #64748b; font-size: 12px;">Kenya National Fuel Control</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='kenya-accent'></div>", unsafe_allow_html=True)

    # Navigation
    st.markdown("<p style='color: #64748b; font-size: 12px; font-weight: 600; letter-spacing: 0.05em;'>NAVIGATION</p>", unsafe_allow_html=True)

    page = st.radio(
        "",
        ["📊 Dashboard", "🗺️ County Map", "⚠️ Alerts", "📈 Analytics", "⚙️ Settings"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    # System Status
    st.markdown("<p style='color: #64748b; font-size: 12px; font-weight: 600; letter-spacing: 0.05em;'>SYSTEM STATUS</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("<span class='status-online'></span>", unsafe_allow_html=True)
    with col2:
        st.markdown("<span style='color: #10b981; font-size: 14px;'>System Online</span>", unsafe_allow_html=True)

    st.markdown(f"<p style='color: #64748b; font-size: 12px; margin-top: 8px;'>Last sync: {datetime.now().strftime('%H:%M:%S')} EAT</p>", unsafe_allow_html=True)

    st.markdown("---")

    # Kenyan Context Info
    st.markdown("""
    <div style="background: rgba(0, 102, 0, 0.1); border: 1px solid rgba(0, 102, 0, 0.3); 
                border-radius: 8px; padding: 12px; margin-top: 1rem;">
        <p style="margin: 0; color: #10b981; font-size: 12px; font-weight: 600;">🇰🇪 KENYA OPERATIONS</p>
        <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 11px;">
            EPRA Compliant<br>
            KPC Integration Ready<br>
            4 Counties Active
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # User Profile
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-top: 2rem;">
        <div style="width: 36px; height: 36px; background: linear-gradient(135deg, #006600, #000000); 
                    border-radius: 50%; display: flex; align-items: center; justify-content: center;
                    border: 2px solid #ff0000;">
            <span style="color: white;">👤</span>
        </div>
        <div>
            <p style="margin: 0; color: #f8fafc; font-weight: 500; font-size: 14px;">Operations Manager</p>
            <p style="margin: 0; color: #64748b; font-size: 12px;">EPRA Licensed</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main Content
if page == "📊 Dashboard":
    # Header
    col1, col2, col3 = st.columns([3, 2, 2])
    with col1:
        st.title("Kenya National Fuel Control Center")
        st.markdown("<p style='color: #64748b; margin-top: -10px;'>🇰🇪 Monitoring strategic petroleum reserves across Kenya</p>", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 8px; 
                    background: rgba(0, 102, 0, 0.2); border: 1px solid rgba(0, 102, 0, 0.5);
                    padding: 8px 16px; border-radius: 20px; margin-top: 12px;">
            <span style="color: #10b981;">●</span>
            <span style="color: #10b981; font-weight: 500; font-size: 14px;">Live EAT (UTC+3)</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        site_filter = st.selectbox("Select Depot", ["All Depots", "Mombasa Terminal", "Nairobi Storage", "Kisumu Depot", "Nakuru Hub"], label_visibility="collapsed")

    st.markdown("---")

    # KPI Cards
    st.markdown("<h3 style='margin-bottom: 1rem;'>National Fuel Reserves</h3>", unsafe_allow_html=True)

    # Calculate totals
    total_volume = sum(tank['volume'] for site in st.session_state.tanks.values() for tank in site)
    total_capacity = sum(tank['capacity'] for site in st.session_state.tanks.values() for tank in site)
    active_tanks = sum(len(site) for site in st.session_state.tanks.values())
    active_alerts = len(st.session_state.alerts)
    avg_temp = np.mean([tank['temp'] for site in st.session_state.tanks.values() for tank in site])

    # Kenyan currency conversion (approximate)
    fuel_value_kes = total_volume * 120  # Assuming avg 120 KES per liter

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Inventory",
            value=f"{total_volume/1_000_000:.1f}M L",
            delta=f"{total_volume/total_capacity*100:.1f}% capacity"
        )
    with col2:
        st.metric(
            label="Strategic Tanks",
            value=f"{active_tanks}",
            delta="4 counties"
        )
    with col3:
        st.metric(
            label="Active Alerts",
            value=f"{active_alerts}",
            delta="Requires attention" if active_alerts > 0 else "All clear",
            delta_color="inverse"
        )
    with col4:
        st.metric(
            label="Avg Temperature",
            value=f"{avg_temp:.1f}°C",
            delta="Coastal: Hot | Highland: Cool"
        )

    st.markdown("---")

    # Tank Grid
    st.markdown("<h3 style='margin-bottom: 1rem;'>Depot Tank Status</h3>", unsafe_allow_html=True)

    # Filter tanks based on selection
    display_tanks = []
    if site_filter == "All Depots":
        for site_name, tanks in st.session_state.tanks.items():
            for tank in tanks:
                display_tanks.append({**tank, 'site': site_name})
    else:
        for tank in st.session_state.tanks[site_filter]:
            display_tanks.append({**tank, 'site': site_filter})

    # Display tanks in grid
    cols = st.columns(2)
    for idx, tank in enumerate(display_tanks):
        with cols[idx % 2]:
            with st.expander(f"**{tank['name']}** - {tank['site']} ({tank['level']:.1f}%)", expanded=True):
                # Status indicator
                status_color = {"normal": "#10b981", "warning": "#f59e0b", "critical": "#ef4444"}[tank['status']]
                status_class = {"normal": "status-online", "warning": "status-warning", "critical": "status-critical"}[tank['status']]

                col1, col2 = st.columns([1, 4])
                with col1:
                    st.markdown(f"<span class='{status_class}'></span>", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"<span style='color: {status_color}; font-weight: 600; text-transform: uppercase; font-size: 12px;'>{tank['status']}</span>", unsafe_allow_html=True)

                # Tank Visualization using Plotly
                fig = go.Figure()

                # Tank background
                fig.add_shape(
                    type="rect", x0=0, y0=0, x1=1, y1=1,
                    fillcolor="rgba(30, 41, 59, 0.5)", line=dict(color="#334155", width=2)
                )

                # Liquid level
                fig.add_shape(
                    type="rect", x0=0, y0=0, x1=1, y1=tank['level']/100,
                    fillcolor=status_color, opacity=0.8,
                    line=dict(width=0)
                )

                # Level text
                fig.add_annotation(
                    x=0.5, y=tank['level']/200,
                    text=f"<b>{tank['level']:.1f}%</b>",
                    showarrow=False, font=dict(size=24, color="white")
                )

                fig.update_layout(
                    height=150, margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    xaxis=dict(visible=False, range=[0, 1]),
                    yaxis=dict(visible=False, range=[0, 1])
                )

                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

                # Tank details
                det_col1, det_col2, det_col3 = st.columns(3)
                with det_col1:
                    st.markdown(f"<p style='text-align: center; margin: 0;'><span style='color: #60a5fa; font-weight: 700; font-size: 18px;'>{tank['volume']:,}</span></p><p style='text-align: center; margin: 0; color: #64748b; font-size: 12px;'>Liters</p>", unsafe_allow_html=True)
                with det_col2:
                    st.markdown(f"<p style='text-align: center; margin: 0;'><span style='color: #a78bfa; font-weight: 700; font-size: 18px;'>{tank['temp']}°C</span></p><p style='text-align: center; margin: 0; color: #64748b; font-size: 12px;'>Temperature</p>", unsafe_allow_html=True)
                with det_col3:
                    st.markdown(f"<p style='text-align: center; margin: 0;'><span style='color: #38bdf8; font-weight: 700; font-size: 18px;'>{tank['ullage']:,}</span></p><p style='text-align: center; margin: 0; color: #64748b; font-size: 12px;'>Ullage (L)</p>", unsafe_allow_html=True)

                # Kenyan fuel type badge
                fuel_colors = {
                    'Super Petrol': '#ef4444',
                    'Premium Petrol': '#f97316',
                    'Diesel': '#f59e0b',
                    'Kerosene': '#3b82f6',
                    'Jet A-1': '#8b5cf6'
                }
                fuel_color = fuel_colors.get(tank['product'], '#10b981')

                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                    <span style="background: {fuel_color}20; border: 1px solid {fuel_color}50; 
                                color: {fuel_color}; padding: 2px 8px; border-radius: 4px; 
                                font-size: 11px; font-weight: 600;">
                        {tank['product']}
                    </span>
                    <span style="color: #64748b; font-size: 12px;">Capacity: {tank['capacity']:,} L</span>
                </div>
                """, unsafe_allow_html=True)

    # Trend Chart - Kenyan context
    st.markdown("---")
    st.markdown("<h3 style='margin-bottom: 1rem;'>Volume Trends - Mombasa Terminal (KPA Supply Point)</h3>", unsafe_allow_html=True)

    # Create trend data showing Kenyan supply patterns
    hours = list(range(24))
    # Simulate higher volumes during day (trucks loading)
    petrol_trend = [45000 + 2000*np.sin((h-8)*np.pi/12) + random.uniform(-1000, 1000) for h in hours]
    diesel_trend = [38000 + 1500*np.sin((h-6)*np.pi/12) + random.uniform(-800, 800) for h in hours]

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=hours, y=petrol_trend, name='Super Petrol',
        fill='tonexty', mode='lines', line=dict(color='#ef4444', width=2),
        fillcolor='rgba(239, 68, 68, 0.1)'
    ))
    fig_trend.add_trace(go.Scatter(
        x=hours, y=diesel_trend, name='Diesel',
        fill='tonexty', mode='lines', line=dict(color='#f59e0b', width=2),
        fillcolor='rgba(245, 158, 11, 0.1)'
    ))

    fig_trend.update_layout(
        height=300,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30, 41, 59, 0.5)",
        font=dict(color="#94a3b8"),
        xaxis=dict(title="Hour of Day (EAT)", gridcolor="rgba(255,255,255,0.1)", zeroline=False),
        yaxis=dict(title="Volume (L)", gridcolor="rgba(255,255,255,0.1)", zeroline=False),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=60, r=20, t=40, b=40)
    )

    st.plotly_chart(fig_trend, use_container_width=True)

elif page == "🗺️ County Map":
    st.title("Kenya County Depots Map")
    st.markdown("<p style='color: #64748b;'>Strategic petroleum storage facilities across Kenyan counties</p>", unsafe_allow_html=True)

    # Kenyan coordinates (approximate for major towns)
    sites_data = {
        'Mombasa Terminal': {'lat': -4.0435, 'lon': 39.6682, 'tanks': 4, 'status': 'Operational', 'county': 'Mombasa', 'role': 'Import/Export Hub'},
        'Nairobi Storage': {'lat': -1.2921, 'lon': 36.8219, 'tanks': 4, 'status': 'Operational', 'county': 'Nairobi', 'role': 'National Distribution'},
        'Kisumu Depot': {'lat': -0.1022, 'lon': 34.7617, 'tanks': 3, 'status': 'Warning', 'county': 'Kisumu', 'role': 'Western Kenya Supply'},
        'Nakuru Hub': {'lat': -0.3031, 'lon': 36.0800, 'tanks': 2, 'status': 'Operational', 'county': 'Nakuru', 'role': 'Rift Valley Distribution'}
    }

    col1, col2 = st.columns([2, 1])

    with col1:
        # Map using plotly - Kenya focused
        fig_map = go.Figure()

        for site, data in sites_data.items():
            color = "#10b981" if data['status'] == 'Operational' else "#f59e0b"
            fig_map.add_trace(go.Scattergeo(
                lon=[data['lon']], lat=[data['lat']],
                mode='markers+text',
                marker=dict(size=20, color=color, symbol='circle', 
                           line=dict(width=2, color='white')),
                text=[site],
                textposition="top center",
                textfont=dict(color="white", size=10),
                name=f"{site} ({data['tanks']} tanks)",
                hovertext=f"<b>{site}</b><br>County: {data['county']}<br>{data['tanks']} tanks<br>Status: {data['status']}<br>Role: {data['role']}",
                hoverinfo='text'
            ))

        # Kenya bounds
        fig_map.update_layout(
            geo=dict(
                scope='africa',
                projection=dict(type='mercator'),
                center=dict(lat=0.5, lon=38),
                lonaxis=dict(range=[33, 42]),
                lataxis=dict(range=[-5, 5]),
                showland=True, landcolor="rgba(30, 41, 59, 0.8)",
                showocean=True, oceancolor="rgba(15, 23, 42, 1)",
                showlakes=True, lakecolor="rgba(59, 130, 246, 0.2)",
                showcountries=True, countrycolor="rgba(255,255,255,0.2)",
                showsubunits=True, subunitcolor="rgba(255,255,255,0.1)",
                bgcolor="rgba(0,0,0,0)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f8fafc"),
            height=600,
            margin=dict(l=0, r=0, t=0, b=0),
            legend=dict(
                yanchor="top", y=0.99, xanchor="left", x=0.01,
                bgcolor="rgba(30, 41, 59, 0.8)", bordercolor="rgba(255,255,255,0.1)", borderwidth=1
            )
        )

        st.plotly_chart(fig_map, use_container_width=True)

    with col2:
        st.markdown("<h4 style='margin-bottom: 1rem;'>Depot Summary</h4>", unsafe_allow_html=True)

        for site, data in sites_data.items():
            status_color = "#10b981" if data['status'] == 'Operational' else "#f59e0b"
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.1); 
                        border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
                <h5 style="margin: 0 0 0.5rem 0; color: #f8fafc;">{site}</h5>
                <p style="margin: 0; color: #64748b; font-size: 12px;">
                    📍 {data['county']} County<br>
                    <span style="color: {status_color};">●</span> {data['status']}<br>
                    🛢️ {data['tanks']} Active Tanks<br>
                    🚛 {data['role']}
                </p>
            </div>
            """, unsafe_allow_html=True)

        # Kenya specific stats
        st.markdown("---")
        st.markdown("""
        <div style="background: rgba(0, 102, 0, 0.1); border: 1px solid rgba(0, 102, 0, 0.3); 
                    border-radius: 8px; padding: 1rem;">
            <h5 style="margin: 0 0 0.5rem 0; color: #10b981;">🇰🇪 National Coverage</h5>
            <p style="margin: 0; color: #94a3b8; font-size: 12px;">
                <b>4</b> Strategic Depots<br>
                <b>13</b> Storage Tanks<br>
                <b>516,000</b> Liters Total Capacity<br>
                <b>47</b> Counties Served
            </p>
        </div>
        """, unsafe_allow_html=True)

elif page == "⚠️ Alerts":
    st.title("EPRA Compliance Alerts")
    st.markdown("<p style='color: #64748b;'>Critical fuel security and safety notifications</p>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Alerts", use_container_width=True):
            st.rerun()

    st.markdown("---")

    # Alert categories
    alert_tabs = st.tabs(["🔴 Critical (2)", "⚠️ Warnings (2)", "✅ Resolved Today (5)"])

    with alert_tabs[0]:
        for alert in [a for a in st.session_state.alerts if a['type'] == 'critical']:
            st.markdown(f"""
            <div class="alert-box">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h4 style="margin: 0 0 0.5rem 0; color: #ef4444;">
                            🔴 {alert['tank']} - {alert['site']}
                        </h4>
                        <p style="margin: 0; color: #cbd5e1; font-size: 14px;">{alert['message']}</p>
                        <p style="margin: 0.5rem 0 0 0; color: #64748b; font-size: 12px;">⏰ {alert['time']} EAT</p>
                    </div>
                    <button style="background: rgba(239, 68, 68, 0.2); 
                                   border: 1px solid rgba(239, 68, 68, 0.5); 
                                   color: #ef4444; padding: 4px 12px; 
                                   border-radius: 4px; cursor: pointer; font-size: 12px;">
                        Dispatch Truck
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with alert_tabs[1]:
        for alert in [a for a in st.session_state.alerts if a['type'] == 'warning']:
            st.markdown(f"""
            <div class="alert-box alert-warning">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div>
                        <h4 style="margin: 0 0 0.5rem 0; color: #f59e0b;">
                            ⚠️ {alert['tank']} - {alert['site']}
                        </h4>
                        <p style="margin: 0; color: #cbd5e1; font-size: 14px;">{alert['message']}</p>
                        <p style="margin: 0.5rem 0 0 0; color: #64748b; font-size: 12px;">⏰ {alert['time']} EAT</p>
                    </div>
                    <button style="background: rgba(245, 158, 11, 0.2); 
                                   border: 1px solid rgba(245, 158, 11, 0.5); 
                                   color: #f59e0b; padding: 4px 12px; 
                                   border-radius: 4px; cursor: pointer; font-size: 12px;">
                        Schedule Delivery
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with alert_tabs[2]:
        resolved = [
            {"tank": "N-201", "site": "Nairobi Storage", "message": "Refilled to 85% - Supply normalized", "time": "08:30"},
            {"tank": "M-103", "site": "Mombasa Terminal", "message": "Kerosene delivery received", "time": "10:15"},
            {"tank": "NK-401", "site": "Nakuru Hub", "message": "Temperature alarm cleared", "time": "11:45"},
            {"tank": "K-302", "site": "Kisumu Depot", "message": "Quality test passed - EPRA compliant", "time": "13:20"},
            {"tank": "N-204", "site": "Nairobi Storage", "message": "Leak test completed - No issues", "time": "15:00"},
        ]
        for item in resolved:
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; 
                        padding: 1rem; border-radius: 0 8px 8px 0; margin-bottom: 0.5rem;">
                <h4 style="margin: 0 0 0.5rem 0; color: #10b981;">✅ {item['tank']} - {item['site']}</h4>
                <p style="margin: 0; color: #cbd5e1; font-size: 14px;">{item['message']}</p>
                <p style="margin: 0.5rem 0 0 0; color: #64748b; font-size: 12px;">⏰ {item['time']} EAT</p>
            </div>
            """, unsafe_allow_html=True)

    # Alert Statistics
    st.markdown("---")
    st.markdown("<h3 style='margin-bottom: 1rem;'>Alert Statistics (24h)</h3>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Critical Alerts", 2, delta="High Priority")
    with col2:
        st.metric("Warnings", 2, delta="Monitor")
    with col3:
        st.metric("Resolved", 5, delta="-2 from yesterday")
    with col4:
        st.metric("Avg Response", "45 min", delta="Fast")

elif page == "📈 Analytics":
    st.title("Kenya Fuel Analytics")
    st.markdown("<p style='color: #64748b;'>Strategic petroleum reserve analysis and forecasting</p>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Volume History", "Temperature Analysis", "County Efficiency"])

    with tab1:
        st.markdown("<h4 style='margin-bottom: 1rem;'>24-Hour Volume History by Depot</h4>", unsafe_allow_html=True)

        # Generate historical data with Kenyan patterns
        timestamps = pd.date_range(end=datetime.now(), periods=24, freq='H')

        fig = go.Figure()
        colors = ['#ef4444', '#f59e0b', '#3b82f6', '#10b981']

        for idx, (site, tanks) in enumerate(st.session_state.tanks.items()):
            total_vol = sum(t['volume'] for t in tanks)
            # Add Kenyan demand patterns (higher during day, lower at night)
            base_pattern = [total_vol + 5000*np.sin((i-8)*np.pi/12) for i in range(24)]
            noise = [random.uniform(-3000, 3000) for _ in range(24)]
            history = [b + n for b, n in zip(base_pattern, noise)]

            fig.add_trace(go.Scatter(
                x=timestamps, y=history, name=site,
                mode='lines', line=dict(color=colors[idx], width=2),
                fill='tonexty' if idx == 0 else None,
                fillcolor=f'rgba{tuple(list(int(colors[idx].lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + [0.1])}'
            ))

        fig.update_layout(
            height=400,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30, 41, 59, 0.5)",
            font=dict(color="#94a3b8"),
            xaxis=dict(title="Time (EAT)", gridcolor="rgba(255,255,255,0.1)"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)", title="Volume (L)"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Kenyan context note
        st.info("📊 **Note:** Higher volumes during daytime (06:00-18:00) correspond to peak truck loading hours at KPC facilities.")

    with tab2:
        st.markdown("<h4 style='margin-bottom: 1rem;'>Temperature Monitoring by Climate Zone</h4>", unsafe_allow_html=True)

        # Group by climate zone
        coastal_temps = [t['temp'] for site, tanks in st.session_state.tanks.items() 
                        for t in tanks if site == 'Mombasa Terminal']
        highland_temps = [t['temp'] for site, tanks in st.session_state.tanks.items() 
                         for t in tanks if site in ['Nairobi Storage', 'Nakuru Hub']]
        lakeside_temps = [t['temp'] for site, tanks in st.session_state.tanks.items() 
                         for t in tanks if site == 'Kisumu Depot']

        zones = ['Coastal (Mombasa)', 'Highland (Nairobi/Nakuru)', 'Lakeside (Kisumu)']
        avg_temps = [np.mean(coastal_temps), np.mean(highland_temps), np.mean(lakeside_temps)]

        fig_temp = go.Figure()
        fig_temp.add_trace(go.Bar(
            x=zones, y=avg_temps,
            marker=dict(
                color=avg_temps,
                colorscale=[[0, '#3b82f6'], [0.5, '#10b981'], [1, '#ef4444']],
                showscale=True,
                colorbar=dict(title="°C")
            )
        ))

        fig_temp.update_layout(
            height=400,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(30, 41, 59, 0.5)",
            font=dict(color="#94a3b8"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.1)", title="Climate Zone"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.1)", title="Avg Temperature (°C)", range=[15, 35]),
        )

        st.plotly_chart(fig_temp, use_container_width=True)

        st.warning("🌡️ **Alert:** Mombasa coastal temperatures averaging 28°C+ require enhanced vapor recovery monitoring per EPRA regulations.")

    with tab3:
        st.markdown("<h4 style='margin-bottom: 1rem;'>County Depot Efficiency Report</h4>", unsafe_allow_html=True)

        efficiency_data = []
        for site, tanks in st.session_state.tanks.items():
            avg_level = np.mean([t['level'] for t in tanks])
            capacity_util = sum(t['volume'] for t in tanks) / sum(t['capacity'] for t in tanks) * 100

            # Kenyan efficiency rating
            if capacity_util > 80:
                rating = "⭐⭐⭐ Optimal"
            elif capacity_util > 50:
                rating = "⭐⭐ Good"
            else:
                rating = "⭐ Needs Attention"

            # County mapping
            county_map = {
                'Mombasa Terminal': 'Mombasa',
                'Nairobi Storage': 'Nairobi',
                'Kisumu Depot': 'Kisumu',
                'Nakuru Hub': 'Nakuru'
            }

            efficiency_data.append({
                'County': county_map[site],
                'Facility': site,
                'Fill Level': f"{avg_level:.1f}%",
                'Capacity Util': f"{capacity_util:.1f}%",
                'Tanks': len(tanks),
                'Rating': rating
            })

        df_eff = pd.DataFrame(efficiency_data)
        st.dataframe(df_eff, use_container_width=True, hide_index=True)

        # Kenyan recommendation
        st.success("✅ **Recommendation:** Kisumu Depot showing low utilization (34% avg). Consider diverting Western Kenya supply from Nairobi to optimize logistics costs.")

elif page == "⚙️ Settings":
    st.title("System Configuration")
    st.markdown("<p style='color: #64748b;'>EPRA compliance and operational settings</p>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h4 style='margin-bottom: 1rem;'>Alert Configuration</h4>", unsafe_allow_html=True)

        st.slider("Critical Alert Threshold (%)", 0, 50, 20, 
                 help="Trigger when tank falls below this level (EPRA minimum reserve requirement)")
        st.slider("Warning Alert Threshold (%)", 20, 70, 45, 
                 help="Trigger warning for reorder planning")

        st.checkbox("Enable EPRA Regulatory Alerts", value=True)
        st.checkbox("Enable KPC Pipeline Integration", value=True)
        st.checkbox("SMS Alerts to County Officers", value=True)
        st.checkbox("Auto-generate EPRA Daily Returns", value=True)

    with col2:
        st.markdown("<h4 style='margin-bottom: 1rem;'>Kenya-Specific Settings</h4>", unsafe_allow_html=True)

        st.selectbox("Currency", ["Kenyan Shillings (KES)", "US Dollars (USD)", "Uganda Shillings (UGX)"])
        st.selectbox("Volume Unit", ["Liters (L)", "Cubic Meters (m³)", "Barrels (bbl)"])
        st.selectbox("Temperature Unit", ["Celsius (°C)", "Fahrenheit (°F)"])
        st.selectbox("Timezone", ["East Africa Time (EAT, UTC+3)", "UTC"])

        st.selectbox("Language", ["English", "Kiswahili", "Both"])

        st.checkbox("Show EPRA License Number", value=True)
        st.checkbox("Enable KRA Excise Integration", value=False)

    st.markdown("---")

    col3, col4 = st.columns(2)
    with col3:
        if st.button("💾 Save Configuration", use_container_width=True):
            st.success("✅ Settings saved to EPRA compliance database!")

    with col4:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            st.info("ℹ️ Settings reset to Kenya Petroleum Regulatory defaults")

    st.markdown("---")

    # Kenyan regulatory info
    st.markdown("""
    <div style="background: rgba(0, 102, 0, 0.1); border: 1px solid rgba(0, 102, 0, 0.3); 
                border-radius: 8px; padding: 1rem;">
        <h4 style="margin: 0 0 0.5rem 0; color: #10b981;">🇰🇪 Regulatory Compliance</h4>
        <p style="margin: 0; color: #94a3b8; font-size: 12px;">
            <b>EPRA License:</b> EPRA/OPS/2024/001<br>
            <b>KPC Agreement:</b> KPC/TSC/2024/089<br>
            <b>Last Audit:</b> 15 February 2024<br>
            <b>Next Inspection:</b> 15 May 2024<br>
            <b>Compliance Status:</b> <span style="color: #10b981;">✅ Fully Compliant</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

# Auto-refresh simulation (every 5 seconds)
if 'last_update' not in st.session_state:
    st.session_state.last_update = time.time()

if time.time() - st.session_state.last_update > 5:
    # Simulate small random changes in tank levels
    for site in st.session_state.tanks.values():
        for tank in site:
            change = random.uniform(-0.5, 0.5)
            tank['level'] = max(0, min(100, tank['level'] + change))
            tank['volume'] = int((tank['level'] / 100) * tank['capacity'])
            tank['ullage'] = tank['capacity'] - tank['volume']

    st.session_state.last_update = time.time()
    st.rerun()