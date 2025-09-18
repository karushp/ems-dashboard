from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sidebar import (
    CHART_COLORS,
    apply_dark_gray_labels,
    create_hourly_pattern_chart,
    create_sidebar_filters,
    display_time_series_section,
)


def load_data():
    """Load Kansai transport data"""
    try:
        df = pd.read_parquet("data/processed/kansai_transport.parquet")
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None


def kansai_transport_page():
    st.title("Kansai Transport Energy Dashboard")
    st.markdown("---")

    # Load data
    df = load_data()
    if df is None:
        return

    # Create sidebar filters
    df, time_aggregation, selected_building = create_sidebar_filters(df)

    # Main content
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
            "Time Series",
            "Building Analysis",
            "Energy Breakdown",
            "Load Signatures",
        ]
    )

    with tab1:
        # Display time series section using sidebar module
        display_time_series_section(df, time_aggregation, "Kansai")

        # Hourly pattern
        fig_hourly = create_hourly_pattern_chart(df, "Kansai")
        st.plotly_chart(fig_hourly, width="stretch", key="kansai_transport_chart_1")

    with tab2:
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
                st.plotly_chart(
                    fig_floor, width="stretch", key="kansai_transport_chart_2"
                )

        with col2:
            # Contract power analysis
            contract_cols = [col for col in df.columns if "Contract Power" in col]
            if contract_cols:
                contract_data = df[contract_cols].sum()
                fig_contract = px.bar(
                    x=contract_data.index,
                    y=contract_data.values,
                    title="Contract Power Distribution",
                )
                fig_contract = apply_dark_gray_labels(fig_contract)
                st.plotly_chart(
                    fig_contract, width="stretch", key="kansai_transport_chart_3"
                )

    with tab3:
        st.subheader("Energy Consumption Breakdown")

        # Energy components
        energy_cols = ["AC", "Lighting", "Power", "Lamp", "Refrigeration", "Other"]
        available_cols = [col for col in energy_cols if col in df.columns]

        if available_cols:
            energy_totals = df[available_cols].sum()
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
            st.plotly_chart(fig_energy, width="stretch", key="kansai_transport_chart_4")

            # Time series for energy components
            energy_ts = df.groupby("Date")[available_cols].sum().reset_index()
            fig_ts = px.line(
                energy_ts,
                x="Date",
                y=available_cols,
                title="Energy Components Over Time",
                color_discrete_sequence=[
                    CHART_COLORS["primary"],
                    CHART_COLORS["secondary"],
                    CHART_COLORS["accent"],
                    CHART_COLORS["neutral"],
                    CHART_COLORS["tertiary"],
                    CHART_COLORS["quaternary"],
                ],
            )
            fig_ts = apply_dark_gray_labels(fig_ts)
            st.plotly_chart(fig_ts, width="stretch", key="kansai_transport_chart_5")

    with tab4:
        st.subheader("Load Signature Analysis")

        if "load_signature_class" in df.columns:
            # Load signature distribution
            signature_counts = df["load_signature_class"].value_counts()
            fig_signature = px.bar(
                x=signature_counts.index,
                y=signature_counts.values,
                title="Load Signature Class Distribution",
            )
            fig_signature = apply_dark_gray_labels(fig_signature)
            st.plotly_chart(
                fig_signature, width="stretch", key="kansai_transport_chart_6"
            )

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
            st.plotly_chart(
                fig_cluster, width="stretch", key="kansai_transport_chart_7"
            )

    # Data table
    st.markdown("---")
    st.subheader("Raw Data")
    st.dataframe(df.head(100), width="stretch")


if __name__ == "__main__":
    kansai_transport_page()
