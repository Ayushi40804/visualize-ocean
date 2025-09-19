import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.data_models import get_mock_agrobots, get_recent_data
import folium
from streamlit_folium import st_folium

def show_page():
    """Display the overview page"""
    st.title("Overview Dashboard")
    
    # Get data
    bots = get_mock_agrobots()
    recent_data = get_recent_data()
    selected_bot = st.session_state.get('selected_bot', None)
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        active_bots = len([b for b in bots if b['status'] == 'active'])
        st.metric(
            label="Active Agro-Bots",
            value=str(active_bots),
            delta="+2"
        )
    
    with col2:
        avg_temp = sum([b['data']['temperature'] for b in bots]) / len(bots)
        st.metric(
            label="Avg Ocean Temperature",
            value=f"{avg_temp:.1f}°C",
            delta="+0.3°C"
        )
    
    with col3:
        total_alerts = 3  # From mock data
        st.metric(
            label="Active Alerts",
            value=str(total_alerts),
            delta="-1"
        )
    
    with col4:
        data_points = "2.4M"
        st.metric(
            label="📡 Data Points",
            value=data_points,
            delta="+12K"
        )
    
    # Main content in two columns
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        # Real-time data chart
        st.subheader("📈 Real-time Ocean Data")
        st.caption("Last 30 minutes")
        
        # Create DataFrame for plotting
        df = pd.DataFrame(recent_data)
        
        # Temperature chart
        fig_temp = px.line(df, x='time', y='temperature', 
                          title='Temperature Trend',
                          labels={'temperature': 'Temperature (°C)', 'time': 'Time'})
        fig_temp.update_layout(height=200)
        st.plotly_chart(fig_temp, use_container_width=True)
        
        # Salinity and pH charts
        col_a, col_b = st.columns(2)
        with col_a:
            fig_sal = px.line(df, x='time', y='salinity',
                             title='Salinity (PSU)')
            fig_sal.update_layout(height=150)
            st.plotly_chart(fig_sal, use_container_width=True)
        
        with col_b:
            fig_ph = px.line(df, x='time', y='ph',
                            title='pH Level')
            fig_ph.update_layout(height=150)
            st.plotly_chart(fig_ph, use_container_width=True)
        
        # Recent data table
        st.subheader("📋 Recent Measurements")
        df_display = df.tail(5).copy()
        df_display['temperature'] = df_display['temperature'].round(1)
        df_display['salinity'] = df_display['salinity'].round(1)
        df_display['ph'] = df_display['ph'].round(1)
        st.dataframe(df_display, use_container_width=True)
    
    with col_right:
        # Interactive Map
        st.subheader("🗺️ Interactive Ocean Map")
        st.caption("Indian Ocean - Live Bot Locations")
        
        # Create map
        m = folium.Map(
            location=[-20.0, 57.5],  # Indian Ocean center
            zoom_start=6,
            tiles='OpenStreetMap'
        )
        
        # Add bot markers
        for bot in bots:
            # Determine marker color based on status
            color = 'green' if bot['status'] == 'active' else 'orange' if bot['status'] == 'maintenance' else 'red'
            
            # Create popup content
            popup_content = f"""
            <b>{bot['name']}</b><br>
            Status: {bot['status']}<br>
            Temperature: {bot['data']['temperature']}°C<br>
            Salinity: {bot['data']['salinity']} PSU<br>
            pH: {bot['data']['ph']}<br>
            Last Update: {datetime.fromisoformat(bot['lastUpdate']).strftime('%H:%M:%S')}
            """
            
            folium.Marker(
                location=[bot['latitude'], bot['longitude']],
                popup=folium.Popup(popup_content, max_width=200),
                tooltip=bot['name'],
                icon=folium.Icon(color=color, icon='info-sign')
            ).add_to(m)
            
            # Add data circles for temperature visualization
            folium.Circle(
                location=[bot['latitude'], bot['longitude']],
                radius=50000,  # 50km
                color='red' if bot['data']['temperature'] > 25 else 'blue',
                fillColor='red' if bot['data']['temperature'] > 25 else 'blue',
                fillOpacity=0.3,
                popup=f"Temperature Zone: {bot['data']['temperature']}°C"
            ).add_to(m)
        
        # Display map
        map_data = st_folium(m, width=700, height=400)
        
        # Selected Bot Details
        st.subheader("🤖 Selected Bot Details")
        
        if selected_bot:
            with st.container():
                st.write(f"**{selected_bot['name']}**")
                
                # Status indicator
                status_color = {"active": "🟢", "maintenance": "🟡", "offline": "🔴"}
                st.write(f"Status: {status_color.get(selected_bot['status'], '⚪')} {selected_bot['status'].title()}")
                
                # Data grid
                col_1, col_2 = st.columns(2)
                
                with col_1:
                    st.metric("🌡️ Temperature", f"{selected_bot['data']['temperature']}°C")
                    st.metric("💧 Salinity", f"{selected_bot['data']['salinity']} PSU")
                    st.metric("⚗️ pH Level", str(selected_bot['data']['ph']))
                
                with col_2:
                    st.metric("💨 Current Speed", f"{selected_bot['data']['currentSpeed']} m/s")
                    st.metric("🧭 Current Direction", f"{selected_bot['data']['currentDirection']}°")
                    st.metric("🏭 Pollution Index", str(selected_bot['data']['pollutionIndex']))
                
                # Last update
                last_update = datetime.fromisoformat(selected_bot['lastUpdate'])
                st.caption(f"Last updated: {last_update.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            st.info("Select an Agro-Bot from the sidebar to view detailed information.")
    
    # Statistics Summary
    st.divider()
    st.subheader("📈 Fleet Statistics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Status distribution
        status_counts = {}
        for bot in bots:
            status = bot['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        fig_status = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="Bot Status Distribution"
        )
        st.plotly_chart(fig_status, use_container_width=True)
    
    with col2:
        # Temperature distribution
        temps = [bot['data']['temperature'] for bot in bots]
        fig_temp_dist = px.histogram(
            x=temps,
            title="Temperature Distribution",
            labels={'x': 'Temperature (°C)', 'y': 'Count'}
        )
        st.plotly_chart(fig_temp_dist, use_container_width=True)
    
    with col3:
        # Pollution index comparison
        pollution_data = []
        for bot in bots:
            pollution_data.append({
                'Bot': bot['name'],
                'Pollution Index': bot['data']['pollutionIndex']
            })
        
        df_pollution = pd.DataFrame(pollution_data)
        fig_pollution = px.bar(
            df_pollution,
            x='Bot',
            y='Pollution Index',
            title="Pollution Index by Bot"
        )
        fig_pollution.update_xaxes(tickangle=45)
        st.plotly_chart(fig_pollution, use_container_width=True)