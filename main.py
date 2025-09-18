import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

# Add modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), "pages_module"))
sys.path.append(os.path.join(os.path.dirname(__file__), "preprocess_module"))

from data_loader import get_data_summary, load_parquet_data
from dynamic_dashboard import display_dashboard_content
from metrics_calculator import get_all_dashboard_metrics


def create_japan_map_data():
    """Create data for st.map showing Kansai and Kanto regions"""

    # Define region coordinates and data
    regions_data = {
        "Kansai": {
            "lat": 34.6937,
            "lon": 135.5023,
            "transport_records": 0,
            "warehouse_records": 0,
        },
        "Kanto": {
            "lat": 35.6762,
            "lon": 139.6503,
            "transport_records": 0,
            "warehouse_records": 0,
        },
    }

    # Load actual data counts
    for region_name in regions_data:
        transport_file = f"data/processed/{region_name.lower()}_transport.parquet"
        warehouse_file = f"data/processed/{region_name.lower()}_warehouse.parquet"

        if os.path.exists(transport_file):
            try:
                transport_df = load_parquet_data(transport_file)
                if transport_df is not None:
                    regions_data[region_name]["transport_records"] = len(transport_df)
            except:
                pass

        if os.path.exists(warehouse_file):
            try:
                warehouse_df = load_parquet_data(warehouse_file)
                if warehouse_df is not None:
                    regions_data[region_name]["warehouse_records"] = len(warehouse_df)
            except:
                pass

    # Create DataFrame for st.map
    map_data = []
    for region_name, data in regions_data.items():
        map_data.append(
            {
                "lat": data["lat"],
                "lon": data["lon"],
                "region": region_name,
                "transport_records": data["transport_records"],
                "warehouse_records": data["warehouse_records"],
                "total_records": data["transport_records"] + data["warehouse_records"],
            }
        )

    return pd.DataFrame(map_data)


def create_overview_charts(all_metrics):
    """Create professional charts for the overview section"""

    # Prepare data for charts
    regions = [m["region"] for m in all_metrics]
    industries = [m["industry"] for m in all_metrics]
    records = [m["total_records"] for m in all_metrics]
    avg_energy = [m["avg_energy"] for m in all_metrics]
    labels = [f"{m['region']} {m['industry']}" for m in all_metrics]

    # Create two columns for charts
    col1, col2 = st.columns(2)

    with col1:
        # Records distribution bar chart
        fig_records = px.bar(
            x=labels,
            y=records,
            title="Total Records by Region & Industry",
            color=records,
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


def create_metric_card(metrics):
    """Create a metric card for a dashboard"""
    region = metrics["region"]
    industry = metrics["industry"]

    # Create card with custom styling
    card_html = f"""
    <div style="
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 1px solid #dee2e6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    ">
        <h4 style="color: #333333; margin-bottom: 15px; text-align: center;">
            {region} {industry}
        </h4>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 14px;">
            <div><strong>Records:</strong><br>{metrics['total_records']:,}</div>
            <div><strong>Avg Energy:</strong><br>{metrics['avg_energy']:.1f} kWh</div>
            <div><strong>Peak Hour:</strong><br>{metrics['peak_hour']}</div>
            <div><strong>Dominant:</strong><br>{metrics['dominant_component']}</div>
        </div>
        <div style="margin-top: 10px; font-size: 12px; color: #666; text-align: center;">
            {metrics['date_range']}
        </div>
    </div>
    """
    return card_html


def show_landing_page():
    """Display the enhanced landing page with metrics cards"""
    st.title("EMS Energy Dashboard")
    st.markdown("### Comprehensive Energy Management System for Japanese Facilities")

    # Data attribution at the top
    st.info(
        "**Data Source**: All data downloaded for research purposes from [EMS Open Data Japan](https://www.ems-opendata.jp/)"
    )

    st.markdown("---")

    # Interactive map
    st.subheader("Data Coverage Map")
    map_data = create_japan_map_data()
    st.map(map_data, zoom=5)

    st.markdown("---")

    # Dashboard overview with metrics cards and visualizations
    st.subheader("Dashboard Overview")
    st.markdown(
        "Select a region and industry from the sidebar to explore detailed analytics, or view the overview below:"
    )

    # Get metrics for all dashboards
    try:
        all_metrics = get_all_dashboard_metrics()

        # Create 4 columns for the metric cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(create_metric_card(all_metrics[0]), unsafe_allow_html=True)

        with col2:
            st.markdown(create_metric_card(all_metrics[1]), unsafe_allow_html=True)

        with col3:
            st.markdown(create_metric_card(all_metrics[2]), unsafe_allow_html=True)

        with col4:
            st.markdown(create_metric_card(all_metrics[3]), unsafe_allow_html=True)

        # Add visualizations below the cards
        st.markdown("---")
        st.subheader("Data Distribution Overview")

        # Create charts showing data distribution
        create_overview_charts(all_metrics)

    except Exception as e:
        st.error(f"Error loading dashboard metrics: {str(e)}")
        st.info(
            "Please ensure all data files are available in the data/processed/ directory"
        )

    # Footer attribution
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 12px;'>"
        "Data provided by <a href='https://www.ems-opendata.jp/' target='_blank'>EMS Open Data Japan</a> | "
        "Dashboard built with Streamlit"
        "</div>",
        unsafe_allow_html=True,
    )


def create_sidebar_navigation():
    """Create sidebar navigation for region and industry selection"""
    st.sidebar.title("EMS Dashboard")

    # Region selection
    region = st.sidebar.selectbox(
        "Select Region", ["Kansai", "Kanto"], key="region_selector"
    )

    # Industry selection
    industry = st.sidebar.selectbox(
        "Select Industry", ["Transport", "Warehouse"], key="industry_selector"
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


def main():
    """Main application function"""
    # Page configuration
    st.set_page_config(
        page_title="EMS Energy Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Initialize session state
    if "current_page" not in st.session_state:
        st.session_state.current_page = "home"
    if "selected_region" not in st.session_state:
        st.session_state.selected_region = "Kansai"
    if "selected_industry" not in st.session_state:
        st.session_state.selected_industry = "Transport"

    # Create sidebar navigation
    sidebar_region, sidebar_industry = create_sidebar_navigation()

    # Main content area
    if st.session_state.current_page == "home":
        show_landing_page()
    elif st.session_state.current_page == "dashboard":
        # Use sidebar selections or session state
        region = st.session_state.selected_region
        industry = st.session_state.selected_industry
        display_dashboard_content(region, industry)
    else:
        show_landing_page()


if __name__ == "__main__":
    main()
