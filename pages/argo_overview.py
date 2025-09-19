import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils.data_models import get_real_argo_data, get_argo_summary_stats
import folium
from streamlit_folium import st_folium
import numpy as np

def show_real_argo_overview():
    """Display overview page with real ARGO data"""
    st.title("Indian Ocean ARGO Data Overview")
    st.caption("Real oceanographic data from ARGO floats - January 2024")
    
    # Get real ARGO data and stats
    argo_stats = get_argo_summary_stats()
    argo_data = get_real_argo_data(limit=500)
    
    # Data source indicator
    if argo_stats['total_measurements'] > 0:
        st.success(f"**Real ARGO Data Active** - {argo_stats['total_measurements']:,} measurements from {argo_stats['unique_floats']} floats")
        date_range = f"{argo_stats['earliest_date']} to {argo_stats['latest_date']}"
        st.info(f"**Data Period**: {date_range}")
    else:
        st.warning("No ARGO data available")
        return
    
    # KPI Metrics using real ARGO data
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Active ARGO Floats",
            value=str(argo_stats['unique_floats']),
            delta=f"{argo_stats['total_measurements']:,} measurements"
        )
    
    with col2:
        st.metric(
            label="Avg Ocean Temperature",
            value=f"{argo_stats['avg_temperature']:.1f}°C",
            delta="Real-time"
        )
    
    with col3:
        st.metric(
            label="Avg Salinity",
            value=f"{argo_stats['avg_salinity']:.1f} PSU",
            delta="Real-time"
        )
    
    with col4:
        st.metric(
            label=" Ocean Regions",
            value=str(len(argo_stats['regional_breakdown'])),
            delta="Covered areas"
        )
    
    # Regional breakdown
    st.subheader(" Regional Data Summary")
    
    if argo_stats['regional_breakdown']:
        regional_df = pd.DataFrame(argo_stats['regional_breakdown'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Regional temperature chart
            fig_temp = px.bar(regional_df, x='region', y='avg_temperature',
                             title='Average Temperature by Region',
                             labels={'avg_temperature': 'Temperature (°C)', 'region': 'Region'},
                             color='avg_temperature',
                             color_continuous_scale='RdYlBu_r')
            st.plotly_chart(fig_temp, use_container_width=True)
        
        with col2:
            # Regional salinity chart
            fig_sal = px.bar(regional_df, x='region', y='avg_salinity',
                            title='Average Salinity by Region',
                            labels={'avg_salinity': 'Salinity (PSU)', 'region': 'Region'},
                            color='avg_salinity',
                            color_continuous_scale='Blues')
            st.plotly_chart(fig_sal, use_container_width=True)
        
        # Regional data table
        st.subheader("📋 Regional Statistics")
        for region_data in argo_stats['regional_breakdown']:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(f"📍 {region_data['region']}", f"{region_data['count']:,} measurements")
            with col2:
                st.metric("🌡️ Avg Temp", f"{region_data['avg_temperature']:.1f}°C")
            with col3:
                st.metric("🧂 Avg Salinity", f"{region_data['avg_salinity']:.1f} PSU")
            with col4:
                percentage = (region_data['count'] / argo_stats['total_measurements']) * 100
                st.metric("📊 Coverage", f"{percentage:.1f}%")
    
    # Time series charts
    if not argo_data.empty:
        st.subheader("📈 Oceanographic Measurements Over Time")
        
        # Convert date_time to datetime
        argo_data['date_time'] = pd.to_datetime(argo_data['date_time'])
        
        # Sample data for visualization (to avoid overcrowding)
        if len(argo_data) > 1000:
            sample_data = argo_data.sample(n=1000).sort_values('date_time')
        else:
            sample_data = argo_data.sort_values('date_time')
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Temperature over time
            fig_temp_time = px.scatter(sample_data, x='date_time', y='temperature',
                                      color='region',
                                      title='Temperature Measurements',
                                      labels={'temperature': 'Temperature (°C)', 'date_time': 'Date & Time'},
                                      hover_data=['float_id', 'depth'])
            st.plotly_chart(fig_temp_time, use_container_width=True)
        
        with col2:
            # Salinity over time
            fig_sal_time = px.scatter(sample_data, x='date_time', y='salinity',
                                     color='region',
                                     title='Salinity Measurements',
                                     labels={'salinity': 'Salinity (PSU)', 'date_time': 'Date & Time'},
                                     hover_data=['float_id', 'depth'])
            st.plotly_chart(fig_sal_time, use_container_width=True)
        
        # Temperature vs Depth profile
        st.subheader("🌊 Ocean Depth Profiles")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Temperature vs depth
            fig_temp_depth = px.scatter(sample_data, x='temperature', y='depth',
                                       color='region',
                                       title='Temperature vs Depth Profile',
                                       labels={'temperature': 'Temperature (°C)', 'depth': 'Depth (m)'},
                                       hover_data=['float_id'])
            fig_temp_depth.update_yaxis(autorange="reversed")  # Depth increases downward
            st.plotly_chart(fig_temp_depth, use_container_width=True)
        
        with col2:
            # Salinity vs depth
            fig_sal_depth = px.scatter(sample_data, x='salinity', y='depth',
                                      color='region',
                                      title='Salinity vs Depth Profile',
                                      labels={'salinity': 'Salinity (PSU)', 'depth': 'Depth (m)'},
                                      hover_data=['float_id'])
            fig_sal_depth.update_yaxis(autorange="reversed")  # Depth increases downward
            st.plotly_chart(fig_sal_depth, use_container_width=True)
    
    # Interactive map of ARGO float locations
    st.subheader("🗺️ ARGO Float Locations")
    st.caption("January 2024 measurement locations in the Indian Ocean")
    
    if not argo_data.empty:
        # Sample unique locations to avoid map overcrowding
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
        
        # Add markers for each float location
        for _, location in unique_locations.iterrows():
            color = region_colors.get(location['region'], 'gray')
            
            folium.CircleMarker(
                location=[location['latitude'], location['longitude']],
                radius=8,
                popup=f"""
                <b>Float ID:</b> {location['float_id']}<br>
                <b>Region:</b> {location['region']}<br>
                <b>Measurements:</b> {location['measurements']}<br>
                <b>Avg Temperature:</b> {location['avg_temp']:.2f}°C<br>
                <b>Avg Salinity:</b> {location['avg_sal']:.2f} PSU<br>
                <b>Location:</b> {location['latitude']:.2f}°N, {location['longitude']:.2f}°E
                """,
                color=color,
                fillColor=color,
                fillOpacity=0.7
            ).add_to(m)
        
        # Display map
        map_data = st_folium(m, width=700, height=500)
    
    # Data table with recent measurements
    st.subheader("📋 Recent ARGO Measurements")
    
    if not argo_data.empty:
        # Show recent measurements
        display_data = argo_data.head(20).copy()
        display_data['temperature'] = display_data['temperature'].round(2)
        display_data['salinity'] = display_data['salinity'].round(2)
        display_data['latitude'] = display_data['latitude'].round(3)
        display_data['longitude'] = display_data['longitude'].round(3)
        display_data['depth'] = display_data['depth'].round(1)
        
        # Rename columns for better display
        display_data = display_data[['float_id', 'region', 'date_time', 'latitude', 'longitude', 
                                   'temperature', 'salinity', 'depth']].rename(columns={
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

if __name__ == "__main__":

    show_real_argo_overview()
