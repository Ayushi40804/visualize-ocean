import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Agro-Ocean SIH",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import custom modules
from utils.auth import check_authentication, logout
from utils.data_models import get_mock_agrobots, get_mock_alerts, get_recent_data
from utils.config import config

# Import pages directly
import pages.overview as overview
import pages.alerts as alerts  
import pages.route_optimization as route_optimization
import pages.ai_chat as ai_chat
import pages.settings as settings

def main():
    """Main application entry point"""
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'selected_bot' not in st.session_state:
        st.session_state.selected_bot = None
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Overview"
    
    # Check authentication - if not authenticated, show login page without sidebar
    if not st.session_state.authenticated:
        # Hide sidebar completely for login page
        st.markdown("""
        <style>
        .css-1d391kg {
            display: none;
        }
        section[data-testid="stSidebar"] {
            display: none;
        }
        .css-1lcbmhc.e1fqkh3o0 {
            margin-left: 0rem;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Apply theme for login page
        if st.session_state.dark_mode:
            st.markdown("""
            <style>
            .stApp {
                background-color: #0e1117;
                color: #fafafa;
            }
            .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
                color: #fafafa !important;
            }
            .stTextInput > div > div > input {
                background-color: #262730;
                color: #fafafa;
                border: 1px solid #4a4a4a;
            }
            .stButton > button {
                background-color: #262730;
                color: #fafafa !important;
                border: 1px solid #4a4a4a;
            }
            .stExpander {
                background-color: #262730;
                border: 1px solid #4a4a4a;
            }
            .stExpander > div > div {
                color: #fafafa !important;
            }
            </style>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <style>
            .stApp {
                background-color: #ffffff;
                color: #262730;
            }
            .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
                color: #262730 !important;
            }
            </style>
            """, unsafe_allow_html=True)
        
        show_login_page()
        return
    
    # Hide sidebar for authenticated users too
    st.markdown("""
    <style>
    .css-1d391kg {
        display: none;
    }
    section[data-testid="stSidebar"] {
        display: none;
    }
    .css-1lcbmhc.e1fqkh3o0 {
        margin-left: 0rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Apply dark mode if enabled
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: #fafafa !important;
        }
        .stText, .stCaption {
            color: #fafafa !important;
        }
        .stSelectbox > div > div {
            background-color: #262730;
            color: #fafafa;
            border: 1px solid #4a4a4a;
        }
        .stSelectbox > div > div > div {
            color: #fafafa;
        }
        .stTextInput > div > div > input {
            background-color: #262730;
            color: #fafafa;
            border: 1px solid #4a4a4a;
        }
        .stButton > button {
            background-color: #262730;
            color: #fafafa !important;
            border: 1px solid #4a4a4a;
        }
        .stButton > button:hover {
            background-color: #3a3a3a;
            border-color: #ffffff;
            color: #fafafa !important;
        }
        .stButton > button[data-baseweb="button"][kind="primary"] {
            background-color: #0068c9;
            color: #ffffff !important;
        }
        .stButton > button[data-baseweb="button"][kind="primary"]:hover {
            background-color: #0056b3;
            color: #ffffff !important;
        }
        .stMetric {
            background-color: #1e1e1e;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #4a4a4a;
        }
        .stMetric > div {
            color: #fafafa !important;
        }
        .stMetric label {
            color: #fafafa !important;
        }
        .stPlotlyChart {
            background-color: #1e1e1e;
        }
        .stDataFrame {
            background-color: #262730;
            color: #fafafa;
        }
        .stExpander {
            background-color: #262730;
            border: 1px solid #4a4a4a;
        }
        .stExpander > div > div {
            color: #fafafa !important;
        }
        .stChatMessage {
            background-color: #262730;
            border: 1px solid #4a4a4a;
        }
        .stChatMessage > div {
            color: #fafafa !important;
        }
        div[data-testid="stForm"] {
            background-color: #262730;
            border: 1px solid #4a4a4a;
        }
        div[data-testid="stForm"] > div {
            color: #fafafa !important;
        }
        .stAlert {
            background-color: #262730;
            color: #fafafa !important;
            border: 1px solid #4a4a4a;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff;
            color: #262730;
        }
        .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: #262730 !important;
        }
        .stText, .stCaption {
            color: #262730 !important;
        }
        .stSelectbox > div > div {
            background-color: #ffffff;
            color: #262730;
            border: 1px solid #ddd;
        }
        .stSelectbox > div > div > div {
            color: #262730;
        }
        .stTextInput > div > div > input {
            background-color: #ffffff;
            color: #262730;
            border: 1px solid #ddd;
        }
        .stButton > button {
            background-color: #ffffff;
            color: #262730 !important;
            border: 1px solid #ddd;
        }
        .stButton > button:hover {
            background-color: #f0f0f0;
            border-color: #999;
            color: #262730 !important;
        }
        .stButton > button[data-baseweb="button"][kind="primary"] {
            background-color: #0068c9;
            color: #ffffff !important;
        }
        .stButton > button[data-baseweb="button"][kind="primary"]:hover {
            background-color: #0056b3;
            color: #ffffff !important;
        }
        .stMetric {
            background-color: #ffffff;
            padding: 1rem;
            border-radius: 0.5rem;
            border: 1px solid #ddd;
        }
        .stMetric > div {
            color: #262730 !important;
        }
        .stMetric label {
            color: #262730 !important;
        }
        .stPlotlyChart {
            background-color: #ffffff;
        }
        .stDataFrame {
            background-color: #ffffff;
            color: #262730;
        }
        .stExpander {
            background-color: #ffffff;
            border: 1px solid #ddd;
        }
        .stExpander > div > div {
            color: #262730 !important;
        }
        .stChatMessage {
            background-color: #ffffff;
            border: 1px solid #ddd;
        }
        .stChatMessage > div {
            color: #262730 !important;
        }
        div[data-testid="stForm"] {
            background-color: #ffffff;
            border: 1px solid #ddd;
        }
        div[data-testid="stForm"] > div {
            color: #262730 !important;
        }
        .stAlert {
            background-color: #ffffff;
            color: #262730 !important;
            border: 1px solid #ddd;
        }
        </style>
        """, unsafe_allow_html=True)
    
    # For authenticated users, show main navigation
    st.markdown("---")
    
    # Top navigation bar
    col1, col2, col3, col4, col5, col6, col7 = st.columns([2, 1, 1, 1, 1, 1, 1])
    
    with col1:
        st.markdown("### Agro-Ocean SIH Dashboard")
        if st.session_state.user:
            st.caption(f"Welcome, {st.session_state.user['name']} ({st.session_state.user['role'].replace('_', ' ').title()})")
    
    with col2:
        if st.button("Overview", use_container_width=True, type="primary" if st.session_state.current_page == "Overview" else "secondary"):
            st.session_state.current_page = "Overview"
            st.rerun()
    
    with col3:
        if st.button("Alerts", use_container_width=True, type="primary" if st.session_state.current_page == "Alerts" else "secondary"):
            st.session_state.current_page = "Alerts"
            st.rerun()
    
    with col4:
        if st.button("Routes", use_container_width=True, type="primary" if st.session_state.current_page == "Route Optimization" else "secondary"):
            st.session_state.current_page = "Route Optimization"
            st.rerun()
    
    with col5:
        if st.button("AI Chat", use_container_width=True, type="primary" if st.session_state.current_page == "AI Chat" else "secondary"):
            st.session_state.current_page = "AI Chat"
            st.rerun()
    
    with col6:
        if st.button("Settings", use_container_width=True, type="primary" if st.session_state.current_page == "Settings" else "secondary"):
            st.session_state.current_page = "Settings"
            st.rerun()
    
    with col7:
        # Dark mode toggle
        dark_mode_label = "Dark Mode" if not st.session_state.dark_mode else "Light Mode"
        if st.button(dark_mode_label, use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    # Bot selection and logout in a second row
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    
    with col1:
        bots = get_mock_agrobots()
        bot_names = ["No Bot Selected"] + [bot['name'] for bot in bots]
        selected_bot_name = st.selectbox("Select Agro-Bot", bot_names, key="bot_selector")
        
        if selected_bot_name != "No Bot Selected":
            st.session_state.selected_bot = next((bot for bot in bots if bot['name'] == selected_bot_name), None)
        else:
            st.session_state.selected_bot = None
    
    with col2:
        st.write("")  # Empty space
    
    with col3:
        st.write("")  # Empty space
    
    with col4:
        if st.button("Logout", type="secondary", use_container_width=True):
            logout()
            st.rerun()
    
    st.markdown("---")
    
    # Main content area - use session state page
    try:
        if st.session_state.current_page == "Overview":
            overview.show_page()
        elif st.session_state.current_page == "Alerts":
            alerts.show_page()
        elif st.session_state.current_page == "Route Optimization":
            route_optimization.show_page()
        elif st.session_state.current_page == "AI Chat":
            ai_chat.show_page()
        elif st.session_state.current_page == "Settings":
            settings.show_page()
    except Exception as e:
        st.error(f"Error loading page '{st.session_state.current_page}': {str(e)}")
        st.write("Debug info:")
        st.write(f"Current page: {st.session_state.current_page}")
        st.write(f"Available pages: Overview, Alerts, Route Optimization, AI Chat, Settings")
        
        # Show traceback for debugging
        import traceback
        st.code(traceback.format_exc())

def show_login_page():
    """Display the login page"""
    # Dark mode toggle for login page
    col_left, col_right = st.columns([4, 1])
    with col_right:
        dark_mode_label = "Dark Mode" if not st.session_state.dark_mode else "Light Mode"
        if st.button(dark_mode_label, key="login_dark_mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    # Center the content with better spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main title with custom styling
    title_color = "#4A90E2" if not st.session_state.dark_mode else "#6BB6FF"
    subtitle_color = "#666" if not st.session_state.dark_mode else "#ccc"
    
    st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="color: {title_color}; font-size: 3rem; margin-bottom: 0.5rem;">Agro-Ocean SIH Platform</h1>
        <h3 style="color: {subtitle_color}; font-weight: 300; margin-bottom: 2rem;">Advanced Ocean Monitoring & Agricultural Intelligence</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create centered login form
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Login form container with theme-aware styling
        bg_color = "white" if not st.session_state.dark_mode else "#262730"
        text_color = "#333" if not st.session_state.dark_mode else "#fafafa"
        border_color = "rgba(0, 0, 0, 0.1)" if not st.session_state.dark_mode else "rgba(255, 255, 255, 0.1)"
        
        st.markdown(f"""
        <div style="background: {bg_color}; padding: 2rem; border-radius: 10px; box-shadow: 0 4px 6px {border_color}; margin: 1rem 0; border: 1px solid {border_color};">
        """, unsafe_allow_html=True)
        
        st.markdown("### Login to your account")
        
        with st.form("login_form"):
            email = st.text_input("Email", placeholder="Enter your email")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            submitted = st.form_submit_button("Login", use_container_width=True, type="primary")
            
            if submitted:
                if check_authentication(email, password):
                    st.success("Login successful!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid credentials. Please try again.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Demo accounts info
        with st.expander("Demo Accounts"):
            st.markdown("""
            **Available demo accounts:**
            - **Researcher**: researcher@agro-ocean.com / password123
            - **Weather Analyst**: analyst@agro-ocean.com / password123
            - **Marine Authority**: authority@agro-ocean.com / password123
            - **Fleet Manager**: fleet@agro-ocean.com / password123
            """)
    
    # Platform features section
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### Platform Features")
    
    # Features in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Real-time Monitoring**
        - Agro-Bot fleet management
        - Live sensor data
        - Status tracking
        """)
        
    with col2:
        st.markdown("""
        **Ocean Analytics**
        - Environmental data visualization
        - Temperature & salinity tracking
        - Pollution monitoring
        """)
        
    with col3:
        st.markdown("""
        **AI-Powered Features**
        - Intelligent alerts
        - Route optimization
        - Chat assistant
        """)

if __name__ == "__main__":
    main()