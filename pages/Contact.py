import streamlit as st
import sys
from pathlib import Path
import textwrap
import inspect

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="SkyGuard | Contact Vishal",
    page_icon="✉️",
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

    /* Professional Navigation */
    .top-nav {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(2, 6, 23, 0.98) 100%);
        backdrop-filter: blur(20px);
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(148, 163, 184, 0.1);
        margin-bottom: 3rem;
        border-radius: 0 0 24px 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .top-nav h3 {
        margin: 0;
        font-size: 1.3rem;
        font-weight: 800;
        color: #f8fafc;
        letter-spacing: -0.02em;
    }
    
    .top-nav span {
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 3rem 2rem 4rem 2rem;
        margin-bottom: 3rem;
        position: relative;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        letter-spacing: -0.03em;
    }
    
    .hero-subtitle {
        color: #cbd5e1;
        font-size: 1.2rem;
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.8;
        font-weight: 400;
    }

    /* Contact Card */
    .contact-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.4) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 24px;
        padding: 3rem;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
    }
    
    .contact-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #60a5fa, transparent);
    }
    
    .contact-card:hover {
        border-color: rgba(96, 165, 250, 0.3);
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.6) 100%);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }

    .name-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .role-subtitle {
        color: #60a5fa;
        font-size: 0.95rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 2rem;
        font-weight: 700;
    }
    
    .contact-description {
        color: #cbd5e1;
        line-height: 1.8;
        margin-bottom: 2.5rem;
        font-size: 0.95rem;
    }

    .contact-item {
        display: flex;
        align-items: center;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: rgba(15, 23, 42, 0.4);
        border-radius: 12px;
        border: 1px solid rgba(148, 163, 184, 0.05);
        transition: all 0.3s ease;
    }
    
    .contact-item:hover {
        background: rgba(59, 130, 246, 0.1);
        border-color: rgba(96, 165, 250, 0.2);
        transform: translateX(5px);
    }

    .contact-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        min-width: 40px;
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(37, 99, 235, 0.1) 100%);
        border-radius: 10px;
        margin-right: 1rem;
        font-size: 1.2rem;
    }
    
    .contact-item a {
        color: #e2e8f0;
        text-decoration: none;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .contact-item:hover a {
        color: #60a5fa;
    }
    
    .contact-item-text {
        color: #e2e8f0;
        font-weight: 500;
    }

    /* Message Form Card */
    .message-card {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.4) 100%);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(148, 163, 184, 0.1);
        border-radius: 24px;
        padding: 3rem;
        position: relative;
        overflow: hidden;
    }
    
    .message-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #60a5fa, transparent);
    }
    
    .message-card h2 {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 2rem;
        letter-spacing: -0.02em;
    }

    /* Form Styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {
        background: rgba(15, 23, 42, 0.8) !important;
        color: #f1f5f9 !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        border-radius: 12px !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus {
        border-color: rgba(96, 165, 250, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        outline: none !important;
    }
    
    .stTextInput > label,
    .stTextArea > label,
    .stSelectbox > label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.6) 100%);
        color: #e2e8f0;
        border: 1.5px solid rgba(148, 163, 184, 0.2);
        border-radius: 16px;
        padding: 1rem 2rem;
        font-weight: 700;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        backdrop-filter: blur(8px);
        letter-spacing: 0.01em;
        width: 100%;
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

    /* Alert Messages */
    .stSuccess, .stError {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(12px);
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
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

# ------------------ TOP NAV ------------------
st.markdown("""
<div class="top-nav">
<h3>SkyGuard <span>Network</span></h3>
</div>
""", unsafe_allow_html=True)

nav_col1, nav_col2, nav_col3 = st.columns([1, 4, 1])
with nav_col3:
    if st.button("← Back to Home", use_container_width=True):
        st.switch_page("Home.py")
with nav_col1:
    if st.button("← Back to Dashboard", use_container_width=True):
        st.switch_page("pages/Dashboard.py")

# ------------------ HERO SECTION ------------------
st.markdown("""
<div class="hero-section">
<h1 class="hero-title">Get in Touch</h1>
<p class="hero-subtitle">Have questions about the AQI monitoring system or want to collaborate on environmental data projects? Let's connect.</p>
</div>
""", unsafe_allow_html=True)

# ------------------ CONTENT ------------------
left_col, right_col = st.columns([1, 1], gap="large")

with left_col:
    contact_html = """
<div class="contact-card">
<div class="name-title">Vishal Baghel</div>
<div class="role-subtitle">Lead Developer • SkyGuard Systems</div>
<p class="contact-description">
Passionate about building intelligent systems that make environmental data accessible and actionable. Open to collaborations, partnerships, and discussions about air quality monitoring solutions.
</p>
<div class="contact-item">
<div class="contact-icon">📧</div>
<a href="mailto:baghelvishal264@gmail.com">baghelvishal264@gmail.com</a>
</div>
<div class="contact-item">
<div class="contact-icon">🔗</div>
<a href="https://www.linkedin.com/in/vishal-baghel-a055b5249/" target="_blank">LinkedIn Profile</a>
</div>
<div class="contact-item">
<div class="contact-icon">📍</div>
<span class="contact-item-text">Ahmedabad, Gujarat, India</span>
</div>
</div>
"""
    st.markdown(contact_html, unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="message-card">', unsafe_allow_html=True)
    st.markdown("<h2>Send a Message</h2>", unsafe_allow_html=True)
    
    with st.form("contact_form", clear_on_submit=True):
        name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email Address", placeholder="your.email@example.com")
        subject = st.selectbox(
            "Subject", 
            ["General Inquiry", "Data Partnership", "Technical Support", "Feedback", "Collaboration Opportunity"]
        )
        message = st.text_area("Your Message", height=150, placeholder="Tell me about your inquiry or project...")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            submit_button = st.form_submit_button("Send Message", type="primary", use_container_width=True)
        
        if submit_button:
            if name and email and message:
                st.success(f"Thank you, {name}! Your message has been received. I'll get back to you shortly.")
            else:
                st.error("Please fill out all required fields before submitting.")
    
    st.markdown('</div>', unsafe_allow_html=True)

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