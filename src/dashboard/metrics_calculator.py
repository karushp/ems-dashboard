"""
Metrics calculator for dashboard overview cards
"""

import pandas as pd


def calculate_dashboard_metrics(region, industry):
    """
    Calculate key metrics for a specific region and industry combination

    Args:
        region (str): 'Kansai' or 'Kanto'
        industry (str): 'Transport', 'Warehouse', or 'All'

    Returns:
        dict: Dictionary containing key metrics
    """
    try:
        # Load the appropriate dataset
        if industry.lower() == "all":
            # Load both transport and warehouse data and combine them
            # Use sample data for Kanto region to reduce memory usage
            if region.lower() == "kanto":
                transport_file = (
                    f"data/processed/sample_{region.lower()}_transport.parquet"
                )
                warehouse_file = (
                    f"data/processed/sample_{region.lower()}_warehouse.parquet"
                )
            else:
                transport_file = f"data/processed/{region.lower()}_transport.parquet"
                warehouse_file = f"data/processed/{region.lower()}_warehouse.parquet"

            transport_df = pd.read_parquet(transport_file)
            warehouse_df = pd.read_parquet(warehouse_file)

            # Add industry column to distinguish the data
            transport_df["Industry"] = "Transport"
            warehouse_df["Industry"] = "Warehouse"

            # Combine the dataframes
            df = pd.concat([transport_df, warehouse_df], ignore_index=True)
        else:
            # Use sample data for Kanto region to reduce memory usage
            if region.lower() == "kanto":
                file_path = (
                    f"data/processed/sample_{region.lower()}_{industry.lower()}.parquet"
                )
            else:
                file_path = (
                    f"data/processed/{region.lower()}_{industry.lower()}.parquet"
                )
            df = pd.read_parquet(file_path)

        # Calculate metrics
        metrics = {
            "region": region,
            "industry": industry,
            "total_records": len(df),
            "avg_energy": df["Total"].mean() if "Total" in df.columns else 0,
            "peak_hour": (
                df.groupby("hour")["Total"].mean().idxmax()
                if "hour" in df.columns and "Total" in df.columns
                else 0
            ),
            "weekend_avg": (
                df[df["is_weekend"] == True]["Total"].mean()
                if "is_weekend" in df.columns and "Total" in df.columns
                else 0
            ),
            "weekday_avg": (
                df[df["is_weekend"] == False]["Total"].mean()
                if "is_weekend" in df.columns and "Total" in df.columns
                else 0
            ),
            "date_range": (
                f"{pd.to_datetime(df['Date']).min().strftime('%Y-%m-%d')} to {pd.to_datetime(df['Date']).max().strftime('%Y-%m-%d')}"
                if "Date" in df.columns
                else "N/A"
            ),
            "dominant_component": get_dominant_component(df),
        }

        return metrics

    except Exception as e:
        # Return default metrics if data loading fails
        return {
            "region": region,
            "industry": industry,
            "total_records": 0,
            "avg_energy": 0,
            "peak_hour": 0,
            "weekend_avg": 0,
            "weekday_avg": 0,
            "date_range": "N/A",
            "dominant_component": "N/A",
        }


def get_dominant_component(df):
    """Get the dominant energy component from the dataframe"""
    energy_cols = ["AC", "Lighting", "Power", "Lamp", "Refrigeration", "Other"]
    available_cols = [col for col in energy_cols if col in df.columns]

    if available_cols:
        component_totals = df[available_cols].sum()
        return component_totals.idxmax()
    return "N/A"


def get_all_dashboard_metrics():
    """Get metrics for all six dashboard combinations"""
    combinations = [
        ("Kansai", "Transport"),
        ("Kansai", "Warehouse"),
        ("Kansai", "All"),
        ("Kanto", "Transport"),
        ("Kanto", "Warehouse"),
        ("Kanto", "All"),
    ]

    all_metrics = []
    for region, industry in combinations:
        metrics = calculate_dashboard_metrics(region, industry)
        all_metrics.append(metrics)

    return all_metrics
