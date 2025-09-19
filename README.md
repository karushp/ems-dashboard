# EMS Energy Consumption Dashboard

An interactive Energy Management System dashboard built with Streamlit for analyzing energy consumption data across Kansai and Kanto regions in Japan.

## Data Source

All data used in this dashboard was downloaded for research purposes from the [EMS Open Data Japan](https://www.ems-opendata.jp/) platform, operated by the Sustainable open Innovation Initiative (SII). This platform provides open access to energy management system data for academic and research purposes.

### Live Application
 **The dashboard is live at: [https://bt9uzzr6a7mtgpx82prnrt.streamlit.app/](https://bt9uzzr6a7mtgpx82prnrt.streamlit.app/)**

## Features

- **Interactive Map**: Visual representation of Japan with highlighted Kansai and Kanto regions
- **Regional Analysis**: Separate dashboards for Transport, Warehouse, or combined All industries
- **Comprehensive Visualizations**: 
  - Energy breakdown analysis
  - Time series analysis with temperature correlation
  - Building characteristics analysis
  - Load signature analysis
- **Interactive Filtering**: Date range, building type, and time aggregation filters
- **Real-time Data**: Live data loading with caching for performance
- **Professional UI**: Clean, modern interface with standardized color palette

## Data Structure

The dashboard analyzes energy consumption data including:
- **Energy Components**: AC, Lighting, Power, Lamp, Refrigeration, Other
- **Building Characteristics**: Floor area, contract power, building types
- **Temporal Analysis**: Daily, weekly, monthly patterns
- **Load Signatures**: Clustering and classification of consumption patterns
- **Temperature Data**: Historical weather correlation for energy analysis

## Installation & Setup

### Prerequisites
- Python 3.13+
- uv package manager

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd ems_opensource

# Install dependencies
uv sync

# Activate virtual environment
source .venv/bin/activate  # On Unix/Mac
# or
.venv\Scripts\activate    # On Windows
```

### Running the Application
```bash
# Start the Streamlit app
streamlit run main.py
```

The application will be available at `http://localhost:8501`

## Project Structure

```
ems_opensource/
├── main.py                          # Main Streamlit application (51 lines)
├── pyproject.toml                   # Project dependencies
├── requirements.txt                 # Alternative requirements file
├── src/                             # Source code
│   ├── dashboard/                   # Dashboard components
│   │   ├── dynamic_dashboard.py     # Main dashboard logic (400 lines)
│   │   ├── landing_page.py          # Landing page + navigation + overview (265 lines)
│   │   ├── metrics_calculator.py   # Metrics calculations (113 lines)
│   │   └── sidebar.py              # Sidebar filters & charts (330 lines)
│   ├── data/                        # Data utilities
│   │   └── data_loader.py          # Data loading and caching (134 lines)
│   └── utils/                       # Utilities and constants
│       └── constants.py             # Color palettes and configuration (32 lines)
└── data/                            # Data files
    └── processed/                   # Processed parquet files 
        ├── kansai_transport.parquet 
        ├── kansai_warehouse.parquet
        ├── kanto_transport.parquet
        ├── kanto_warehouse.parquet
        ├── temperature_kansai.parquet  
        └── temperature_kanto.parquet   
```

## Dashboard Features

### Landing Page
- Interactive map of Japan highlighting regions
- Overview metrics cards for all 6 region/industry combinations
- Data distribution charts and summary statistics

### Dynamic Dashboard
- **Energy Breakdown**: Component analysis, efficiency trends, peak/off-peak comparison
- **Time Series**: Energy consumption vs temperature correlation, hourly patterns
- **Building Analysis**: Contract power distribution, building characteristics
- **Load Signatures**: Signature distribution and clustering analysis

### Interactive Filters
- Date range selection (start/end dates)
- Building type filtering (All, Single Building, Tenant)
- Time aggregation (Daily, Weekly, Monthly)
- Industry selection (Transport, Warehouse, All)
- Real-time data updates

## Regional Coverage

### Kansai Region
- **Location**: Western Japan (Osaka, Kyoto, Kobe)
- **Focus**: Historical and cultural centers
- **Data**: Transport and warehouse energy consumption

### Kanto Region  
- **Location**: Eastern Japan (Tokyo, Yokohama, Saitama)
- **Focus**: Metropolitan and industrial centers
- **Data**: Transport and warehouse energy consumption

## Technical Architecture

- **Frontend**: Streamlit with custom CSS styling
- **Data Processing**: Pandas for data manipulation
- **Visualizations**: Plotly for interactive charts
- **Data Storage**: Parquet files for efficient data access
- **Modular Design**: Clean separation of concerns with focused modules
- **Optimized Data**: Only essential files included (100% usage efficiency)

## Data Overview

### Energy Data (4 files, 63.6MB)
- **Kansai Transport**: 3.3MB
- **Kansai Warehouse**: 4.3MB
- **Kanto Transport**: 30MB
- **Kanto Warehouse**: 26MB

### Temperature Data (2 files, 10KB)
- **Kansai Temperature**: 5KB
- **Kanto Temperature**: 5KB

## Deployment

### Local Development
```bash
# Run in development mode
streamlit run main.py --server.port 8502 --server.headless true
```

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Data Attribution

This project uses data from [EMS Open Data Japan](https://www.ems-opendata.jp/) provided by the Sustainable open Innovation Initiative (SII). The data is used for research and educational purposes in accordance with the platform's terms of use.