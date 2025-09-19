"""
Constants and configuration for the EMS Dashboard
"""

# Vibrant color palette
CHART_COLORS = {
    "primary": "#2E8B57",  # Deep teal/blue-green
    "secondary": "#DAA520",  # Golden yellow/mustard
    "accent": "#8B4B8C",  # Deep purple/plum
    "neutral": "#32CD32",  # Bright light green/lime
    "tertiary": "#CD853F",  # Burnt orange/terracotta
    "quaternary": "#FFA07A",  # Light orange/peach
    "quinary": "#20B2AA",  # Light aqua/mint green
    "temperature": "#666666",  # Dark gray for temperature lines
    "energy": "#2E8B57",  # Primary color for energy data
}

# Dashboard configuration
DASHBOARD_CONFIG = {
    "regions": ["Kansai", "Kanto"],
    "industries": ["Transport", "Warehouse"],
    "time_aggregations": ["Daily", "Weekly", "Monthly"],
    "building_types": ["All", "Single Building", "Tenant"],
}

# Data paths
DATA_PATHS = {
    "processed": "data/processed/",
    "temperature": "data/processed/",
    "raw": "data/",
}
