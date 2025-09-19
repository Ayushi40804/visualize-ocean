import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.data_models import get_real_argo_data, get_argo_summary_stats
import folium
from streamlit_folium import st_folium
import numpy as np

def show_page():
    """Display the overview page"""
    st.title("🌊 Ocean Data Overview Dashboard")
    st.caption("Real-time ARGO float data from the Indian Ocean")
    
    # Get real ARGO data
    argo_stats = get_argo_summary_stats()
    argo_data = get_real_argo_data(limit=200)
    
    # Check if we have data
    if argo_stats['total_measurements'] == 0:
        st.warning("⚠️ No ARGO data available. Please ensure the database is populated.")
        return
    
    # Data source indicator
    if argo_stats['total_measurements'] > 0:
        st.success(f"✅ **Real ARGO Data Active** - {argo_stats['total_measurements']:,} measurements from {argo_stats['unique_floats']} floats")
        date_range = f"{argo_stats['earliest_date']} to {argo_stats['latest_date']}"
        st.info(f"📅 **Data Period**: {date_range}")
    
    # KPI Metrics using real ARGO data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🚢 Active ARGO Floats",
            value=str(argo_stats['unique_floats']),
            delta=f"{argo_stats['total_measurements']:,} measurements"
        )
    
    with col2:
        st.metric(
            label="🌡️ Avg Ocean Temperature",
            value=f"{argo_stats['avg_temperature']:.1f}°C",
            delta="Real-time"
        )
    
    with col3:
        st.metric(
            label="🧂 Avg Salinity",
            value=f"{argo_stats['avg_salinity']:.1f} PSU",
            delta="Real-time"
        )
    
    with col4:
        st.metric(
            label="🌐 Ocean Regions",
            value=str(len(argo_stats['regional_breakdown'])),
            delta="Covered areas"
        )
    
    # Main content in two columns
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        # Real-time ARGO data charts
        st.subheader("📈 Real ARGO Oceanographic Data")
        st.caption("Recent measurements from ARGO floats")
        
        if not argo_data.empty:
            # Convert date_time to datetime
            argo_data['date_time'] = pd.to_datetime(argo_data['date_time'])
            
            # Sample data for time series (take most recent 50 points)
            time_series_data = argo_data.head(50).sort_values('date_time')
            
            # Temperature chart
            fig_temp = px.line(time_series_data, x='date_time', y='temperature', 
                              color='region',
                              title='Temperature Measurements',
                              labels={'temperature': 'Temperature (°C)', 'date_time': 'Date & Time'})
            fig_temp.update_layout(height=250)
            st.plotly_chart(fig_temp, use_container_width=True)
            
            # Salinity and pH charts
            col_a, col_b = st.columns(2)
            with col_a:
                fig_sal = px.line(time_series_data, x='date_time', y='salinity',
                                 color='region',
                                 title='Salinity (PSU)',
                                 labels={'salinity': 'Salinity (PSU)', 'date_time': 'Date & Time'})
                fig_sal.update_layout(height=200)
                st.plotly_chart(fig_sal, use_container_width=True)
            
            with col_b:
                if 'ph' in time_series_data.columns and time_series_data['ph'].notna().any():
                    fig_ph = px.line(time_series_data, x='date_time', y='ph',
                                    color='region',
                                    title='pH Level',
                                    labels={'ph': 'pH Level', 'date_time': 'Date & Time'})
                    fig_ph.update_layout(height=200)
                    st.plotly_chart(fig_ph, use_container_width=True)
                else:
                    st.info("pH data not available for selected measurements")
            
            # Recent measurements table
            st.subheader("📋 Recent ARGO Measurements")
            display_data = argo_data.head(10).copy()
            display_data['temperature'] = display_data['temperature'].round(2)
            display_data['salinity'] = display_data['salinity'].round(2)
            display_data['latitude'] = display_data['latitude'].round(3)
            display_data['longitude'] = display_data['longitude'].round(3)
            display_data['depth'] = display_data['depth'].round(1)
            
            # Select and rename columns for display
            display_columns = ['float_id', 'region', 'date_time', 'latitude', 'longitude', 
                             'temperature', 'salinity', 'depth']
            display_data = display_data[display_columns].rename(columns={
                'float_id': 'Float ID',
                'region': 'Region',
                'date_time': 'Date & Time',
                'latitude': 'Latitude',
                'longitude': 'Longitude',
                'temperature': 'Temperature (°C)',
                'salinity': 'Salinity (PSU)',
                'depth': 'Depth (m)'
            })
            st.dataframe(display_data, use_container_width=True)
        else:
            st.warning("No ARGO data available for charts")
    
    with col_right:
        # Interactive Map with real ARGO float locations
        st.subheader("🗺️ ARGO Float Locations")
        st.caption("Real ARGO float positions in the Indian Ocean")
        
        if not argo_data.empty:
            # Get unique float locations to avoid map overcrowding
            unique_locations = argo_data.groupby(['float_id', 'latitude', 'longitude']).agg({
                'temperature': 'mean',
                'salinity': 'mean',
                'date_time': 'count',
                'region': 'first'
            }).reset_index()
            unique_locations.columns = ['float_id', 'latitude', 'longitude', 'avg_temp', 'avg_sal', 'measurements', 'region']
            
            # Create map centered on Indian Ocean
            m = folium.Map(
                location=[15.0, 75.0],  # Central Indian Ocean
                zoom_start=4,
                tiles="OpenStreetMap"
            )
            
            # Color mapping for regions
            region_colors = {
                'Arabian Sea': 'red',
                'Bay of Bengal': 'blue', 
                'Indian Ocean': 'green'
            }
            
            # Add markers for each ARGO float location
            for _, location in unique_locations.iterrows():
                color = region_colors.get(location['region'], 'gray')
                
                folium.CircleMarker(
                    location=[location['latitude'], location['longitude']],
                    radius=8,
                    popup=f"""
                    <b>ARGO Float:</b> {location['float_id']}<br>
                    <b>Region:</b> {location['region']}<br>
                    <b>Measurements:</b> {location['measurements']}<br>
                    <b>Avg Temperature:</b> {location['avg_temp']:.2f}°C<br>
                    <b>Avg Salinity:</b> {location['avg_sal']:.2f} PSU<br>
                    <b>Location:</b> {location['latitude']:.2f}°N, {location['longitude']:.2f}°E
                    """,
                    color=color,
                    fillColor=color,
                    fillOpacity=0.7,
                    tooltip=f"ARGO Float {location['float_id']}"
                ).add_to(m)
            
            # Display map
            map_data = st_folium(m, width=700, height=400)
        else:
            st.warning("No ARGO data available for map")
        
        # Selected Float Details
        st.subheader("🚢 ARGO Float Information")
        
        if not argo_data.empty:
            # Get unique floats for selection
            unique_floats = argo_data['float_id'].unique()
            selected_float = st.selectbox("Select an ARGO Float:", unique_floats)
            
            if selected_float:
                float_data = argo_data[argo_data['float_id'] == selected_float].iloc[0]
                
                st.write(f"**ARGO Float {selected_float}**")
                st.write(f"Region: 🌊 {float_data['region']}")
                
                # Float metrics
                col_1, col_2 = st.columns(2)
                
                with col_1:
                    st.metric("🌡️ Temperature", f"{float_data['temperature']:.2f}°C")
                    st.metric("💧 Salinity", f"{float_data['salinity']:.2f} PSU")
                    if pd.notna(float_data.get('ph')):
                        st.metric("pH Level", f"{float_data['ph']:.2f}")
                    else:
                        st.metric("pH Level", "N/A")
                
                with col_2:
                    st.metric("🌊 Depth", f"{float_data['depth']:.1f} m")
                    st.metric("📍 Latitude", f"{float_data['latitude']:.3f}°")
                    st.metric("📍 Longitude", f"{float_data['longitude']:.3f}°")
                
                # Last measurement time
                measurement_time = pd.to_datetime(float_data['date_time'])
                st.caption(f"Last measurement: {measurement_time.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            st.info("No ARGO float data available.")
    
    # Statistics Summary using real ARGO data
    st.divider()
    st.subheader("📈 ARGO Data Statistics")
    
    if not argo_data.empty and argo_stats['regional_breakdown']:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Regional distribution
            regional_df = pd.DataFrame(argo_stats['regional_breakdown'])
            
            fig_regional = px.pie(
                regional_df,
                values='count',
                names='region',
                title="Regional Data Distribution",
                color_discrete_map={
                    'Arabian Sea': '#ff7f0e',
                    'Bay of Bengal': '#1f77b4', 
                    'Indian Ocean': '#2ca02c'
                }
            )
            st.plotly_chart(fig_regional, use_container_width=True)
        
        with col2:
            # Temperature distribution
            fig_temp_dist = px.histogram(
                argo_data.head(1000),  # Sample for performance
                x='temperature',
                title="Temperature Distribution",
                labels={'temperature': 'Temperature (°C)', 'count': 'Count'},
                nbins=20,
                color_discrete_sequence=['#ff7f0e']
            )
            st.plotly_chart(fig_temp_dist, use_container_width=True)
        
        with col3:
            # Regional temperature comparison
            regional_temp_data = []
            for region_data in argo_stats['regional_breakdown']:
                regional_temp_data.append({
                    'Region': region_data['region'],
                    'Avg Temperature': region_data['avg_temperature'],
                    'Measurements': region_data['count']
                })
            
            df_regional_temp = pd.DataFrame(regional_temp_data)
            fig_regional_temp = px.bar(
                df_regional_temp,
                x='Region',
                y='Avg Temperature',
                title="Avg Temperature by Region",
                labels={'Avg Temperature': 'Temperature (°C)'},
                color='Avg Temperature',
                color_continuous_scale='RdYlBu_r'
            )
            fig_regional_temp.update_xaxes(tickangle=45)
            st.plotly_chart(fig_regional_temp, use_container_width=True)
        
        # Additional depth vs temperature analysis
        st.subheader("🌊 Depth Analysis")
        col1, col2 = st.columns(2)
        
        with col1:
            # Sample data for depth analysis
            depth_sample = argo_data.head(500)
            fig_depth_temp = px.scatter(
                depth_sample,
                x='temperature',
                y='depth',
                color='region',
                title='Temperature vs Depth Profile',
                labels={'temperature': 'Temperature (°C)', 'depth': 'Depth (m)'},
                color_discrete_map={
                    'Arabian Sea': 'red',
                    'Bay of Bengal': 'blue', 
                    'Indian Ocean': 'green'
                }
            )
            fig_depth_temp.update_layout(yaxis=dict(autorange="reversed"))  # Depth increases downward
            st.plotly_chart(fig_depth_temp, use_container_width=True)
        
        with col2:
            # Salinity vs depth
            fig_depth_sal = px.scatter(
                depth_sample,
                x='salinity',
                y='depth',
                color='region',
                title='Salinity vs Depth Profile',
                labels={'salinity': 'Salinity (PSU)', 'depth': 'Depth (m)'},
                color_discrete_map={
                    'Arabian Sea': 'red',
                    'Bay of Bengal': 'blue', 
                    'Indian Ocean': 'green'
                }
            )
            fig_depth_sal.update_layout(yaxis=dict(autorange="reversed"))  # Depth increases downward
            st.plotly_chart(fig_depth_sal, use_container_width=True)
    else:
        st.info("Insufficient data for statistical analysis")
