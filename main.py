"""
EMS Energy Consumption Dashboard - Main Application
"""

import os
import sys

import streamlit as st

# Disable file watching to avoid inotify limit issues
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.dashboard.dynamic_dashboard import display_dashboard_content
from src.dashboard.landing_page import create_sidebar_navigation, show_landing_page


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
