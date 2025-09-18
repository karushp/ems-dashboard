# EMS Open Source Dashboard

An interactive Energy Management System dashboard built with Streamlit for analyzing energy consumption data across Kansai and Kanto regions in Japan.

## Data Source

All data used in this dashboard was downloaded for research purposes from the [EMS Open Data Japan](https://www.ems-opendata.jp/) platform, operated by the Sustainable open Innovation Initiative (SII). This platform provides open access to energy management system data for academic and research purposes.

## Features

- **Interactive Map**: Visual representation of Japan with highlighted Kansai and Kanto regions
- **Regional Analysis**: Separate dashboards for Transport and Warehouse facilities
- **Comprehensive Visualizations**: 
  - Time series analysis
  - Building characteristics
  - Energy consumption breakdown
  - Load signature analysis
- **Interactive Filtering**: Date range and building type filters
- **Real-time Data**: Live data loading with caching for performance

## Data Structure

The dashboard analyzes energy consumption data including:
- **Energy Components**: AC, Lighting, Power, Lamp, Refrigeration, Other
- **Building Characteristics**: Floor area, contract power, building types
- **Temporal Analysis**: Hourly, daily, weekly patterns
- **Load Signatures**: Clustering and classification of consumption patterns

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
├── main.py                          # Main Streamlit application
├── pyproject.toml                   # Project dependencies
├── requirements.txt                 # Alternative requirements file
├── pages_module/                    # Individual dashboard pages
│   ├── kansai_transport.py         # Kansai transport analysis
│   ├── kansai_warehouse.py         # Kansai warehouse analysis
│   ├── kanto_transport.py          # Kanto transport analysis
│   └── kanto_warehouse.py          # Kanto warehouse analysis
├── preprocess_module/               # Data utilities
│   └── data_loader.py              # Data loading and caching
└── data/processed/                 # Processed parquet files
    ├── kansai_transport.parquet
    ├── kansai_warehouse.parquet
    ├── kanto_transport.parquet
    └── kanto_warehouse.parquet
```

## Regional Coverage

### Kansai Region
- **Location**: Western Japan (Osaka, Kyoto, Kobe)
- **Focus**: Historical and cultural centers
- **Data**: Transport and warehouse energy consumption

### Kanto Region  
- **Location**: Eastern Japan (Tokyo, Yokohama, Saitama)
- **Focus**: Metropolitan and industrial centers
- **Data**: Transport and warehouse energy consumption

## Dashboard Pages

1. **Home Page**: Regional overview with interactive map
2. **Transport Dashboards**: Detailed analysis of transport facility energy consumption
3. **Warehouse Dashboards**: Comprehensive warehouse energy analysis

Each dashboard includes:
- Key performance metrics
- Interactive time series charts
- Building characteristic analysis
- Energy component breakdown
- Load signature clustering

## Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your repository to Streamlit Cloud
3. Deploy with the main file as `main.py`

### GitHub Pages (Static)
For static deployment, consider using Streamlit's static export feature or converting to a static site generator.

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Data Attribution

This project uses data from [EMS Open Data Japan](https://www.ems-opendata.jp/) provided by the Sustainable open Innovation Initiative (SII). The data is used for research and educational purposes in accordance with the platform's terms of use.
