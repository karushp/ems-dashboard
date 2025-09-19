from typing import Any, Dict, Optional

import pandas as pd
import streamlit as st


@st.cache_data
def load_parquet_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load parquet data with caching for better performance

    Args:
        file_path: Path to the parquet file

    Returns:
        DataFrame or None if error
    """
    try:
        df = pd.read_parquet(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading {file_path}: {str(e)}")
        return None


def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Get summary statistics for the dataframe

    Args:
        df: Input dataframe

    Returns:
        Dictionary with summary statistics
    """
    if df is None or df.empty:
        return {}

    summary = {
        "total_records": len(df),
        "date_range": None,
        "avg_total_consumption": None,
        "peak_hour": None,
        "weekend_vs_weekday": None,
        "building_types": [],
        "energy_components": [],
    }

    try:
        # Date range
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
            summary["date_range"] = (df["Date"].min(), df["Date"].max())

        # Average consumption
        if "Total" in df.columns:
            summary["avg_total_consumption"] = df["Total"].mean()

        # Peak hour
        if "hour" in df.columns and "Total" in df.columns:
            summary["peak_hour"] = df.groupby("hour")["Total"].mean().idxmax()

        # Weekend vs weekday
        if "is_weekend" in df.columns and "Total" in df.columns:
            weekend_avg = df[df["is_weekend"] == True]["Total"].mean()
            weekday_avg = df[df["is_weekend"] == False]["Total"].mean()
            summary["weekend_vs_weekday"] = (weekend_avg, weekday_avg)

        # Building types
        building_cols = [col for col in df.columns if "Building Type" in col]
        summary["building_types"] = building_cols

        # Energy components
        energy_cols = ["AC", "Lighting", "Power", "Lamp", "Refrigeration", "Other"]
        summary["energy_components"] = [col for col in energy_cols if col in df.columns]

    except Exception as e:
        st.warning(f"Error calculating summary: {str(e)}")

    return summary


def filter_data(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """
    Apply filters to the dataframe

    Args:
        df: Input dataframe
        filters: Dictionary of filters to apply

    Returns:
        Filtered dataframe
    """
    if df is None or df.empty:
        return df

    filtered_df = df.copy()

    try:
        # Date range filter
        if (
            "date_range" in filters
            and filters["date_range"]
            and "Date" in filtered_df.columns
        ):
            start_date, end_date = filters["date_range"]
            if start_date and end_date:
                filtered_df = filtered_df[
                    (filtered_df["Date"] >= pd.to_datetime(start_date))
                    & (filtered_df["Date"] <= pd.to_datetime(end_date))
                ]

        # Building type filter
        if "building_type" in filters and filters["building_type"] != "All":
            building_col = filters.get(
                "building_type_column", "Building Type_Single Building"
            )
            if building_col in filtered_df.columns:
                filtered_df = filtered_df[
                    filtered_df[building_col] == filters["building_type"]
                ]

        # Energy component filter
        if "min_consumption" in filters:
            if "Total" in filtered_df.columns:
                filtered_df = filtered_df[
                    filtered_df["Total"] >= filters["min_consumption"]
                ]

    except Exception as e:
        st.warning(f"Error applying filters: {str(e)}")

    return filtered_df
