import sys
from pathlib import Path
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import inspect
import plotly.express as px
import time

# ------------------ PATH FIX ------------------
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

try:
    from services.api_client import (
        get_current_aqi,
        get_cities,
        get_last_24_hours_aqi
    )
except ImportError:
    def get_cities(): return ["Delhi", "Mumbai", "Ahmedabad", "Kolkata", "Chennai", "Bengaluru"]
    def get_current_aqi(city): return None
    def get_last_24_hours_aqi(city): return []

@st.cache_data(ttl=300)  # cache for 5 minutes
def cached_current_aqi(city):
    return get_current_aqi(city)

@st.cache_data(ttl=600)  # cache for 10 minutes
def cached_last_24_hours(city):
    return get_last_24_hours_aqi(city)

# ------------------ ENHANCED LOGIC FUNCTIONS ------------------

def get_safety_advice(aqi):
    """Actionable health advice with Safe Outdoor Windows."""
    advice = {
        1: {
            "title": "Clean Air - Safe",
            "desc": "Air quality is ideal for all outdoor activities.",
            "steps": ["Perfect for outdoor exercise", "Safe for children and elderly", "Open windows for fresh air"],
            "color": "#22c55e",
            "safe_window": "Unlimited",
            "risk_level": "Low",
            "icon": "check-circle"
        },
        2: {
            "title": "Fair - Low Risk",
            "desc": "Air quality is acceptable; no special precautions needed.",
            "steps": ["Regular activity is fine", "Ventilation is safe", "No risk for sensitive groups"],
            "color": "#84cc16",
            "safe_window": "4 - 6 Hours",
            "risk_level": "Minor",
            "icon": "check-circle"
        },
        3: {
            "title": "Moderate - Warning",
            "desc": "Sensitive individuals may experience slight health effects.",
            "steps": ["Sensitive groups should wear masks", "Reduce heavy outdoor exertion", "Close windows if you feel irritation"],
            "color": "#eab308",
            "safe_window": "1 - 2 Hours",
            "risk_level": "Moderate",
            "icon": "alert-triangle"
        },
        4: {
            "title": "Poor - Unhealthy",
            "desc": "Everyone may begin to experience health effects.",
            "steps": ["Avoid outdoor cardio exercise", "Wear N95 masks outdoors", "Use indoor air purifiers"],
            "color": "#f97316",
            "safe_window": "30 Minutes",
            "risk_level": "High",
            "icon": "alert-circle"
        },
        5: {
            "title": "Very Poor - Hazardous",
            "desc": "Health warnings for emergency conditions.",
            "steps": ["Stay indoors strictly", "Keep all windows shut", "High-grade masks mandatory"],
            "color": "#ef4444",
            "safe_window": "Avoid Exposure",
            "risk_level": "Severe",
            "icon": "alert-octagon"
        }
    }
    return advice.get(aqi, advice[3])

def get_aqi_theme(aqi):
    """Visual theme with background colors for glassmorphism."""
    themes = {
        1: {"label": "GOOD", "color": "#22c55e", "bg_color": "rgba(34, 197, 94, 0.1)"},
        2: {"label": "FAIR", "color": "#84cc16", "bg_color": "rgba(132, 204, 22, 0.1)"},
        3: {"label": "MODERATE", "color": "#eab308", "bg_color": "rgba(234, 179, 8, 0.1)"},
        4: {"label": "POOR", "color": "#f97316", "bg_color": "rgba(249, 115, 22, 0.1)"},
        5: {"label": "VERY POOR", "color": "#ef4444", "bg_color": "rgba(239, 68, 68, 0.1)"}
    }
    return themes.get(aqi, {"label": "UNKNOWN", "color": "#64748b", "bg_color": "rgba(100, 116, 139, 0.1)"})

def format_timestamp(ts_string):
    try:
        dt = datetime.fromisoformat(str(ts_string).replace('Z', '+00:00'))
        return dt.strftime("%b %d, %Y • %I:%M %p")
    except:
        return ts_string

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="SkyGuard | Analytics", page_icon="🌍", layout="wide")

# ------------------ ENHANCED PROFESSIONAL STYLING ------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: -0.01em;
    }
    
    .stApp { 
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        color: #f1f5f9; 
    }
    
    #MainMenu, footer, header {display: none;}

    /* Professional Dashboard Header */
    .dashboard-header {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%);
        backdrop-filter: blur(20px);
        padding: 3rem;
        border-radius: 24px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #60a5fa, transparent);
    }

    /* Professional Safety Card */
    .safety-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.4) 100%);
        backdrop-filter: blur(16px);
        padding: 2rem;
        border-radius: 20px;
        border-left: 4px solid;
        margin-bottom: 2rem;
        border-right: 1px solid rgba(148, 163, 184, 0.05);
        border-top: 1px solid rgba(148, 163, 184, 0.05);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    .safety-card ul {
        list-style: none;
        padding-left: 0;
        margin-top: 1rem;
    }
    
    .safety-card li {
        padding: 0.75rem 0;
        padding-left: 2rem;
        position: relative;
        color: #cbd5e1;
        line-height: 1.6;
        border-bottom: 1px solid rgba(148, 163, 184, 0.05);
    }
    
    .safety-card li:last-child {
        border-bottom: none;
    }
    
    .safety-card li::before {
        content: '→';
        position: absolute;
        left: 0.5rem;
        color: #60a5fa;
        font-weight: 700;
    }

    /* City Title */
    .city-title {
        font-size: 2.75rem;
        font-weight: 800;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }
    
    /* Section Headers */
    .section-head {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 3rem 0 1.5rem 0;
        padding-left: 1.5rem;
        position: relative;
    }
    
    .section-head::before {
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 4px;
        height: 70%;
        background: linear-gradient(180deg, #3b82f6, #60a5fa);
        border-radius: 2px;
    }
    
    /* Instruction Box */
    .instruction-text {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1) 0%, rgba(96, 165, 250, 0.05) 100%);
        color: #93c5fd;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-left: 3px solid #3b82f6;
    }

    /* Medical Cards Grid */
    .med-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .med-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.3) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.08);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border-left: 3px solid;
        position: relative;
        overflow: hidden;
    }
    
    .med-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, transparent 0%, rgba(255, 255, 255, 0.02) 100%);
        opacity: 0;
        transition: opacity 0.4s;
    }
    
    .med-card:hover {
        transform: translateY(-8px);
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.5) 100%);
        border-color: rgba(96, 165, 250, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .med-card:hover::before {
        opacity: 1;
    }
    
    .med-title {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }
    
    .med-desc {
        color: #cbd5e1;
        font-size: 0.9rem;
        line-height: 1.7;
        font-weight: 400;
    }
    
    .med-desc b {
        color: #f1f5f9;
        font-weight: 600;
    }

    /* Status Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1.25rem;
        border-radius: 24px;
        font-weight: 700;
        font-size: 0.85rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        border: 1.5px solid;
    }

    /* Safe Window Card */
    .safe-window-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(37, 99, 235, 0.05) 100%);
        border: 1px solid rgba(59, 130, 246, 0.15);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        backdrop-filter: blur(12px);
    }
    
    .safe-window-label {
        color: #93c5fd;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 1rem;
    }
    
    .safe-window-value {
        font-size: 2.25rem;
        font-weight: 800;
        color: #f8fafc;
        margin: 1rem 0;
        letter-spacing: -0.02em;
    }
    
    .risk-badge {
        background: rgba(96, 165, 250, 0.15);
        color: #60a5fa;
        font-size: 0.7rem;
        padding: 0.5rem 1rem;
        border-radius: 12px;
        display: inline-block;
        font-weight: 700;
        letter-spacing: 0.05em;
        border: 1px solid rgba(96, 165, 250, 0.2);
    }

    /* Sync Time */
    .sync-time {
        color: #64748b;
        font-size: 0.8rem;
        font-weight: 500;
        letter-spacing: 0.02em;
    }

    /* AQI Display */
    .aqi-display {
        font-size: 5rem;
        font-weight: 900;
        line-height: 1;
        margin: 1.5rem 0;
        letter-spacing: -0.03em;
    }
    
    .aqi-label {
        font-size: 1.1rem;
        color: #94a3b8;
        vertical-align: middle;
        font-weight: 500;
        margin-left: 0.5rem;
    }

    /* Button Enhancements */
    .stButton > button {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.6) 100%);
        color: #e2e8f0;
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        backdrop-filter: blur(8px);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.15) 100%);
        border-color: rgba(96, 165, 250, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);
    }

    /* Metric Cards */
    .stMetric {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.2) 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.08);
        backdrop-filter: blur(8px);
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.3) 100%);
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        font-weight: 600;
    }

    /* Footer */
    .footer-container {
        text-align: center;
        padding: 4rem 2rem;
        margin-top: 6rem;
        border-top: 1px solid rgba(148, 163, 184, 0.08);
        background: linear-gradient(to bottom, rgba(2, 6, 23, 0), rgba(15, 23, 42, 0.4));
    }
    
    .footer-logo {
        font-size: 1.3rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }
    
    .footer-logo span {
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .footer-credits {
        color: #475569;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ TOP NAV ------------------
nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([5, 1.5, 1.5, 1.5])

with nav_col1:
    st.markdown(
        "### SkyGuard <span style='color:#60a5fa'>Analytics</span>",
        unsafe_allow_html=True
    )

with nav_col2:
    if st.button("Home", use_container_width=True):
        st.switch_page("Home.py")

with nav_col3:
    if st.button("What is AQI?", use_container_width=True):
        st.switch_page("pages/About.py")

with nav_col4:
    if st.button("Contact", use_container_width=True):
        st.switch_page("pages/Contact.py")

# ------------------ CITY SELECTION ------------------
st.markdown('<div class="instruction-text"><b>Quick Tip:</b> Choose a station to view real-time health intelligence and safe outdoor windows.</div>', unsafe_allow_html=True)

cities = get_cities()
if 'selected_city' not in st.session_state:
    st.session_state.selected_city = cities[0]
    st.session_state.city_loading = False

# Initialize loading state flag
if 'city_loading' not in st.session_state:
    st.session_state.city_loading = False

city_cols = st.columns(len(cities))
for idx, city_name in enumerate(cities):
    if city_cols[idx].button(city_name, use_container_width=True):
        st.session_state.selected_city = city_name
        st.session_state.city_loading = True
        st.rerun()

selected_city = st.session_state.selected_city

# ------------------ LOADING ANIMATION FOR CITY CHANGE ------------------
if st.session_state.get('city_loading', False):
    placeholder = st.empty()
    
    status_messages = [
        f"Connecting to {selected_city} station...",
        "Establishing secure connection...",
        "Loading air quality data...",
        "Synchronizing with sensors...",
        "Processing environmental metrics...",
        "Calibrating monitoring systems...",
        "Data integrity verified...",
        "Ready to display analytics..."
    ]

    # Countdown loop from 7 down to 0
    for i in range(7, -1, -1):
        # Calculate progress percentage (0% to 100%)
        progress_pct = int(((7 - i) / 7) * 100)
        
        # Determine status message (ensuring we don't out-of-index)
        msg_idx = min(7 - i, len(status_messages) - 1)
        current_msg = status_messages[msg_idx]
        if i == 4:
            try:
                st.session_state.current_city_data = cached_current_aqi(selected_city)
                st.session_state.current_city_history = cached_last_24_hours(selected_city)
            except Exception as e:
                st.session_state.fetch_error = str(e)

        with placeholder.container():
            st.markdown(f"""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;900&display=swap');
                
                .loader-container {{
                    position: fixed;
                    top: 0; left: 0; width: 100vw; height: 100vh;
                    background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
                    display: flex; flex-direction: column;
                    align-items: center; justify-content: center;
                    z-index: 9999;
                    font-family: 'Inter', sans-serif;
                }}
                
                .air-wave-container {{
                    position: relative; width: 150px; height: 150px; margin-bottom: 2rem;
                }}
                
                .air-wave {{
                    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                    width: 60px; height: 60px; border-radius: 50%;
                    background: radial-gradient(circle, rgba(96, 165, 250, 0.3), transparent);
                    animation: wave 1.5s ease-out infinite;
                }}
                
                @keyframes wave {{
                    0% {{ width: 60px; height: 60px; opacity: 1; }}
                    100% {{ width: 150px; height: 150px; opacity: 0; }}
                }}
                
                .earth-icon {{
                    position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                    font-size: 2.5rem; animation: float 2s ease-in-out infinite;
                }}

                @keyframes float {{
                    0%, 100% {{ transform: translate(-50%, -50%) translateY(0px); }}
                    50% {{ transform: translate(-50%, -50%) translateY(-8px); }}
                }}

                .countdown {{
                    font-size: 3.5rem; font-weight: 900;
                    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                }}

                .status-text {{ color: #94a3b8; font-size: 0.9rem; margin-bottom: 2rem; font-weight: 500; }}

                .progress-container {{
                    width: 300px; height: 4px; background: rgba(148, 163, 184, 0.2);
                    border-radius: 10px; overflow: hidden;
                }}

                .progress-bar {{
                    width: {progress_pct}%; height: 100%;
                    background: linear-gradient(90deg, #60a5fa, #a78bfa);
                    transition: width 0.4s ease;
                }}
            </style>
            
            <div class="loader-container">
                <div class="air-wave-container">
                    <div class="air-wave"></div>
                    <div class="air-wave" style="animation-delay: 0.5s"></div>
                    <div class="earth-icon">🌍</div>
                </div>
                <div style="color: #cbd5e1; font-weight: 600; letter-spacing: 0.1em;">{selected_city.upper()} STATION</div>
                <div class="countdown">{i}</div>
                <div class="status-text">{current_msg}</div>
                <div class="progress-container">
                    <div class="progress-bar"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        time.sleep(1)
    
    # Clean up
    placeholder.empty()
    st.session_state.city_loading = False
    st.rerun()
# ------------------ DATA FETCH & RENDER ------------------
data = st.session_state.get('current_city_data')
history = st.session_state.get('current_city_history')
if not data:
    with st.spinner("Finalizing data connection..."):
        data = cached_current_aqi(selected_city)
        history = cached_last_24_hours(selected_city)


if data:
    
    try:
        data = cached_current_aqi(selected_city)
        if data:
            aqi = data["aqi"]
            pollutants = data["pollutants"]
            recorded_at = format_timestamp(data.get("recorded_at", "N/A"))
            theme = get_aqi_theme(aqi)
            safety = get_safety_advice(aqi)

            # 1. Header Card & Safe Window
            col_header, col_window = st.columns([3, 1])
            with col_header:
                st.markdown(f"""
    <div class="dashboard-header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
    <div class="city-title">{selected_city.upper()}</div>
    <div class="sync-time">LAST SYNC: {recorded_at}</div>
    </div>
    <div class="aqi-display" style="color: {theme['color']};">
    {aqi}<span class="aqi-label">AQI Index</span>
    </div>
    <div class="status-badge" style="background: {theme['bg_color']}; color: {theme['color']}; border-color: {theme['color']};">
    {theme['label']}
    </div>
    </div>
    """, unsafe_allow_html=True)
                
            with col_window:
                st.markdown(f"""
    <div class="safe-window-card">
    <div class="safe-window-label">Safe Outdoor Window</div>
    <div class="safe-window-value">{safety['safe_window']}</div>
    <div class="risk-badge" style="background: {safety['color']}22; color: {safety['color']}; border-color: {safety['color']}33;">
    RISK: {safety['risk_level']}
    </div>
    </div>
    """, unsafe_allow_html=True)

            # 2. Safety Recommendations
            st.markdown(f"""
    <div class="safety-card" style="border-left-color: {safety['color']};">
    <h3 style="color: {safety['color']}; margin:0; font-size: 1.5rem; font-weight: 700;">{safety['title']}</h3>
    <p style="margin: 1rem 0 0 0; color: #e2e8f0; line-height: 1.6;">{safety['desc']}</p>
    <p style="font-size: 0.95rem; font-weight: 700; margin-top: 1.5rem; color: #f1f5f9;">Recommended Precautions:</p>
    <ul>
    {"".join([f"<li>{step}</li>" for step in safety['steps']])}
    </ul>
    </div>
    """, unsafe_allow_html=True)

            # 3. MEDICAL GUIDE
            st.markdown("<div class='section-head'>Medical Intelligence Hub</div>", unsafe_allow_html=True)
            with st.expander("Deep Dive: How Pollutants Affect Your Biology"):
                st.markdown(f"""
    <div class="med-grid">
    <div class="med-card" style="border-left-color: #ef4444;">
    <div class="med-title" style="color: #ef4444;">PM2.5 (Fine Particulate Matter)</div>
    <div class="med-desc">Particles smaller than 2.5 microns that bypass natural filters to enter the <b>bloodstream</b> directly. <b>Health Risks:</b> Cardiovascular disease, heart attacks, and chronic respiratory conditions including asthma.</div>
    </div>
    <div class="med-card" style="border-left-color: #f59e0b;">
    <div class="med-title" style="color: #f59e0b;">NO₂ (Nitrogen Dioxide)</div>
    <div class="med-desc">Toxic gas primarily from vehicle exhaust and industrial emissions. High concentrations cause <b>airway inflammation</b> and contribute to chronic respiratory issues and reduced lung function.</div>
    </div>
    <div class="med-card" style="border-left-color: #3b82f6;">
    <div class="med-title" style="color: #3b82f6;">PM10 (Coarse Particulate Matter)</div>
    <div class="med-desc">Larger dust particles and pollen that irritate the upper respiratory tract. <b>Health Risks:</b> Nasal congestion, throat irritation, and exacerbation of existing respiratory conditions.</div>
    </div>
    </div>
    """, unsafe_allow_html=True)

            # 4. Technical Metrics
            st.markdown("<div class='section-head'>Live Pollutant Breakdown</div>", unsafe_allow_html=True)
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("PM2.5", f"{pollutants['pm2_5']} µg/m³")
            m2.metric("PM10", f"{pollutants['pm10']} µg/m³")
            m3.metric("Nitrogen Dioxide", f"{pollutants['no2']} µg/m³")
            m4.metric("Carbon Monoxide", f"{pollutants['co']} mg/m³")   

            # 5. CHARTS & TRENDS
            st.markdown("<div class='section-head'>24-Hour Analysis & Trends</div>", unsafe_allow_html=True)
            
            history = cached_last_24_hours(selected_city)
            if history:
                df_hist = pd.DataFrame(history)
                df_hist["recorded_at"] = pd.to_datetime(df_hist["recorded_at"])
                df_hist_idx = df_hist.set_index("recorded_at")

                # Bar Chart
                st.markdown("#### Current Pollutant Concentration")
                bar_data = pd.DataFrame(pollutants.items(), columns=["Gas", "Value"])
                fig_bar = px.bar(bar_data, x="Gas", y="Value", color="Gas", title="Current Levels (µg/m³)", template="plotly_dark")
                fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_bar, use_container_width=True)

                # Donut Chart
                st.markdown("#### Pollutant Contribution Distribution")
                fig_pie = px.pie(bar_data, names="Gas", values="Value", hole=0.55, title="Atmospheric Composition %", template="plotly_dark")
                fig_pie.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_pie, use_container_width=True)

                # Area Chart
                st.markdown("#### Historical Pollutant Load")
                pollutant_cols = ['pm2_5', 'pm10', 'no2']
                available_cols = [col for col in pollutant_cols if col in df_hist_idx.columns]
                fig_area = px.area(df_hist_idx.reset_index(), x="recorded_at", y=available_cols, title="24-Hour Pollutant Volume", template="plotly_dark")
                fig_area.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_area, use_container_width=True)

                # Line Chart
                st.markdown("#### 24-Hour AQI Trend Analysis")
                fig_line = px.line(df_hist_idx.reset_index(), x="recorded_at", y="aqi", title="AQI Stability Tracker", template="plotly_dark")
                fig_line.update_traces(line=dict(width=4, color="#ef4444"))
                fig_line.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_line, use_container_width=True)

            else:
                st.info("Historical data is being synchronized for this station.")        

    except Exception as e:
        st.error(f"Critical System Failure: {str(e)}")
else:
    st.warning(f"No active data streams found for {selected_city}. Please try another station.")
# ------------------ FOOTER ------------------
st.markdown("""
<div class="footer-container">
<div class="footer-logo">🌍 Sky<span>Guard</span></div>
<div class="footer-credits">
SkyGuard Systems • Architected by <b>Vishal Baghel</b> • © 2025
<br><span style="font-size: 10px; opacity: 0.5; margin-top: 10px; display: block;">v2.5.0 Stable Release</span>
</div>
</div>
""", unsafe_allow_html=True)