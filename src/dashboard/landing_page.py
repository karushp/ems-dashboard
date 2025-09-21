"""
Landing page components for the EMS Dashboard
"""

import os

import pandas as pd
import plotly.express as px
import streamlit as st

# Removed data loading imports for lazy loading
# from src.dashboard.metrics_calculator import get_all_dashboard_metrics
# from src.data.data_loader import load_parquet_data


def create_japan_map_data():
    """Create static data for st.map showing Kansai and Kanto regions"""

    # Static region coordinates - no data loading
    regions_data = {
        "Kansai": {
            "lat": 34.6937,
            "lon": 135.5023,
            "transport_records": "Available",
            "warehouse_records": "Available",
        },
        "Kanto": {
            "lat": 35.6762,
            "lon": 139.6503,
            "transport_records": "Available",
            "warehouse_records": "Available",
        },
    }

    # Create DataFrame for st.map
    map_data = []
    for region, data in regions_data.items():
        map_data.append(
            {
                "lat": data["lat"],
                "lon": data["lon"],
                "region": region,
                "transport_records": data["transport_records"],
                "warehouse_records": data["warehouse_records"],
            }
        )

    return pd.DataFrame(map_data)


def create_metric_card(metrics):
    """Create HTML for a metric card"""
    return f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h3 style="margin: 0 0 0.5rem 0; font-size: 1.1rem;">{metrics['region']} {metrics['industry']}</h3>
        <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">{metrics['total_records']:,}</div>
        <div style="font-size: 0.9rem; opacity: 0.9;">Total Records</div>
        <div style="font-size: 1.2rem; margin-top: 0.5rem;">{metrics['avg_energy']:.1f} kWh</div>
        <div style="font-size: 0.8rem; opacity: 0.8;">Avg Energy</div>
    </div>
    """


def create_overview_charts(all_metrics):
    """Create overview charts for the landing page"""
    # Extract data for charts
    labels = [f"{m['region']} {m['industry']}" for m in all_metrics]
    total_records = [m["total_records"] for m in all_metrics]
    avg_energy = [m["avg_energy"] for m in all_metrics]

    # Create two columns for side-by-side charts
    col1, col2 = st.columns(2)

    with col1:
        # Total records bar chart
        fig_records = px.bar(
            x=labels,
            y=total_records,
            title="Total Records by Region & Industry",
            color=total_records,
            color_continuous_scale="Viridis",
            labels={"x": "Region & Industry", "y": "Total Records"},
        )
        fig_records.update_layout(
            title_font=dict(color="#333333"),
            xaxis_title_font=dict(color="#333333"),
            yaxis_title_font=dict(color="#333333"),
            xaxis_tickfont=dict(color="#333333"),
            yaxis_tickfont=dict(color="#333333"),
            showlegend=False,
            height=400,
        )
        fig_records.update_xaxes(tickangle=45)
        st.plotly_chart(fig_records, width="stretch", key="overview_records")

    with col2:
        # Average energy consumption bar chart
        fig_energy = px.bar(
            x=labels,
            y=avg_energy,
            title="Average Energy Consumption by Region & Industry",
            color=avg_energy,
            color_continuous_scale="Plasma",
            labels={"x": "Region & Industry", "y": "Average Energy (kWh)"},
        )
        fig_energy.update_layout(
            title_font=dict(color="#333333"),
            xaxis_title_font=dict(color="#333333"),
            yaxis_title_font=dict(color="#333333"),
            xaxis_tickfont=dict(color="#333333"),
            yaxis_tickfont=dict(color="#333333"),
            showlegend=False,
            height=400,
        )
        fig_energy.update_xaxes(tickangle=45)
        st.plotly_chart(fig_energy, width="stretch", key="overview_energy")

    # Add a summary table
    st.markdown("---")
    st.subheader("Summary Statistics")

    # Create summary DataFrame
    summary_data = []
    for m in all_metrics:
        summary_data.append(
            {
                "Region": m["region"],
                "Industry": m["industry"],
                "Total Records": f"{m['total_records']:,}",
                "Avg Energy (kWh)": f"{m['avg_energy']:.1f}",
                "Peak Hour": f"{m['peak_hour']}:00",
                "Dominant Component": m["dominant_component"],
                "Date Range": m["date_range"],
            }
        )

    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df, width="stretch", hide_index=True)


def create_sidebar_navigation():
    """Create sidebar navigation for region and industry selection"""
    st.sidebar.title("EMS Dashboard")

    # Region selection
    region = st.sidebar.selectbox(
        "Select Region", ["Kansai", "Kanto"], key="region_selector"
    )

    # Industry selection
    industry = st.sidebar.selectbox(
        "Select Industry", ["All", "Transport", "Warehouse"], key="industry_selector"
    )

    # View Dashboard button
    if st.sidebar.button("View Dashboard", key="view_dashboard_btn", type="primary"):
        st.session_state.current_page = "dashboard"
        st.session_state.selected_region = region
        st.session_state.selected_industry = industry
        st.rerun()

    # Home button
    if st.sidebar.button("Home", key="home_btn"):
        st.session_state.current_page = "home"
        st.rerun()

    return region, industry


def show_landing_page():
    """Display the landing page with map and dashboard overview"""
    st.title("EMS Energy Consumption Dashboard")
    st.markdown("Data provided by [EMS Open Data Japan](https://www.ems-opendata.jp/)")

    # Interactive map
    st.subheader("Regional Overview")
    st.markdown(
        "Select a region and industry from the sidebar to explore detailed analytics:"
    )

    map_data = create_japan_map_data()
    st.map(map_data, zoom=5)

    st.markdown("---")

    # Footer attribution
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 12px;'>"
        "Data provided by <a href='https://www.ems-opendata.jp/' target='_blank'>EMS Open Data Japan</a> | "
        "Dashboard built with Streamlit"
        "</div>",
        unsafe_allow_html=True,
    )
