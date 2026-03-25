# Processed Data

This folder contains the final dataset used for modelling.

The processed dataset was created by integrating:

- Generation mix data
- Electricity demand data
- System frequency data (aggregated to 30-minute intervals)
- Weather data (resampled to 30-minute intervals)
- Calendar features (holidays and time-based variables)

## Key Processing Steps

- Time alignment across multiple data sources
- Handling of BST/GMT transitions
- Aggregation of high-frequency data
- Feature engineering for machine learning
- Construction of the Grid Resilience Index (GRI)

## Note

The full processed dataset is not included due to size constraints.
Please refer to the notebooks for data preparation steps.
