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
            start_lat = st.number_input("Latitude", value=19.0760, format="%.4f", key="start_lat")
            start_lon = st.number_input("Longitude", value=72.8777, format="%.4f", key="start_lon")
            start_port = st.text_input("Port Name", value="Mumbai", key="start_port")
        
        with col2:
            st.subheader("Destination")
            end_lat = st.number_input("Latitude", value=-20.1619, format="%.4f", key="end_lat")
            end_lon = st.number_input("Longitude", value=57.5012, format="%.4f", key="end_lon")
            end_port = st.text_input("Port Name", value="Port Louis", key="end_port")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            vessel_type = st.selectbox("Vessel Type", ["Container Ship", "Bulk Carrier", "Tanker", "Fishing Vessel"])
        with col2:
            cargo_weight = st.number_input("Cargo Weight (tons)", value=5000, min_value=0)
        with col3:
            priority = st.selectbox("Optimization Priority", ["Fuel Efficiency", "Time", "Safety", "Weather"])
        
        if st.button("🧠 Optimize Route", type="primary"):
            with st.spinner("Calculating optimal route..."):
                st.success("Route optimized successfully!")
                st.balloons()
    
    # Route selection
    st.divider()
    st.subheader("📋 Available Routes")
    
    if routes:
        selected_route = st.selectbox(
            "Select a route to view details:",
            routes,
            format_func=lambda x: x['name']
        )
        
        if selected_route:
            # Route details
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Route map visualization
                st.subheader("🗺️ Route Visualization")
                
                # Create a simple route map using plotly
                path_df = pd.DataFrame(selected_route['optimizedPath'])
                
                fig = go.Figure()
                
                # Add the route line
                fig.add_trace(go.Scattermapbox(
                    mode="markers+lines",
                    lon=path_df['longitude'],
                    lat=path_df['latitude'],
                    marker={'size': 8, 'color': 'blue'},
                    line={'width': 3, 'color': 'blue'},
                    name="Optimized Route"
                ))
                
                # Add start and end markers
                fig.add_trace(go.Scattermapbox(
                    mode="markers",
                    lon=[selected_route['startPoint']['longitude']],
                    lat=[selected_route['startPoint']['latitude']],
                    marker={'size': 15, 'color': 'green'},
                    name="Start",
                    text=["Start Point"]
                ))
                
                fig.add_trace(go.Scattermapbox(
                    mode="markers",
                    lon=[selected_route['endPoint']['longitude']],
                    lat=[selected_route['endPoint']['latitude']],
                    marker={'size': 15, 'color': 'red'},
                    name="End",
                    text=["End Point"]
                ))
                
                fig.update_layout(
                    mapbox_style="open-street-map",
                    mapbox=dict(
                        center=dict(
                            lat=(selected_route['startPoint']['latitude'] + selected_route['endPoint']['latitude']) / 2,
                            lon=(selected_route['startPoint']['longitude'] + selected_route['endPoint']['longitude']) / 2
                        ),
                        zoom=3
                    ),
                    height=400,
                    margin={"r":0,"t":0,"l":0,"b":0}
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Route metrics
                st.subheader("📊 Route Metrics")
                
                st.metric(
                    label="⏱️ Estimated Time",
                    value=selected_route['estimatedTime']
                )
                
                st.metric(
                    label="Fuel Savings",
                    value=f"{selected_route['fuelSavings']}%"
                )
                
                st.metric(
                    label="🌤️ Weather Conditions",
                    value=selected_route['weatherConditions']
                )
                
                # Route waypoints
                st.subheader("📍 Waypoints")
                for i, point in enumerate(selected_route['optimizedPath']):
                    if i == 0:
                        st.write(f"🟢 Start: {point['latitude']:.3f}, {point['longitude']:.3f}")
                    elif i == len(selected_route['optimizedPath']) - 1:
                        st.write(f"🔴 End: {point['latitude']:.3f}, {point['longitude']:.3f}")
                    else:
                        st.write(f"🔵 WP{i}: {point['latitude']:.3f}, {point['longitude']:.3f}")
    
    # Route analytics
    st.divider()
    st.subheader("📈 Route Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Fuel savings comparison
        route_names = [route['name'] for route in routes]
        fuel_savings = [route['fuelSavings'] for route in routes]
        
        fig_fuel = px.bar(
            x=route_names,
            y=fuel_savings,
            title="Fuel Savings by Route (%)",
            labels={'x': 'Route', 'y': 'Fuel Savings (%)'}
        )
        fig_fuel.update_xaxes(tickangle=45)
        st.plotly_chart(fig_fuel, use_container_width=True)
    
    with col2:
        # Weather conditions distribution
        weather_conditions = [route['weatherConditions'] for route in routes]
        weather_counts = {}
        for condition in weather_conditions:
            weather_counts[condition] = weather_counts.get(condition, 0) + 1
        
        fig_weather = px.pie(
            values=list(weather_counts.values()),
            names=list(weather_counts.keys()),
            title="Weather Conditions Distribution"
        )
        st.plotly_chart(fig_weather, use_container_width=True)
    
    with col3:
        # Route efficiency metrics
        st.write("**Route Efficiency Metrics**")
        total_routes = len(routes)
        avg_fuel_savings = sum(fuel_savings) / len(fuel_savings) if fuel_savings else 0
        
        st.metric("Total Routes", total_routes)
        st.metric("Avg Fuel Savings", f"{avg_fuel_savings:.1f}%")
        st.metric("Optimization Rate", "94.2%")
    
    # Advanced features
    st.divider()
    st.subheader("🔧 Advanced Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌊 Ocean Current Analysis")
        
        # Mock current data
        current_data = {
            'Region': ['North Indian Ocean', 'South Indian Ocean', 'Arabian Sea', 'Bay of Bengal'],
            'Current Speed (m/s)': [0.8, 1.2, 0.6, 0.9],
            'Direction (°)': [120, 95, 140, 110],
            'Impact on Route': ['Moderate', 'High', 'Low', 'Moderate']
        }
        
        df_currents = pd.DataFrame(current_data)
        st.dataframe(df_currents, use_container_width=True)
        
        # Current speed chart
        fig_current = px.bar(
            df_currents,
            x='Region',
            y='Current Speed (m/s)',
            title="Ocean Current Speeds by Region"
        )
        st.plotly_chart(fig_current, use_container_width=True)
    
    with col2:
        st.subheader("🌪️ Weather Impact Assessment")
        
        # Mock weather data
        weather_data = {
            'Date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18'],
            'Wind Speed (km/h)': [25, 30, 15, 20],
            'Wave Height (m)': [2.1, 2.8, 1.5, 1.9],
            'Visibility (km)': [10, 8, 15, 12],
            'Route Impact': ['Low', 'Medium', 'Low', 'Low']
        }
        
        df_weather = pd.DataFrame(weather_data)
        st.dataframe(df_weather, use_container_width=True)
        
        # Weather trend chart
        fig_weather_trend = px.line(
            df_weather,
            x='Date',
            y=['Wind Speed (km/h)', 'Wave Height (m)'],
            title="Weather Trends"
        )
        st.plotly_chart(fig_weather_trend, use_container_width=True)
    
    # Real-time updates
    st.divider()
    with st.container():
        st.subheader("🔄 Real-time Route Updates")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Refresh Routes", type="secondary"):
                st.success("Routes refreshed!")
        
        with col2:
            if st.button("📡 Update Weather Data", type="secondary"):
                st.success("Weather data updated!")
        
        with col3:
            if st.button("🌊 Update Ocean Conditions", type="secondary"):
                st.success("Ocean conditions updated!")
        
        # Status indicators
        st.write("**System Status:**")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write("🟢 Route Optimization: Online")
        with col2:
            st.write("🟢 Weather API: Connected")
        with col3:
            st.write("🟢 Ocean Data: Real-time")
        with col4:
            st.write("🟢 Navigation: Active")