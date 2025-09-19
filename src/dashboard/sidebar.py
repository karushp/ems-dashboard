"""
Sidebar module for dashboard filters and chart creation
"""

import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.utils.constants import CHART_COLORS


def load_temperature_data(region_name):
    """Load temperature data for the specified region"""
    try:
        # Try to load region-specific temperature data first
        region_file = f"data/processed/temperature_{region_name.lower()}.parquet"
        if os.path.exists(region_file):
            temp_df = pd.read_parquet(region_file)
            # print(f"Temperature data loaded: {len(temp_df)} records")
            # print(
            #     f"Temperature date range: {temp_df['date'].min()} to {temp_df['date'].max()}"
            # )
            # print(
            #     f"Temperature range: {temp_df['temperature'].min():.1f}°C to {temp_df['temperature'].max():.1f}°C"
            # )
            return temp_df
        else:
            # Fallback to general temperature data
            general_file = "data/processed/temperature_data.parquet"
            if os.path.exists(general_file):
                temp_df = pd.read_parquet(general_file)
                # print(f"Temperature data loaded: {len(temp_df)} records")
                # print(
                #     f"Temperature date range: {temp_df['date'].min()} to {temp_df['date'].max()}"
                # )
                # print(
                #     f"Temperature range: {temp_df['temperature'].min():.1f}°C to {temp_df['temperature'].max():.1f}°C"
                # )
                return temp_df
            else:
                # print("No temperature data found")
                return None
    except Exception as e:
        # print(f"Error loading temperature data: {str(e)}")
        return None


def create_sidebar_filters(df):
    """Create sidebar filters and return filtered data"""
    # st.sidebar.header("Filters")

    # Convert Date column to datetime at the beginning
    df = df.copy()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

    # Date range filters
    st.sidebar.subheader("Date Range")
    # Get default dates safely
    if "Date" in df.columns and len(df) > 0:
        # Ensure Date column is datetime before calling .date()
        if not pd.api.types.is_datetime64_any_dtype(df["Date"]):
            df["Date"] = pd.to_datetime(df["Date"])
        default_start = df["Date"].min().date()
        default_end = df["Date"].max().date()
    else:
        default_start = pd.Timestamp("2013-01-01").date()
        default_end = pd.Timestamp("2013-12-31").date()

    start_date = st.sidebar.date_input(
        "Start Date",
        value=default_start,
        key="start_date",
    )
    end_date = st.sidebar.date_input(
        "End Date",
        value=default_end,
        key="end_date",
    )

    # Building type filter
    st.sidebar.subheader("Building Type")
    building_type_options = {
        "All": "All",
        "Single Building": "Single Building",
        "Tenant": "Tenant",
    }

    selected_building_label = st.sidebar.radio(
        "Select building type:",
        list(building_type_options.keys()),
        help="Single Building: Standalone facilities. Tenant: Shared building spaces.",
    )

    # Time aggregation
    st.sidebar.subheader("Time Aggregation")
    time_aggregation = st.sidebar.radio(
        "Aggregate data by:",
        ["Daily", "Weekly", "Monthly"],
        help="Choose how to group the time series data",
    )

    # Apply filters
    filtered_df = df.copy()

    # Date filter
    if "Date" in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df["Date"] >= pd.Timestamp(start_date))
            & (filtered_df["Date"] <= pd.Timestamp(end_date))
        ]

    # Building type filter
    if selected_building_label != "All":
        # Find the corresponding building type column
        building_col = f"Building Type_{selected_building_label}"
        if building_col in filtered_df.columns:
            # Filter for rows where this building type is 1 (True)
            filtered_df = filtered_df[filtered_df[building_col] == 1]

    return filtered_df, time_aggregation, selected_building_label


def create_energy_consumption_chart(consumption_data, title_suffix, region_name=None):
    """Create energy consumption chart with temperature overlay"""

    # Load temperature data
    temp_data = load_temperature_data(region_name) if region_name else None

    # Create the figure
    fig = go.Figure()

    # Convert index to timestamps if it contains Period objects
    if pd.api.types.is_period_dtype(consumption_data.index):
        x_values = consumption_data.index.to_timestamp()
    else:
        x_values = consumption_data.index
        # Ensure x_values are datetime objects for Plotly compatibility
        if not pd.api.types.is_datetime64_any_dtype(x_values):
            x_values = pd.to_datetime(x_values)

    # Add energy consumption bars
    fig.add_trace(
        go.Bar(
            x=x_values,
            y=consumption_data.values,
            name="Energy Consumption",
            marker_color=CHART_COLORS["energy"],
            yaxis="y",
        )
    )

    # Add temperature line if data is available
    if temp_data is not None:
        # Merge temperature data with consumption data by date
        temp_data["date"] = pd.to_datetime(temp_data["date"])
        consumption_data_df = consumption_data.reset_index()

        # Handle different index names based on aggregation
        date_col = consumption_data_df.columns[0]  # Get the first column (index)

        # Rename the index column to 'Date' for consistency
        consumption_data_df = consumption_data_df.rename(columns={date_col: "Date"})
        date_col = "Date"

        # Convert Period objects to timestamps if needed
        if pd.api.types.is_period_dtype(consumption_data_df[date_col]):
            consumption_data_df[date_col] = consumption_data_df[
                date_col
            ].dt.to_timestamp()
        else:
            consumption_data_df[date_col] = pd.to_datetime(
                consumption_data_df[date_col]
            )

        # Merge on date
        merged_data = pd.merge(
            consumption_data_df,
            temp_data,
            left_on=date_col,
            right_on="date",
            how="left",
        )

        if not merged_data["temperature"].isna().all():
            fig.add_trace(
                go.Scatter(
                    x=merged_data[date_col],
                    y=merged_data["temperature"],
                    mode="lines",
                    name="Temperature",
                    line=dict(color=CHART_COLORS["temperature"], width=2),
                    yaxis="y2",
                )
            )

            # Set y2 axis range based on temperature data
            temp_min = merged_data["temperature"].min()
            temp_max = merged_data["temperature"].max()
            temp_range = temp_max - temp_min
            padding = temp_range * 0.1

            fig.update_layout(
                yaxis2=dict(
                    title="Temperature (°C)",
                    title_font=dict(color="#333333"),
                    overlaying="y",
                    side="right",
                    range=[temp_min - padding, temp_max + padding],
                    showgrid=False,
                    tickfont=dict(color="#333333"),
                )
            )

    # Update layout
    fig.update_layout(
        title=f"Energy Consumption vs Temperature Over Time - {title_suffix}",
        title_font=dict(color="#333333"),
        xaxis_title="Date",
        xaxis_title_font=dict(color="#333333"),
        yaxis_title="Energy Consumption (kWh)",
        yaxis_title_font=dict(color="#333333"),
        xaxis=dict(tickfont=dict(color="#333333")),
        yaxis=dict(tickfont=dict(color="#333333"), showgrid=True),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            orientation="h",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1,
        ),
        hovermode="x unified",
    )

    return fig


def display_time_series_section(df, time_aggregation, region_name=None):
    """Display time series section with aggregation options"""

    st.subheader("Energy Consumption Over Time")

    # Show aggregation info
    st.info(f"Data aggregated by: {time_aggregation}")

    # Date column is already converted to datetime in create_sidebar_filters
    df = df.copy()

    # Aggregate data based on selection
    if time_aggregation == "Daily":
        consumption_data = df.groupby("Date")["Total"].sum()
        title_suffix = "Daily"
    elif time_aggregation == "Weekly":
        df_weekly = df.copy()
        df_weekly["Week"] = df_weekly["Date"].dt.to_period("W")
        consumption_data = df_weekly.groupby("Week")["Total"].sum()
        title_suffix = "Weekly"
    else:  # Monthly
        df_monthly = df.copy()
        df_monthly["Month"] = df_monthly["Date"].dt.to_period("M")
        consumption_data = df_monthly.groupby("Month")["Total"].sum()
        title_suffix = "Monthly"

    # Create and display chart
    fig_consumption = create_energy_consumption_chart(
        consumption_data, title_suffix, region_name
    )
    st.plotly_chart(fig_consumption, width="stretch")


def create_hourly_pattern_chart(df, region_name=None):
    """Create hourly consumption pattern chart"""

    # Calculate average hourly consumption
    hourly_avg = df.groupby("hour")["Total"].mean()

    # Create the figure
    fig = go.Figure()

    # Add hourly consumption bars
    fig.add_trace(
        go.Bar(
            x=hourly_avg.index,
            y=hourly_avg.values,
            name="Average Consumption",
            marker_color=CHART_COLORS["energy"],
        )
    )

    # Update layout
    fig.update_layout(
        title="Average Hourly Consumption Pattern",
        title_font=dict(color="#333333"),
        xaxis_title="Hour of Day",
        xaxis_title_font=dict(color="#333333"),
        yaxis_title="Average Energy Consumption (kWh)",
        yaxis_title_font=dict(color="#333333"),
        xaxis=dict(tickfont=dict(color="#333333")),
        yaxis=dict(tickfont=dict(color="#333333")),
        legend=dict(
            yanchor="top",
            y=1.02,
            xanchor="right",
            x=0.99,
            orientation="h",
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="rgba(0,0,0,0.2)",
            borderwidth=1,
        ),
    )

    return fig


def apply_dark_gray_labels(fig):
    """Apply dark gray labels to a plotly figure"""
    fig.update_layout(
        title_font=dict(color="#333333"),
        xaxis_title_font=dict(color="#333333"),
        yaxis_title_font=dict(color="#333333"),
        xaxis=dict(tickfont=dict(color="#333333")),
        yaxis=dict(tickfont=dict(color="#333333")),
    )
    return fig
