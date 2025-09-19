import streamlit as st
from typing import Dict, List, Optional

# Mock user database
MOCK_USERS = [
    {
        'id': '1',
        'name': 'Dr. Sarah Chen',
        'email': 'researcher@agro-ocean.com',
        'role': 'researcher',
        'password': 'password123'
    },
    {
        'id': '2',
        'name': 'Alex Kumar',
        'email': 'analyst@agro-ocean.com',
        'role': 'weather_analyst',
        'password': 'password123'
    },
    {
        'id': '3',
        'name': 'Captain Maria Santos',
        'email': 'authority@agro-ocean.com',
        'role': 'marine_authority',
        'password': 'password123'
    },
    {
        'id': '4',
        'name': 'John Fisher',
        'email': 'fleet@agro-ocean.com',
        'role': 'fleet_manager',
        'password': 'password123'
    }
]

def check_authentication(email: str, password: str) -> bool:
    """
    Check if the provided credentials are valid
    
    Args:
        email: User email
        password: User password
        
    Returns:
        bool: True if credentials are valid, False otherwise
    """
    user = next((u for u in MOCK_USERS if u['email'] == email and u['password'] == password), None)
    
    if user:
        # Store user in session state
        st.session_state.authenticated = True
        st.session_state.user = {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user['role']
        }
        return True
    
    return False

def logout():
    """Logout the current user"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.selected_bot = None

def get_current_user() -> Optional[Dict]:
    """Get the currently authenticated user"""
    return st.session_state.get('user', None)

def require_auth():
    """Decorator to require authentication for a page"""
    if not st.session_state.get('authenticated', False):
        st.error("Please log in to access this page.")
        st.stop()