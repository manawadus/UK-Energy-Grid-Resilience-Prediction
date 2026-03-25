# Raw Data

Raw data files are not included in this repository due to size and source constraints.

This project uses publicly available datasets from the following sources:

## Data Sources

### 1. Generation Mix (NESO)
- Source: https://www.neso.energy/data-portal  
- Features: Gas, Coal, Nuclear, Wind, Wind_EMB, Hydro, Biomass, Solar, Imports, Storage, Other, Carbon Intensity  
- Time resolution: 30 minutes  
- Format: CSV  

### 2. Electricity Demand (NESO)
- Source: https://www.neso.energy/data-portal  
- Features: Total GB Demand, England & Wales Demand, Scotland Demand  
- Time resolution: 30 minutes  
- Format: CSV  

### 3. System Frequency (NESO)
- Source: https://www.neso.energy/data-portal  
- Features: Grid Frequency (Hz)  
- Time resolution: 1 second  
- Format: CSV  

### 4. Weather Data (Open-Meteo)
- Source: https://archive-api.open-meteo.com/  
- Features: Wind Speed, Wind Direction, Shortwave Radiation (Solar Proxy), Temperature, Cloud Cover, Precipitation  
- Time resolution: Hourly  
- Collection: Python API  

### 5. Calendar Data
- Source: https://www.gov.uk/bank-holidays  
- Features: Public Holidays, Working Day Indicators  
- Collection: Python  

## Notes

- All datasets were integrated and aligned to a common 30-minute resolution.
- System frequency data was aggregated from 1-second intervals.
- Weather data was resampled from hourly to 30-minute intervals.
- Time alignment was handled in UTC with adjustments for BST/GMT transitions.
