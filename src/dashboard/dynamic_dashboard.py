"""
Dynamic dashboard component that loads content based on region and industry selection
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.dashboard.sidebar import (
    apply_dark_gray_labels,
    create_hourly_pattern_chart,
    create_sidebar_filters,
    display_time_series_section,
)
from src.utils.constants import CHART_COLORS


def load_dashboard_data(region, industry):
    """Load data for the specified region and industry"""
    try:
        if industry.lower() == "all":
            # Load both transport and warehouse data and combine them
            transport_file = f"data/processed/{region.lower()}_transport.parquet"
            warehouse_file = f"data/processed/{region.lower()}_warehouse.parquet"

            transport_df = pd.read_parquet(transport_file)
            warehouse_df = pd.read_parquet(warehouse_file)

            # Add industry column to distinguish the data
            transport_df["Industry"] = "Transport"
            warehouse_df["Industry"] = "Warehouse"

            # Combine the dataframes
            combined_df = pd.concat([transport_df, warehouse_df], ignore_index=True)
            return combined_df
        else:
            file_path = f"data/processed/{region.lower()}_{industry.lower()}.parquet"
            df = pd.read_parquet(file_path)
            return df
    except Exception as e:
        st.error(f"Error loading data for {region} {industry}: {str(e)}")
        return None


def display_dashboard_content(region, industry):
    """Display the full dashboard content for the selected region and industry"""
    if industry.lower() == "all":
        st.title(f"{region} All Industries Energy Dashboard")
        st.info("Showing combined data from Transport and Warehouse facilities")
    else:
        st.title(f"{region} {industry} Energy Dashboard")
    st.markdown("---")

    # Load data
    df = load_dashboard_data(region, industry)
    if df is None:
        return

    # Create sidebar filters
    df, time_aggregation, selected_building = create_sidebar_filters(df)

    # Main content metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Records", f"{len(df):,}")

    with col2:
        avg_total = df["Total"].mean()
        st.metric("Avg Total Consumption", f"{avg_total:.1f} kWh")

    with col3:
        peak_hour = df.groupby("hour")["Total"].mean().idxmax()
        st.metric("Peak Hour", f"{peak_hour}:00")

    with col4:
        weekend_avg = df[df["is_weekend"] == True]["Total"].mean()
        weekday_avg = df[df["is_weekend"] == False]["Total"].mean()
        st.metric("Weekend vs Weekday", f"{weekend_avg:.1f} vs {weekday_avg:.1f}")

    st.markdown("---")

    # Charts section
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Energy Breakdown",
            "Time Series",
            "Building Analysis",
            "Load Signatures",
        ]
    )

    with tab1:
        display_energy_breakdown_tab(df)

    with tab2:
        # Display time series section using sidebar module
        display_time_series_section(df, time_aggregation, region)

        # Hourly pattern
        fig_hourly = create_hourly_pattern_chart(df, region)
        st.plotly_chart(
            fig_hourly,
            width="stretch",
            key=f"{region.lower()}_{industry.lower()}_hourly",
        )

    with tab3:
        display_building_analysis_tab(df, region, industry)

    with tab4:
        display_load_signatures_tab(df, region, industry)

    # Data table
    st.markdown("---")
    st.subheader("Raw Data")
    st.dataframe(df.head(100), width="stretch")


def display_energy_breakdown_tab(df):
    """Display energy breakdown tab content"""
    # st.subheader("Energy Consumption Breakdown")

    # Energy components
    energy_cols = ["AC", "Lighting", "Power", "Lamp", "Refrigeration", "Other"]
    available_cols = [col for col in energy_cols if col in df.columns]

    if available_cols:
        energy_totals = df[available_cols].sum()

        # COMPONENT ANALYSIS
        # st.markdown("### Component Analysis")

        col1, col2 = st.columns(2)

        with col1:
            fig_energy = px.pie(
                values=energy_totals.values,
                names=energy_totals.index,
                title="Energy Consumption by Component",
                color_discrete_sequence=[
                    CHART_COLORS["primary"],
                    CHART_COLORS["secondary"],
                    CHART_COLORS["accent"],
                    CHART_COLORS["neutral"],
                    CHART_COLORS["tertiary"],
                    CHART_COLORS["quaternary"],
                ],
            )
            fig_energy = apply_dark_gray_labels(fig_energy)
            st.plotly_chart(fig_energy, width="stretch", key="energy_pie")

        with col2:
            # Create DataFrame for bar chart
            energy_df = pd.DataFrame(
                {"Component": energy_totals.index, "Energy": energy_totals.values}
            )
            fig_bar = px.bar(
                energy_df,
                x="Component",
                y="Energy",
                title="Energy Consumption by Component (Bar Chart)",
                color="Component",
                color_discrete_sequence=[
                    CHART_COLORS["primary"],
                    CHART_COLORS["secondary"],
                    CHART_COLORS["accent"],
                    CHART_COLORS["neutral"],
                    CHART_COLORS["tertiary"],
                    CHART_COLORS["quaternary"],
                ],
            )
            fig_bar.update_layout(
                showlegend=False,
                xaxis_title="Component",
                yaxis_title="Total Energy Consumption (kWh)",
            )
            fig_bar = apply_dark_gray_labels(fig_bar)
            st.plotly_chart(fig_bar, width="stretch", key="energy_bar")

        # Component Efficiency Over Time (Stacked Area Chart)
        daily_components = df.groupby("Date")[available_cols].sum().reset_index()
        daily_components["Date"] = pd.to_datetime(daily_components["Date"])

        fig_stacked = px.area(
            daily_components,
            x="Date",
            y=available_cols,
            title="Component Efficiency Over Time",
            labels={"value": "Energy Consumption (kWh)", "Date": "Date"},
            color_discrete_sequence=[
                CHART_COLORS["primary"],
                CHART_COLORS["secondary"],
                CHART_COLORS["accent"],
                CHART_COLORS["neutral"],
                CHART_COLORS["tertiary"],
                CHART_COLORS["quaternary"],
            ],
        )
        fig_stacked = apply_dark_gray_labels(fig_stacked)
        st.plotly_chart(fig_stacked, width="stretch", key="component_stacked")

        # Peak vs Off-Peak Energy Comparison
        peak_hours = df[df["hour"].between(8, 18)]
        off_peak_hours = df[~df["hour"].between(8, 18)]

        peak_data = pd.DataFrame(
            {
                "Period": ["Peak Hours (8-18)", "Off-Peak Hours"],
                "Average Energy": [
                    peak_hours["Total"].mean(),
                    off_peak_hours["Total"].mean(),
                ],
            }
        )

        fig_peak = px.bar(
            peak_data,
            x="Period",
            y="Average Energy",
            title="Peak vs Off-Peak Energy Comparison",
            color="Period",
            color_discrete_sequence=[
                CHART_COLORS["primary"],
                CHART_COLORS["secondary"],
            ],
        )
        fig_peak = apply_dark_gray_labels(fig_peak)
        st.plotly_chart(fig_peak, width="stretch", key="peak_comparison")

        # Top 3 Components Hourly Patterns
        top_3_components = energy_totals.nlargest(3).index.tolist()
        hourly_components = df.groupby("hour")[top_3_components].mean().reset_index()

        fig_hourly = px.line(
            hourly_components,
            x="hour",
            y=top_3_components,
            title="Top 3 Components Hourly Patterns",
            labels={"value": "Average Energy (kWh)", "hour": "Hour of Day"},
            color_discrete_sequence=[
                CHART_COLORS["primary"],
                CHART_COLORS["secondary"],
                CHART_COLORS["accent"],
            ],
        )
        fig_hourly = apply_dark_gray_labels(fig_hourly)
        st.plotly_chart(fig_hourly, width="stretch", key="hourly_patterns")

        # TEMPORAL ANALYSIS
        # st.markdown("### Temporal Analysis")

        # Daily Energy Patterns
        weekday_names = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]
        daily_patterns = df.groupby("weekday")["Total"].mean().reset_index()
        daily_patterns["weekday_name"] = daily_patterns["weekday"].map(
            lambda x: weekday_names[x]
        )

        fig_daily = px.bar(
            daily_patterns,
            x="weekday_name",
            y="Total",
            title="Daily Energy Patterns (Average by Day of Week)",
            color="Total",
            color_continuous_scale="Viridis",
        )
        fig_daily = apply_dark_gray_labels(fig_daily)
        st.plotly_chart(fig_daily, width="stretch", key="daily_patterns")

        # Monthly Energy Trends
        monthly_energy = df.groupby("month")["Total"].sum().reset_index()
        month_names = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ]
        monthly_energy["month_name"] = monthly_energy["month"].map(
            lambda x: month_names[x - 1]
        )

        fig_monthly = px.bar(
            monthly_energy,
            x="month_name",
            y="Total",
            title="Monthly Energy Trends",
            color="Total",
            color_continuous_scale="Plasma",
        )
        fig_monthly = apply_dark_gray_labels(fig_monthly)
        st.plotly_chart(fig_monthly, width="stretch", key="monthly_trends")

        # Weekday vs Weekend Comparison
        weekday_data = df[df["is_weekend"] == False]["Total"].mean()
        weekend_data = df[df["is_weekend"] == True]["Total"].mean()

        weekend_comparison = pd.DataFrame(
            {
                "Period": ["Weekday", "Weekend"],
                "Average Energy": [weekday_data, weekend_data],
            }
        )

        fig_weekend = px.bar(
            weekend_comparison,
            x="Period",
            y="Average Energy",
            title="Weekday vs Weekend Energy Comparison",
            color="Period",
            color_discrete_sequence=[CHART_COLORS["primary"], CHART_COLORS["accent"]],
        )
        fig_weekend = apply_dark_gray_labels(fig_weekend)
        st.plotly_chart(fig_weekend, width="stretch", key="weekend_comparison")


def display_building_analysis_tab(df, region, industry):
    """Display building analysis tab content"""
    st.subheader("Building Characteristics Analysis")

    col1, col2 = st.columns(2)

    with col1:
        # Floor area distribution
        floor_area_cols = [col for col in df.columns if "Floor Area" in col]
        if floor_area_cols:
            floor_data = df[floor_area_cols].sum()
            fig_floor = px.pie(
                values=floor_data.values,
                names=floor_data.index,
                title="Floor Area Distribution",
                color_discrete_sequence=[
                    CHART_COLORS["primary"],
                    CHART_COLORS["secondary"],
                    CHART_COLORS["accent"],
                    CHART_COLORS["neutral"],
                    CHART_COLORS["tertiary"],
                    CHART_COLORS["quaternary"],
                ],
            )
            fig_floor = apply_dark_gray_labels(fig_floor)
            st.plotly_chart(fig_floor, width="stretch", key="floor_area")

    with col2:
        # Contract power analysis
        contract_cols = [col for col in df.columns if "Contract Power" in col]
        if contract_cols:
            contract_data = df[contract_cols].sum()
            # Create DataFrame for plotly
            contract_df = pd.DataFrame(
                {"Contract Type": contract_data.index, "Count": contract_data.values}
            )
            fig_contract = px.bar(
                contract_df,
                x="Contract Type",
                y="Count",
                title="Contract Power Distribution",
            )
            fig_contract = apply_dark_gray_labels(fig_contract)
            st.plotly_chart(fig_contract, width="stretch", key="contract_power")


def display_load_signatures_tab(df, region, industry):
    """Display load signatures tab content"""
    st.subheader("Load Signature Analysis")

    if "load_signature_class" in df.columns:
        # Load signature distribution
        signature_counts = df["load_signature_class"].value_counts()
        # Create DataFrame for bar chart
        signature_df = pd.DataFrame(
            {
                "Signature Class": signature_counts.index,
                "Count": signature_counts.values,
            }
        )
        fig_signature = px.bar(
            signature_df,
            x="Signature Class",
            y="Count",
            title="Load Signature Class Distribution",
        )
        fig_signature = apply_dark_gray_labels(fig_signature)
        st.plotly_chart(fig_signature, width="stretch", key="load_signature")

    if "cluster_class" in df.columns:
        # Cluster analysis
        cluster_counts = df["cluster_class"].value_counts()
        fig_cluster = px.pie(
            values=cluster_counts.values,
            names=cluster_counts.index,
            title="Energy Consumption Clusters",
            color_discrete_sequence=[
                CHART_COLORS["primary"],
                CHART_COLORS["secondary"],
                CHART_COLORS["accent"],
                CHART_COLORS["neutral"],
                CHART_COLORS["tertiary"],
                CHART_COLORS["quaternary"],
            ],
        )
        fig_cluster = apply_dark_gray_labels(fig_cluster)
        st.plotly_chart(fig_cluster, width="stretch", key="cluster_analysis")
