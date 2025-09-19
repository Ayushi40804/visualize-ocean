import streamlit as st
import pandas as pd
from datetime import datetime
from utils.data_models import get_mock_alerts

def show_page():
    """Display the alerts page"""
    st.title("Alerts & Notifications")
    
    # Get alerts data
    alerts = get_mock_alerts()
    
    # Filter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        severity_filter = st.selectbox(
            "Filter by Severity",
            ["All", "Critical", "High", "Medium", "Low"]
        )
    
    with col2:
        type_filter = st.selectbox(
            "Filter by Type",
            ["All", "Pollution", "Anomaly", "Equipment", "Cyclone"]
        )
    
    with col3:
        status_filter = st.selectbox(
            "Filter by Status",
            ["All", "Unread", "Read"]
        )
    
    # Apply filters
    filtered_alerts = alerts.copy()
    
    if severity_filter != "All":
        filtered_alerts = [a for a in filtered_alerts if a['severity'].lower() == severity_filter.lower()]
    
    if type_filter != "All":
        filtered_alerts = [a for a in filtered_alerts if a['type'].lower() == type_filter.lower()]
    
    if status_filter == "Unread":
        filtered_alerts = [a for a in filtered_alerts if not a['isRead']]
    elif status_filter == "Read":
        filtered_alerts = [a for a in filtered_alerts if a['isRead']]
    
    # Summary metrics
    st.divider()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_alerts = len(alerts)
        st.metric("Total Alerts", total_alerts)
    
    with col2:
        unread_alerts = len([a for a in alerts if not a['isRead']])
        st.metric("Unread", unread_alerts)
    
    with col3:
        critical_alerts = len([a for a in alerts if a['severity'] == 'critical'])
        high_alerts = len([a for a in alerts if a['severity'] == 'high'])
        st.metric("Critical/High", critical_alerts + high_alerts)
    
    with col4:
        recent_alerts = len([a for a in alerts if 
                           (datetime.now() - datetime.fromisoformat(a['timestamp'])).total_seconds() < 3600])
        st.metric("Last Hour", recent_alerts)
    
    st.divider()
    
    # Alert cards
    if not filtered_alerts:
        st.info("No alerts match the current filters.")
    else:
        for alert in filtered_alerts:
            # Determine alert styling
            severity_colors = {
                'critical': ('🔴', '#fee2e2', '#dc2626'),
                'high': ('🟠', '#fef3c7', '#d97706'),
                'medium': ('🟡', '#ecfdf5', '#059669'),
                'low': ('🔵', '#eff6ff', '#2563eb')
            }
            
            icon, bg_color, border_color = severity_colors.get(alert['severity'], ('⚪', '#f9fafb', '#6b7280'))
            
            # Create alert card
            with st.container():
                st.markdown(f"""
                <div style="
                    border-left: 4px solid {border_color};
                    background-color: {bg_color};
                    padding: 1rem;
                    margin: 0.5rem 0;
                    border-radius: 0.375rem;
                ">
                    <div style="display: flex; justify-content: between; align-items: start;">
                        <div style="flex: 1;">
                            <h4 style="margin: 0; color: {border_color};">
                                {icon} {alert['title']}
                            </h4>
                            <p style="margin: 0.25rem 0; color: #4b5563;">
                                {alert['description']}
                            </p>
                            <div style="display: flex; gap: 1rem; margin-top: 0.5rem; font-size: 0.875rem; color: #6b7280;">
                                <span>{alert['location']['latitude']:.2f}, {alert['location']['longitude']:.2f}</span>
                                <span>{datetime.fromisoformat(alert['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}</span>
                                <span>{alert['type'].title()}</span>
                                <span>{'Read' if alert['isRead'] else 'Unread'}</span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Action buttons
                col_btn1, col_btn2, col_btn3, col_btn4 = st.columns([1, 1, 1, 3])
                
                with col_btn1:
                    if st.button(f"Mark {'Unread' if alert['isRead'] else 'Read'}", key=f"read_{alert['id']}"):
                        st.success(f"Alert marked as {'unread' if alert['isRead'] else 'read'}!")
                
                with col_btn2:
                    if st.button("View Details", key=f"details_{alert['id']}"):
                        show_alert_details(alert)
                
                with col_btn3:
                    if st.button("Resolve", key=f"resolve_{alert['id']}"):
                        st.success("Alert resolved!")
                
                st.write("")  # Add spacing
    
    # Alert Statistics
    st.divider()
    st.subheader("Alert Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Severity distribution
        severity_counts = {}
        for alert in alerts:
            severity = alert['severity']
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        if severity_counts:
            df_severity = pd.DataFrame(list(severity_counts.items()), columns=['Severity', 'Count'])
            st.bar_chart(df_severity.set_index('Severity'))
            st.caption("Alert Distribution by Severity")
    
    with col2:
        # Type distribution
        type_counts = {}
        for alert in alerts:
            alert_type = alert['type']
            type_counts[alert_type] = type_counts.get(alert_type, 0) + 1
        
        if type_counts:
            df_types = pd.DataFrame(list(type_counts.items()), columns=['Type', 'Count'])
            st.bar_chart(df_types.set_index('Type'))
            st.caption("Alert Distribution by Type")

def show_alert_details(alert):
    """Show detailed alert information in a modal"""
    with st.expander(f"🔍 Alert Details: {alert['title']}", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Alert Information:**")
            st.write(f"- **ID:** {alert['id']}")
            st.write(f"- **Type:** {alert['type'].title()}")
            st.write(f"- **Severity:** {alert['severity'].title()}")
            st.write(f"- **Status:** {'Read' if alert['isRead'] else 'Unread'}")
        
        with col2:
            st.write("**Location & Timing:**")
            st.write(f"- **Latitude:** {alert['location']['latitude']}")
            st.write(f"- **Longitude:** {alert['location']['longitude']}")
            st.write(f"- **Timestamp:** {datetime.fromisoformat(alert['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.write("**Description:**")
        st.write(alert['description'])
        
        # Recommended actions based on alert type
        st.write("**Recommended Actions:**")
        if alert['type'] == 'pollution':
            st.write("- Deploy additional monitoring bots to the area")
            st.write("- Notify environmental authorities")
            st.write("- Investigate potential pollution sources")
        elif alert['type'] == 'anomaly':
            st.write("- Verify sensor readings")
            st.write("- Check weather conditions")
            st.write("- Monitor adjacent areas")
        elif alert['type'] == 'equipment':
            st.write("- Schedule maintenance visit")
            st.write("- Check equipment diagnostics")
            st.write("- Deploy backup systems if available")
        else:
            st.write("- Review alert parameters")
            st.write("- Take appropriate safety measures")
            st.write("- Contact relevant authorities if needed")