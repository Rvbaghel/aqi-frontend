import streamlit as st
import sys
import folium
from streamlit_folium import st_folium
from pathlib import Path
import inspect
import time

# ------------------ PATH CONFIGURATION ------------------
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

try:
    from services.api_client import get_cities, get_current_aqi
except Exception:
    def get_cities():
        return ["Delhi", "Mumbai", "Ahmedabad", "Bengaluru", "Kolkata", "Chennai"]
    def get_current_aqi(city):
        return None

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="SkyGuard | Air Quality Intelligence",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

import streamlit as st
import time

# ------------------ LOADING ANIMATION WITH COUNTDOWN ------------------
if 'page_loaded' not in st.session_state:
    st.session_state.page_loaded = False

if not st.session_state.page_loaded:
    placeholder = st.empty()
    
    status_messages = [
        "Initializing atmospheric sensors...",
        "Establishing secure connection...",
        "Loading air quality data...",
        "Synchronizing with satellites...",
        "Processing environmental metrics...",
        "Calibrating monitoring systems...",
        "Verifying data integrity...",
        "Preparing analytics dashboard...",
        "Finalizing configuration...",
        "Ready to launch...",
        "Welcome!"
    ]

    # Countdown loop from 10 to 0
    for i in range(10, -1, -1):
        # Calculate progress percentage (0% to 100%)
        progress_pct = (10 - i) * 10 
        
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
                
                .earth-icon {{
                    font-size: 4rem;
                    margin-bottom: 20px;
                    animation: float 3s ease-in-out infinite;
                }}

                @keyframes float {{
                    0%, 100% {{ transform: translateY(0px); }}
                    50% {{ transform: translateY(-15px); }}
                }}

                .countdown {{
                    font-size: 3.5rem;
                    font-weight: 900;
                    background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    margin: 10px 0;
                }}

                .status-text {{
                    color: #94a3b8;
                    font-size: 1rem;
                    margin-bottom: 20px;
                    height: 20px;
                }}

                .progress-container {{
                    width: 300px;
                    height: 6px;
                    background: rgba(255, 255, 255, 0.1);
                    border-radius: 10px;
                    overflow: hidden;
                }}

                .progress-bar {{
                    width: {progress_pct}%;
                    height: 100%;
                    background: linear-gradient(90deg, #60a5fa, #a78bfa);
                    transition: width 0.5s ease-in-out;
                }}
            </style>
            
            <div class="loader-container">
                <div class="earth-icon">🌍</div>
                <div style="color: #cbd5e1; font-weight: 600;">DATABASE SYNC</div>
                <div class="countdown">{i}</div>
                <div class="status-text">{status_messages[10-i]}</div>
                <div class="progress-container">
                    <div class="progress-bar"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        time.sleep(1)
    
    placeholder.empty()
    st.session_state.page_loaded = True
    st.rerun()

# # --- Main App Content ---
# st.success("Successfully connected to PostgreSQL!")
# st.title("AQI Analytics Dashboard")
# ------------------ HELPERS ------------------
def get_marker_color(aqi):
    colors = {1: '#22c55e', 2: '#84cc16', 3: '#eab308', 4: '#f97316', 5: '#ef4444'}
    return colors.get(aqi, '#94a3b8')

def calculate_safe_time(aqi):
    """Simple logic for safe outdoor exposure based on AQI index."""
    if aqi <= 1: return "Unlimited"
    if aqi == 2: return "4 - 6 Hours"
    if aqi == 3: return "1 - 2 Hours"
    if aqi == 4: return "30 Minutes"
    return "Stay Indoors"

@st.cache_data(ttl=3600)
def get_cached_cities():
    return get_cities()

@st.cache_data(ttl=300)
def get_cached_aqi(city):
    return get_current_aqi(city)

# ------------------ ADVANCED PROFESSIONAL STYLING ------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: -0.01em;
    }
    
    html { scroll-behavior: smooth; }
    
    .stApp { 
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
    }
    
    #MainMenu, footer, header, .stDeployButton {display: none;}
    [id^="section-"] { scroll-margin-top: 100px; }

    /* Professional Navigation */
    .top-nav {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(2, 6, 23, 0.98) 100%);
        backdrop-filter: blur(20px);
        padding: 1rem 5%;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        position: sticky;
        top: 0;
        z-index: 999;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .logo { 
        font-size: 1.5rem;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: -0.02em;
    }
    
    .logo span { 
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .nav-links {
        display: flex;
        align-items: center;
        gap: 2rem;
    }
    
    .nav-links a {
        color: #cbd5e1;
        text-decoration: none;
        font-size: 0.9rem;
        font-weight: 600;
        transition: all 0.3s ease;
        position: relative;
        padding: 0.5rem 0;
    }
    
    .nav-links a::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 0;
        height: 2px;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        transition: width 0.3s ease;
    }
    
    .nav-links a:hover {
        color: #60a5fa;
    }
    
    .nav-links a:hover::after {
        width: 100%;
    }

    .status-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(16, 185, 129, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        border: 1px solid rgba(16, 185, 129, 0.3);
    }
    
    .pulse {
        height: 8px;
        width: 8px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse-animation 2s infinite;
    }
    
    @keyframes pulse-animation {
        0% { box-shadow: 0 0 0 0px rgba(16, 185, 129, 0.7); }
        100% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
    }
    
    .status-text {
        color: #10b981;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.05em;
    }

    /* Enhanced Hero Section */
    .hero-container {
        background: radial-gradient(ellipse at top, rgba(59, 130, 246, 0.15) 0%, transparent 60%),
                    linear-gradient(135deg, #1e293b 0%, #020617 100%);
        padding: 8rem 2rem 6rem 2rem;
        text-align: center;
        border-radius: 0 0 60px 60px;
        position: relative;
        overflow: hidden;
        border-bottom: 1px solid rgba(148, 163, 184, 0.08);
    }
    
    .hero-container::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M 100 0 L 0 0 0 100" fill="none" stroke="rgba(148,163,184,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        opacity: 0.3;
    }
    
    .earth-wrapper {
        display: inline-block;
        margin-bottom: 2rem;
        position: relative;
        z-index: 1;
    }
    
    .spinning-earth {
        font-size: 5rem;
        display: inline-block;
        animation: realisticRotation 30s linear infinite;
        filter: drop-shadow(0 0 40px rgba(96, 165, 250, 0.4));
    }
    
    @keyframes realisticRotation {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .hero-title {
        font-size: 4.5rem;
        font-weight: 900;
        margin-bottom: 2rem;
        letter-spacing: -0.03em;
        line-height: 1.1;
        color: #f8fafc;
        position: relative;
        z-index: 1;
    }
    
    .hero-gradient-text {
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    
    .badge-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 2.5rem;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }
    
    .hero-badge {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.3) 100%);
        backdrop-filter: blur(12px);
        padding: 0.65rem 1.5rem;
        border-radius: 24px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.05em;
        border: 1.5px solid;
        transition: all 0.3s ease;
    }
    
    .hero-badge:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    
    .hero-description {
        color: #cbd5e1;
        font-size: 1.2rem;
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.8;
        position: relative;
        z-index: 1;
        font-weight: 400;
    }

    /* Section Titles */
    .section-title {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        color: #f8fafc;
        margin: 5rem 0 3rem 0;
        letter-spacing: -0.02em;
        position: relative;
        display: inline-block;
        width: 100%;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        border-radius: 2px;
    }

    /* City Cards - Enhanced Professional Design */
    .city-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.3) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 24px;
        padding: 2.5rem 2rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .city-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #60a5fa, transparent);
        opacity: 0;
        transition: opacity 0.4s;
    }
    
    .city-card:hover {
        transform: translateY(-10px);
        border-color: rgba(96, 165, 250, 0.3);
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.5) 100%);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
    }
    
    .city-card:hover::before {
        opacity: 1;
    }
    
    .city-card h3 {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.5rem;
        letter-spacing: -0.01em;
    }
    
    .city-status {
        color: #10b981;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    .city-status::before {
        content: '';
        width: 6px;
        height: 6px;
        background: #10b981;
        border-radius: 50%;
        animation: pulse-animation 2s infinite;
    }

    /* View Button */
    .view-btn {
        display: inline-block;
        margin-top: 1rem;
        padding: 0.75rem 2rem;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.15) 0%, rgba(37, 99, 235, 0.1) 100%);
        color: #60a5fa;
        border: 1.5px solid rgba(96, 165, 250, 0.3);
        border-radius: 24px;
        font-size: 0.85rem;
        font-weight: 700;
        text-decoration: none;
        transition: all 0.3s ease;
        letter-spacing: 0.02em;
    }
    
    .view-btn:hover {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-color: #3b82f6;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
        transform: translateY(-2px);
    }

    /* Medical Cards */
    .med-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmin(280px, 1fr));
        gap: 1.5rem;
        margin-top: 2rem;
    }
    
    .med-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.3) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.08);
        border-radius: 20px;
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
        font-size: 1.15rem;
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

    /* CTA Section */
    .cta-wrapper {
        text-align: center;
        padding: 5rem 2rem;
        background: radial-gradient(ellipse at center, rgba(59, 130, 246, 0.08) 0%, transparent 70%);
        border-radius: 40px;
        margin: 5rem 5%;
        border: 1px solid rgba(148, 163, 184, 0.08);
        position: relative;
        overflow: hidden;
    }
    
    .cta-wrapper::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(96, 165, 250, 0.03) 0%, transparent 100%);
    }
    
    .cta-text {
        color: #94a3b8;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        letter-spacing: 0.01em;
        position: relative;
        z-index: 1;
    }
    
    .cta-wrapper h2 {
        color: #f8fafc;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
    }

    /* Streamlit Button Enhancement */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 16px;
        padding: 1rem 3rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        letter-spacing: 0.02em;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    }

    /* Expander Enhancement */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.3) 100%);
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.1);
        font-weight: 700;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: rgba(96, 165, 250, 0.3);
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.5) 100%);
    }

    /* Footer */
    .footer-container {
        text-align: center;
        padding: 4rem 2rem;
        margin-top: 6rem;
        border-top: 1px solid rgba(148, 163, 184, 0.08);
        background: linear-gradient(to bottom, transparent, rgba(15, 23, 42, 0.3));
    }
    
    .footer-logo {
        font-size: 1.3rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 1.5rem;
        letter-spacing: -0.01em;
    }
    
    .footer-logo span {
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .footer-links {
        margin-bottom: 2rem;
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
    }
    
    .footer-links a {
        color: #64748b;
        text-decoration: none;
        font-size: 0.85rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .footer-links a:hover {
        color: #60a5fa;
    }
    
    .footer-credits {
        color: #475569;
        font-size: 0.75rem;
        letter-spacing: 0.05em;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# ------------------ PROFESSIONAL NAVBAR ------------------
st.markdown("""
<div class="top-nav">
    <div class="logo">Sky<span>Guard</span></div>
    <div class="nav-links">
        <a href="#section-hero">Intelligence</a>
        <a href="#section-map">Geospatial</a>
        <a href="#section-grid">Network</a>
        <div class="status-indicator">
            <span class="pulse"></span>
            <span class="status-text">LIVE SECURE</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------ ENHANCED HERO SECTION ------------------
st.markdown('<div id="section-hero"></div>', unsafe_allow_html=True)

hero_html = """
<div class="hero-container">
<div class="earth-wrapper">
<div class="spinning-earth">🌍</div>
</div>
<h1 class="hero-title">
The Future of<br><span class="hero-gradient-text">Atmospheric Intelligence</span>
</h1>
<div class="badge-container">
<div class="hero-badge" style="border-color: #22c55e; color: #22c55e;">ULTRA PURE</div>
<div class="hero-badge" style="border-color: #60a5fa; color: #60a5fa;">REAL-TIME DATA</div>
<div class="hero-badge" style="border-color: #f59e0b; color: #f59e0b;">SKY GUARD</div>
</div>
<p class="hero-description">
Empowering global citizens with hyper-local air quality insights.
Utilizing AI-driven models to predict and protect your urban environment.
</p>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# ------------------ PROFESSIONAL MAP SECTION ------------------
st.markdown('<div id="section-map"></div>', unsafe_allow_html=True)
m_col1, m_col2, m_col3 = st.columns([1, 10, 1])
with m_col2:
    st.markdown("<h2 class='section-title'>Global Geospatial Index</h2>", unsafe_allow_html=True)
    city_coords = {
        "Delhi": [28.6139, 77.2090], "Mumbai": [19.0760, 72.8777],
        "Ahmedabad": [23.0258, 72.5873], "Bengaluru": [12.9716, 77.5946],
        "Kolkata": [22.5726, 88.3639], "Chennai": [13.0827, 80.2707]
    }
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles="CartoDB dark_matter", scrollWheelZoom=False)   
    for city, coords in city_coords.items():
        try:
            data = get_current_aqi(city)
            aqi_val = data.get("aqi", 1)
            color = get_marker_color(aqi_val)
            folium.CircleMarker(location=coords, radius=12, color=color, fill=True, fill_opacity=0.6).add_to(m)
        except: continue
    st_folium(m, width="100%", height=500)

cities = get_cached_cities()

# ------------------ MEDICAL INTELLIGENCE HUB ------------------
st.markdown("<div id='section-medical'></div>", unsafe_allow_html=True)
st.markdown("<h2 class='section-title'>Medical Intelligence Hub</h2>", unsafe_allow_html=True)

with st.expander("Deep Dive: How Pollutants Affect Your Biology"):
    st.markdown("""
<div class="med-grid">
<div class="med-card" style="border-left-color: #ef4444;">
<div class="med-title" style="color: #ef4444;">PM2.5 (Fine Particulate Matter)</div>
<div class="med-desc">
Microscopic particles smaller than 2.5 microns that bypass natural filters to enter the <b>bloodstream</b> directly.
<br><br><b>Health Risks:</b> Cardiovascular disease, heart attacks, decreased lung function, and aggravated asthma.
</div>
</div>
<div class="med-card" style="border-left-color: #f59e0b;">
<div class="med-title" style="color: #f59e0b;">NO₂ (Nitrogen Dioxide)</div>
<div class="med-desc">
A toxic gas primarily from vehicle emissions. High concentrations cause <b>airway inflammation</b> and respiratory issues.
<br><br><b>Health Risks:</b> Increased susceptibility to respiratory infections and chronic bronchitis.
</div>
</div>
<div class="med-card" style="border-left-color: #3b82f6;">
<div class="med-title" style="color: #3b82f6;">PM10 (Coarse Particulate Matter)</div>
<div class="med-desc">
Larger particles like dust and pollen that irritate the upper respiratory tract. Less deep-penetrating than PM2.5.
<br><br><b>Health Risks:</b> Nasal congestion, persistent coughing, and throat irritation.
</div>
</div>
<div class="med-card" style="border-left-color: #a78bfa;">
<div class="med-title" style="color: #a78bfa;">CO (Carbon Monoxide)</div>
<div class="med-desc">
An odorless gas that reduces the blood's ability to carry <b>oxygen</b> to vital organs including the heart and brain.
<br><br><b>Health Risks:</b> Dizziness, confusion, headaches, and cardiovascular strain.
</div>
</div>
</div>
""", unsafe_allow_html=True)

# ------------------ PROFESSIONAL MONITORING NETWORK ------------------
st.markdown('<div id="section-grid"></div>', unsafe_allow_html=True)
st.markdown("<h2 class='section-title'>Monitoring Network</h2>", unsafe_allow_html=True)

rows = [cities[i:i + 3] for i in range(0, len(cities), 3)]
for row in rows:
    cols = st.columns(3)
    for i, city in enumerate(row):
        with cols[i]:
            st.markdown(f"""
<div class="city-card">
<h3>{city}</h3>
<div class="city-status">STATION ONLINE</div>
<a href="/Dashboard" target="_self" class="view-btn">VIEW ANALYTICS →</a>
</div>
""", unsafe_allow_html=True)

# ------------------ PROFESSIONAL CTA SECTION ------------------
st.markdown("""
<div class="cta-wrapper">
<h2>Ready for Deep Insights?</h2>
<p class="cta-text">Join thousands of users monitoring urban air quality in real-time.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Launch Deep Analytics Dashboard", type="primary", use_container_width=True):
        st.switch_page("pages/Dashboard.py")

# ------------------ PROFESSIONAL FOOTER ------------------
st.markdown("""
<div class="footer-container">
<div class="footer-logo">Sky<span>Guard</span></div>
<div class="footer-links">
<a href="#section-hero">Top</a>
<a href="#section-map">Geospatial</a>
<a href="#section-medical">Health Intelligence</a>
<a href="#section-grid">Network Status</a>
</div>
<div class="footer-credits">
SkyGuard Systems • Architected by <b>Vishal Baghel</b> • © 2025
<br><span style="font-size: 10px; opacity: 0.5; margin-top: 10px; display: block;">v2.5.0 Stable Release</span>
</div>
</div>
""", unsafe_allow_html=True)