import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.data_models import get_mock_routes

def show_page():
    """Display the route optimization page"""
    st.title("Route Optimization")
    st.caption("AI-powered maritime route planning and optimization")
    
    # Get route data
    routes = get_mock_routes()
    
    # Route planning form
    with st.expander("Plan New Route", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Starting Point")
            start_lat = st.number_input("Start Latitude", value=19.0760, step=0.001, format="%.3f")
            start_lon = st.number_input("Start Longitude", value=72.8777, step=0.001, format="%.3f")
            
        with col2:
            st.subheader("Destination")
            end_lat = st.number_input("End Latitude", value=-20.1619, step=0.001, format="%.3f")
            end_lon = st.number_input("End Longitude", value=57.5012, step=0.001, format="%.3f")
        
        col3, col4 = st.columns(2)
        with col3:
            departure_date = st.date_input("Departure Date", value=datetime.now().date())
            vessel_type = st.selectbox("Vessel Type", ["Cargo Ship", "Tanker", "Container Ship", "Bulk Carrier"])
            
        with col4:
            priority = st.selectbox("Optimization Priority", ["Fuel Efficiency", "Shortest Time", "Safest Route", "Weather Avoidance"])
            cargo_weight = st.number_input("Cargo Weight (tons)", value=5000, step=100)
        
        if st.button("Calculate Optimal Route", type="primary"):
            with st.spinner("Calculating optimal route..."):
                # Simulate route calculation
                import time
                time.sleep(2)
                st.success("Route calculated successfully! Results shown below.")
                
                # Add mock route visualization
                st.subheader("Route Visualization")
                
                # Create a simple map using plotly
                fig = go.Figure()
                
                # Add route line
                route_lats = [start_lat, (start_lat + end_lat)/2, end_lat]
                route_lons = [start_lon, (start_lon + end_lon)/2, end_lon]
                
                fig.add_trace(go.Scattermapbox(
                    lat=route_lats,
                    lon=route_lons,
                    mode='lines+markers',
                    line=dict(width=3, color='blue'),
                    marker=dict(size=10, color=['green', 'yellow', 'red']),
                    name='Optimal Route'
                ))
                
                fig.update_layout(
                    mapbox=dict(
                        style='open-street-map',
                        center=dict(lat=(start_lat + end_lat)/2, lon=(start_lon + end_lon)/2),
                        zoom=3
                    ),
                    height=400,
                    margin=dict(l=0, r=0, t=0, b=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Route metrics
                st.subheader("Route Metrics")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric(
                        label="Estimated Time",
                        value="14d 6h",
                        delta="-2d 4h"
                    )
                with col2:
                    st.metric(
                        label="Distance",
                        value="3,247 nm",
                        delta="-156 nm"
                    )
                with col3:
                    st.metric(
                        label="Fuel Savings",
                        value="15.2%",
                        delta="2.1%"
                    )
                with col4:
                    st.metric(
                        label="Weather Conditions",
                        value="Favorable",
                        delta="Good"
                    )
                
                # Waypoint details
                with st.expander("Waypoint Details"):
                    waypoints = [(start_lat, start_lon), ((start_lat + end_lat)/2, (start_lon + end_lon)/2), (end_lat, end_lon)]
                    for i, point in enumerate(waypoints):
                        if i == 0:
                            st.write(f"Start: {point[0]:.3f}, {point[1]:.3f}")
                        elif i == len(waypoints) - 1:
                            st.write(f"End: {point[0]:.3f}, {point[1]:.3f}")
                        else:
                            st.write(f"WP{i}: {point[0]:.3f}, {point[1]:.3f}")
    
    # Route Analytics
    st.subheader("Route Analytics")
    
    # Historical route performance
    col1, col2 = st.columns(2)
    
    with col1:
        # Fuel efficiency chart
        efficiency_data = pd.DataFrame({
            'Route': ['Mumbai-Port Louis', 'Chennai-Colombo', 'Kochi-Male', 'Paradip-Chittagong'],
            'Fuel Savings (%)': [15.2, 8.7, 12.1, 6.5],
            'Distance (nm)': [3247, 654, 892, 1156]
        })
        
        fig = px.bar(efficiency_data, x='Route', y='Fuel Savings (%)', 
                     title='Fuel Savings by Route',
                     color='Fuel Savings (%)',
                     color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Weather impact chart
        weather_data = pd.DataFrame({
            'Conditions': ['Clear', 'Partly Cloudy', 'Overcast', 'Light Rain', 'Heavy Seas'],
            'Delay Hours': [0, 2, 8, 24, 72],
            'Frequency (%)': [45, 25, 15, 10, 5]
        })
        
        fig = px.scatter(weather_data, x='Frequency (%)', y='Delay Hours',
                        size='Frequency (%)', color='Conditions',
                        title='Weather Impact on Routes')
        st.plotly_chart(fig, use_container_width=True)
    
    # Current routes table
    st.subheader("Current Active Routes")
    
    routes_df = pd.DataFrame(routes)
    if not routes_df.empty:
        # Create a simplified dataframe for display
        display_df = pd.DataFrame({
            'Route Name': [route['name'] for route in routes],
            'Estimated Time': [route['estimatedTime'] for route in routes],
            'Fuel Savings': [f"{route['fuelSavings']}%" for route in routes],
            'Weather': [route['weatherConditions'] for route in routes]
        })
        
        st.dataframe(display_df, use_container_width=True)
    
    # Advanced Features
    st.subheader("Advanced Features")
    
    tab1, tab2, tab3 = st.tabs(["Ocean Current Analysis", "Weather Impact", "System Status"])
    
    with tab1:
        st.subheader("Ocean Current Analysis")
        
        # Create mock current data
        current_data = pd.DataFrame({
            'Time': pd.date_range('2023-01-01', periods=24, freq='H'),
            'Current Speed (m/s)': [0.5 + 0.3 * np.sin(i/4) for i in range(24)],
            'Direction (degrees)': [120 + 30 * np.sin(i/6) for i in range(24)]
        })
        
        fig = px.line(current_data, x='Time', y='Current Speed (m/s)',
                     title='Ocean Current Speed (24h forecast)')
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Current Speed", "0.8 m/s", "0.1 m/s")
        with col2:
            st.metric("Dominant Direction", "125°", "5°")
    
    with tab2:
        st.subheader("Weather Impact Assessment")
        
        # Weather forecast data
        weather_forecast = pd.DataFrame({
            'Date': pd.date_range('2023-01-01', periods=7, freq='D'),
            'Wind Speed (km/h)': [15, 22, 18, 35, 28, 12, 16],
            'Wave Height (m)': [1.2, 1.8, 1.5, 3.2, 2.4, 0.9, 1.1],
            'Visibility (km)': [15, 12, 18, 8, 10, 20, 18]
        })
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(weather_forecast, x='Date', y='Wind Speed (km/h)',
                         title='Wind Speed Forecast')
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            fig = px.line(weather_forecast, x='Date', y='Wave Height (m)',
                         title='Wave Height Forecast', color_discrete_sequence=['red'])
            st.plotly_chart(fig, use_container_width=True)
        
        # Weather alerts
        st.warning("High seas expected on Day 4 (Wave height: 3.2m)")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Conditions", "Good", "Improving")
        with col2:
            st.metric("48h Outlook", "Moderate", "Stable")
        with col3:
            st.metric("Storm Risk", "Low", "Decreasing")
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**System Performance**")
            if st.button("Update Ocean Conditions", type="secondary"):
                st.success("Ocean conditions updated!")
            
            st.write("**Data Sources**")
            st.write("NOAA Ocean Service")
            st.write("European Weather Centre")
            st.write("Maritime Traffic Database")
            
        with col2:
            st.write("**Service Status**")
            st.write("Route Optimization: Online")
            st.write("Weather API: Connected")
            st.write("Ocean Data: Real-time")
            st.write("Navigation: Active")

# Import numpy for calculations
import numpy as np