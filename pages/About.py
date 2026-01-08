import streamlit as st
import inspect

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="SkyGuard | Understanding Air Quality",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ------------------ ENHANCED PROFESSIONAL STYLING ------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * { 
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        letter-spacing: -0.01em;
    }

    .stApp { 
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        color: #f1f5f9;
    }

    #MainMenu, footer, header {display: none;}

    /* Hero Header Section */
    .hero-header {
        background: radial-gradient(ellipse at top, rgba(59, 130, 246, 0.15) 0%, transparent 60%),
                    linear-gradient(135deg, #1e293b 0%, #020617 100%);
        padding: 5rem 2rem 4rem 2rem;
        text-align: center;
        border-radius: 0 0 48px 48px;
        margin-bottom: 4rem;
        position: relative;
        overflow: hidden;
        border-bottom: 1px solid rgba(148, 163, 184, 0.08);
    }
    
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg"><defs><pattern id="grid" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M 100 0 L 0 0 0 100" fill="none" stroke="rgba(148,163,184,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
        opacity: 0.3;
    }

    .title-text {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        letter-spacing: -0.03em;
        position: relative;
        z-index: 1;
    }
    
    .subtitle-text {
        color: #cbd5e1;
        font-size: 1.2rem;
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.8;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }

    /* Section Headers */
    .section-header {
        font-size: 2rem;
        font-weight: 800;
        color: #f8fafc;
        margin: 4rem 0 2rem 0;
        letter-spacing: -0.02em;
        position: relative;
        padding-left: 1.5rem;
    }
    
    .section-header::before {
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

    /* Content Cards */
    .content-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.3) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        padding: 2.5rem;
        border-radius: 24px;
        height: 100%;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .content-card::before {
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
    
    .content-card:hover {
        border-color: rgba(96, 165, 250, 0.3);
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.5) 100%);
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .content-card:hover::before {
        opacity: 1;
    }
    
    .content-card h3 {
        font-size: 1.5rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }
    
    .content-card p {
        color: #cbd5e1;
        line-height: 1.8;
        font-size: 0.95rem;
        font-weight: 400;
    }

    /* Info Cards - Pollutants */
    .info-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.3) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        padding: 2rem;
        border-radius: 20px;
        height: 100%;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border-left: 3px solid;
        position: relative;
        overflow: hidden;
    }
    
    .info-card::before {
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
    
    .info-card:hover {
        transform: translateY(-8px);
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.5) 100%);
        border-color: rgba(96, 165, 250, 0.3);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .info-card:hover::before {
        opacity: 1;
    }
    
    .gas-name {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }
    
    .info-card p {
        color: #cbd5e1;
        line-height: 1.8;
        font-size: 0.95rem;
        font-weight: 400;
    }

    /* AQI Scale Reference */
    .aqi-container {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.3) 100%);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 2rem 0;
    }
    
    .aqi-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1.25rem 1.5rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        border-left: 4px solid;
        gap: 1.5rem;
    }
    
    .aqi-row:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }
    
    .aqi-range {
        font-weight: 700;
        font-size: 1rem;
        min-width: 100px;
        letter-spacing: -0.01em;
    }
    
    .aqi-status {
        font-weight: 700;
        font-size: 1.1rem;
        min-width: 140px;
        letter-spacing: -0.01em;
    }
    
    .aqi-advice {
        color: #cbd5e1;
        font-size: 0.95rem;
        line-height: 1.6;
        flex: 1;
    }

    /* Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.2), transparent);
        margin: 4rem 0;
    }

    /* Navigation Footer */
    .nav-footer {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.3) 100%);
        backdrop-filter: blur(16px);
        padding: 3rem 2rem;
        border-radius: 24px;
        text-align: center;
        margin-top: 5rem;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .nav-footer h3 {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 2rem;
        letter-spacing: -0.02em;
    }

    /* Button Enhancements */
    .stButton > button {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.6) 100%);
        color: #e2e8f0;
        border: 1.5px solid rgba(148, 163, 184, 0.2);
        border-radius: 16px;
        padding: 1rem 2rem;
        margin-top: 5rem;
        margin-bottom: 2rem;        
        font-weight: 700;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(8px);
        letter-spacing: 0.01em;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.15) 100%);
        border-color: rgba(96, 165, 250, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.2);
        color: #f8fafc;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.4);
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

# ------------------ HERO HEADER ------------------
st.markdown("""
<div class="hero-header">
<h1 class="title-text">Understanding Air Quality</h1>
<p class="subtitle-text">Knowledge is the first step toward a healthier environment. Learn how air quality impacts your daily life and health.</p>
</div>
""", unsafe_allow_html=True)

# ------------------ WHAT IS AQI? ------------------
st.markdown('<h2 class="section-header">What is the Air Quality Index?</h2>', unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
<div class="content-card">
<h3>Understanding AQI</h3>
<p>The <strong>Air Quality Index (AQI)</strong> is a standardized system used by government agencies worldwide to communicate how polluted the air currently is or how polluted it is forecast to become.</p>
<br>
<p>Think of the AQI as a measurement scale that runs from 0 to 500. The higher the AQI value, the greater the level of air pollution and the greater the health concern for the general population.</p>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="content-card">
<h3>Low vs High AQI Impact</h3>
<p><strong>When AQI is Low (0-50):</strong> The air is considered satisfactory, and air pollution poses little or no risk. Outdoor activities are encouraged for everyone.</p>
<br>
<p><strong>When AQI is High (200+):</strong> Everyone may begin to experience health effects. Members of sensitive groups may experience more serious health effects. It's recommended to stay indoors and use air purifiers.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ------------------ POLLUTANT DETAILS ------------------
st.markdown('<h2 class="section-header">Key Pollutants Explained</h2>', unsafe_allow_html=True)

p_col1, p_col2, p_col3 = st.columns(3, gap="large")

with p_col1:
    st.markdown("""
<div class="info-card" style="border-left-color: #ef4444;">
<div class="gas-name" style="color: #ef4444;">PM2.5 & PM10</div>
<p>Fine particulate matter that can penetrate deep into the lungs and even enter the bloodstream. PM2.5 is primarily from combustion sources (vehicles, power plants), while PM10 includes larger particles like dust and pollen.</p>
</div>
""", unsafe_allow_html=True)

with p_col2:
    st.markdown("""
<div class="info-card" style="border-left-color: #a78bfa;">
<div class="gas-name" style="color: #a78bfa;">CO (Carbon Monoxide)</div>
<p>A colorless, odorless gas that can be harmful when inhaled in large amounts. It is released when something is burned, typically by motor vehicle exhaust and industrial processes.</p>
</div>
""", unsafe_allow_html=True)

with p_col3:
    st.markdown("""
<div class="info-card" style="border-left-color: #f59e0b;">
<div class="gas-name" style="color: #f59e0b;">NO₂ (Nitrogen Dioxide)</div>
<p>NO₂ primarily enters the air from the burning of fuel. It can cause respiratory issues, aggravate asthma, and is a major contributor to the formation of ground-level ozone and smog.</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ------------------ AQI SCALE REFERENCE ------------------
st.markdown('<h2 class="section-header">The AQI Scale Reference</h2>', unsafe_allow_html=True)

st.markdown('<div class="aqi-container">', unsafe_allow_html=True)

def aqi_row(range_text, status, color, advice):
    st.markdown(f"""
<div class="aqi-row" style="background: {color}15; border-left-color: {color};">
<div class="aqi-range" style="color: #f8fafc;">{range_text}</div>
<div class="aqi-status" style="color: {color};">{status}</div>
<div class="aqi-advice">{advice}</div>
</div>
""", unsafe_allow_html=True)

aqi_row("0 - 50", "Good", "#22c55e", "Air quality is ideal. Enjoy your usual outdoor activities.")
aqi_row("51 - 100", "Moderate", "#84cc16", "Air quality is acceptable. Unusually sensitive people should consider limiting prolonged outdoor exertion.")
aqi_row("101 - 200", "Unhealthy", "#f97316", "Members of sensitive groups may experience health effects. The general public should begin to limit outdoor time.")
aqi_row("201 - 300", "Very Unhealthy", "#ef4444", "Health alert: everyone may experience more serious health effects. Avoid all outdoor physical activities.")
aqi_row("300+", "Hazardous", "#b91c1c", "Health warnings of emergency conditions. The entire population is more likely to be affected. Remain indoors.")

st.markdown('</div>', unsafe_allow_html=True)

# ------------------ NAVIGATION FOOTER ------------------
st.markdown("""
<div class="nav-footer">
<h3>Ready to see the data?</h3>
</div>
""", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])

with nav_col1:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("Home.py")

with nav_col3:
    if st.button("Open Dashboard →", use_container_width=True, type="primary"):
        st.switch_page("pages/Dashboard.py")

# ------------------ FOOTER ------------------
st.markdown("""
<div class="footer-container">
<div class="footer-logo">Sky<span>Guard</span></div>
<div class="footer-credits">
SkyGuard Systems • Architected by <b>Vishal Baghel</b> • © 2025
<br><span style="font-size: 10px; opacity: 0.5; margin-top: 10px; display: block;">v2.5.0 Stable Release</span>
</div>
</div>
""", unsafe_allow_html=True)