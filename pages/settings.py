import streamlit as st
from utils.auth import get_current_user

def show_page():
    """Display the settings page"""
    st.title("Settings")
    st.caption("Configure your Agro-Ocean platform preferences")
    
    user = get_current_user()
    
    # User Profile Settings
    st.subheader("User Profile")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image("https://via.placeholder.com/150x150/4A90E2/FFFFFF?text=Profile", width=150)
        if st.button("Change Photo", type="secondary"):
            st.info("Photo upload functionality would be implemented here.")
    
    with col2:
        if user:
            name = st.text_input("Full Name", value=user.get('name', ''))
            email = st.text_input("Email", value=user.get('email', ''), disabled=True)
            role = st.selectbox("Role", 
                               ["researcher", "weather_analyst", "marine_authority", "fleet_manager"],
                               index=0 if user.get('role') == 'researcher' else
                                     1 if user.get('role') == 'weather_analyst' else
                                     2 if user.get('role') == 'marine_authority' else 3,
                               disabled=True)
    
    # Notification Settings
    st.divider()
    st.subheader("🔔 Notification Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Alert Notifications**")
        email_alerts = st.checkbox("Email notifications for critical alerts", value=True)
        sms_alerts = st.checkbox("SMS notifications for emergencies", value=False)
        push_alerts = st.checkbox("Browser push notifications", value=True)
        
        st.write("**Alert Frequency**")
        alert_frequency = st.selectbox("Alert check frequency", 
                                     ["Real-time", "Every 5 minutes", "Every 15 minutes", "Hourly"])
    
    with col2:
        st.write("**System Notifications**")
        maintenance_alerts = st.checkbox("Bot maintenance reminders", value=True)
        data_alerts = st.checkbox("Data sync notifications", value=False)
        system_updates = st.checkbox("System update notifications", value=True)
        
        st.write("**Report Frequency**")
        report_frequency = st.selectbox("Automated report frequency",
                                      ["Daily", "Weekly", "Monthly", "Disabled"])
    
    # Display Settings
    st.divider()
    st.subheader("🎨 Display Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Theme**")
        theme = st.selectbox("Color theme", ["Light", "Dark", "Auto"])
        
        st.write("**Dashboard Layout**")
        layout = st.selectbox("Default dashboard layout", 
                             ["Compact", "Detailed", "Custom"])
        
        st.write("**Map Settings**")
        map_style = st.selectbox("Map style", 
                               ["OpenStreetMap", "Satellite", "Terrain", "Ocean"])
        show_currents = st.checkbox("Show ocean currents", value=True)
        show_temperature = st.checkbox("Show temperature overlay", value=True)
    
    with col2:
        st.write("**Data Display**")
        units = st.selectbox("Temperature units", ["Celsius", "Fahrenheit"])
        decimal_places = st.slider("Decimal places for readings", 1, 4, 2)
        
        st.write("**Chart Settings**")
        chart_style = st.selectbox("Chart style", ["Modern", "Classic", "Minimal"])
        animation = st.checkbox("Enable chart animations", value=True)
        
        st.write("**Time Zone**")
        timezone = st.selectbox("Display timezone", 
                              ["UTC", "Local", "Eastern", "Pacific", "GMT+5:30"])
    
    # Data & Privacy Settings
    st.divider()
    st.subheader("Data & Privacy")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Data Retention**")
        data_retention = st.selectbox("Data retention period", 
                                    ["30 days", "90 days", "1 year", "2 years", "Indefinite"])
        
        st.write("**Privacy Settings**")
        share_analytics = st.checkbox("Share anonymous usage analytics", value=True)
        location_tracking = st.checkbox("Enable location tracking for mobile app", value=False)
        
        st.write("**Data Export**")
        if st.button("📥 Export My Data", type="secondary"):
            st.success("Data export request submitted. You'll receive an email with download link.")
    
    with col2:
        st.write("**Security**")
        two_factor = st.checkbox("Enable two-factor authentication", value=False)
        session_timeout = st.selectbox("Session timeout", 
                                     ["15 minutes", "30 minutes", "1 hour", "4 hours", "Never"])
        
        st.write("**API Access**")
        api_access = st.checkbox("Enable API access", value=False)
        if api_access:
            st.code("API Key: agro-ocean-api-key-123456789")
            if st.button("Regenerate API Key", type="secondary"):
                st.success("New API key generated!")
    
    # System Settings (Admin only)
    if user and user.get('role') in ['marine_authority', 'researcher']:
        st.divider()
        st.subheader("System Settings")
        st.caption("Administrative settings - changes affect all users")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Bot Management**")
            auto_deploy = st.checkbox("Auto-deploy new bots", value=True)
            maintenance_window = st.selectbox("Maintenance window", 
                                            ["2:00-4:00 AM", "12:00-2:00 AM", "Custom"])
            
            st.write("**Alert Thresholds**")
            temp_threshold = st.slider("Temperature alert threshold (°C)", 20.0, 30.0, 25.0)
            pollution_threshold = st.slider("Pollution index threshold", 1.0, 5.0, 3.0)
            
        with col2:
            st.write("**System Monitoring**")
            health_check = st.selectbox("System health check frequency", 
                                      ["Every minute", "Every 5 minutes", "Every 15 minutes"])
            
            st.write("**Backup Settings**")
            backup_frequency = st.selectbox("Backup frequency", 
                                          ["Hourly", "Daily", "Weekly"])
            backup_retention = st.selectbox("Backup retention", 
                                          ["7 days", "30 days", "90 days"])
    
    # Advanced Settings
    st.divider()
    st.subheader("Advanced Settings")
    
    with st.expander("Experimental Features"):
        st.warning("These features are experimental and may not work as expected.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ai_predictions = st.checkbox("AI-powered weather predictions", value=False)
            machine_learning = st.checkbox("Enable machine learning optimizations", value=False)
            beta_features = st.checkbox("Access beta features", value=False)
        
        with col2:
            advanced_analytics = st.checkbox("Advanced analytics dashboard", value=False)
            real_time_processing = st.checkbox("Real-time data processing", value=True)
            custom_algorithms = st.checkbox("Custom algorithm support", value=False)
    
    # Save Settings
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 4])
    
    with col1:
        if st.button("💾 Save Settings", type="primary"):
            st.success("Settings saved successfully!")
    
    with col2:
        if st.button("Reset to Defaults", type="secondary"):
            st.warning("Settings reset to defaults!")
    
    # System Information
    st.divider()
    st.subheader("System Information")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Platform Version**")
        st.code("v2.1.0")
        st.write("**Last Update**")
        st.code("2024-01-15")
    
    with col2:
        st.write("**Database Status**")
        st.write("Connected")
        st.write("**API Status**")
        st.write("Online")
    
    with col3:
        st.write("**Storage Used**")
        st.progress(0.65)
        st.caption("65% of 100GB")
        st.write("**Active Sessions**")
        st.code("24 users online")
    
    # Support
    st.divider()
    st.subheader("Support")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Documentation**")
        st.markdown("- [User Guide](https://docs.agro-ocean.com/user-guide)")
        st.markdown("- [API Documentation](https://docs.agro-ocean.com/api)")
        st.markdown("- [Troubleshooting](https://docs.agro-ocean.com/troubleshooting)")
    
    with col2:
        st.write("**Contact Support**")
        st.markdown("- Email: support@agro-ocean.com")
        st.markdown("- Phone: +1-800-AGRO-OCN")
        st.markdown("- Live chat (24/7)")
        
        if st.button("Submit Feedback", type="secondary"):
            st.info("Feedback form would open here.")