# UK Energy Grid Resilience Prediction Using Open Data

## Project Overview

This repository presents my MSc Data Science dissertation project, **UK Energy Grid Resilience Prediction Using Open Data**. The project develops a data-driven framework to quantify and forecast short-term electricity grid resilience in **Great Britain (GB)** using publicly available operational, weather, and calendar datasets.

The study integrates multiple data sources and applies feature engineering and machine learning techniques to model grid behaviour. As part of this process, a **Grid Resilience Index (GRI)** is constructed to represent system resilience as a single, interpretable target variable. The index combines five key operational dimensions, conceptually aligned with international resilience frameworks from the National Infrastructure Advisory Council (USA), the UK Cabinet Office, and the Multidisciplinary Centre for Earthquake Engineering Research (MCEER):

- Supply–Demand Margin  
- Fuel-Mix Diversity  
- Import Dependence  
- Storage Contribution  
- Frequency Stability  

Using this framework, machine learning models are applied to forecast the GRI **6 hours ahead**, based on time-based, operational, and weather-derived features.

---

## Research Aim

The aim of this project is to develop a machine learning framework that predicts short-term grid resilience, up to **6 hours ahead**, by integrating electricity generation, demand, weather, and time indicators into a unified analytical model.

---

## Research Objectives

1. Define and operationalise grid resilience by constructing a composite **Grid Resilience Index (GRI)**.
2. Identify, collect, and integrate relevant open data sources for UK grid resilience analysis.
3. Perform preprocessing and feature engineering, including lags, rolling windows, and calendar features.
4. Apply **XGBoost** and **Support Vector Regression (SVR)** to predict grid resilience.
5. Evaluate model performance and use **SHAP** for interpretability.

---

## Problem Context

The GB electricity system is becoming more complex due to:

- increasing penetration of renewable generation
- stronger weather dependence of supply
- tighter operational margins
- growing use of storage and imports
- the need for better short-term analytical visibility

Traditional reliability indicators do not fully capture this multidimensional operational picture. This project addresses that gap by developing a structured resilience index and testing whether short-term resilience can be forecast using open data.

---

## Study Scope

- **Region:** Great Britain
- **Forecast horizon:** 6 hours ahead
- **Temporal resolution:** 30-minute settlement-period level
- **Coverage:** 1 January 2020 to 14 September 2025
- **Target variable:** Grid Resilience Index (GRI)

---

## Data Sources

The project uses publicly available, government-supported open datasets.

### 1. NESO / National Energy System Operator
Source of system-level electricity data for Great Britain:
- historic generation mix and carbon intensity
- historic demand data
- system frequency data

### 2. Open-Meteo API
Weather data collected for five geographically distributed GB locations:
- Aberdeen
- Humber
- Camborne
- Ashford
- East Anglia

Weather variables include:
- temperature
- precipitation
- wind speed
- wind direction
- shortwave radiation
- cloud cover

### 3. Calendar and Public Holiday Data
Used to generate:
- weekday / weekend indicators
- holiday indicators
- calendar-based demand behaviour features

---

## Data Engineering Workflow

The repository follows a multi-stage data engineering workflow:

1. Download and ingest generation, demand, frequency, weather, and calendar data
2. Standardise timestamps and align all sources to a common 30-minute resolution
3. Handle settlement-period alignment across BST/GMT transitions
4. Aggregate 1-second frequency data into 30-minute statistics
5. Upsample hourly weather data to 30-minute intervals
6. Merge all data into a single master analytical table
7. Build the Grid Resilience Index
8. Engineer lag, rolling, temporal, and PCA-based weather features
9. Train and evaluate forecasting models
10. Interpret model behaviour using SHAP

---

## Time Alignment Strategy

A major part of the project was temporal harmonisation across heterogeneous sources:

- Generation mix: 30-minute UTC
- System frequency: 1-second UTC
- Weather: hourly UTC
- Demand: settlement date + settlement period in local time

To preserve operational integrity:

- all timestamps were standardised in UTC
- local time was reconstructed using `Europe/London`
- settlement periods were recalculated across daylight-saving transitions
- weather data was resampled from hourly to 30-minute intervals using forward fill
- system frequency was aggregated into 30-minute windows

This ensured reliable alignment even on 46- or 50-period daylight-saving days.

---

## Grid Resilience Index (GRI)

The GRI is a weighted composite score scaled to a 0–100 range.

### Components

#### 1. Supply–Demand Margin (M)
Measures adequacy of total generation relative to transmission system demand.

#### 2. Fuel-Mix Diversity (D)
Measures how balanced the generation mix is across fuel types using an inverse concentration approach.

#### 3. Import Dependence (I)
Represents dependence on imported electricity. Lower dependency is treated as stronger resilience.

#### 4. Storage Contribution (S)
Measures balancing support provided by storage relative to demand.

#### 5. Frequency Stability (F)
Captures deviation of average system frequency from the nominal 50 Hz.

### Weighting

The final GRI uses the following weights:

- **M = 0.40**
- **D = 0.20**
- **I = 0.10**
- **S = 0.10**
- **F = 0.20**

These are modelling assumptions designed to provide a balanced and interpretable operational score.

---

## Feature Engineering

The final feature set includes:

### Time-based features
- hour
- day of week
- month
- day of year
- cyclical time transforms such as `hour_sin`, `hour_cos`, `month_cos`

### Lag features
Lagged versions of key operational variables to capture temporal dependence.

### Rolling features
Rolling means and standard deviations to capture short-term dynamics.

### Weather PCA
Because weather data from multiple locations introduced multicollinearity, PCA was applied separately to major weather groups such as:
- temperature
- wind
- solar
- precipitation
- cloud cover

This reduced redundancy while preserving most of the variance.

---

## Machine Learning Models

Two regression models were used for 6-hour ahead forecasting:

### XGBoost
A gradient-boosted tree model suited to non-linear interactions and high-dimensional tabular data.

### Support Vector Regression (SVR)
A kernel-based regression model used as a comparative benchmark.

### Validation Strategy

A time-aware chronological split was used:

- **Training:** 2020–2023
- **Testing:** 2024–2025 (until 30 August)

This avoids information leakage and reflects real forecasting conditions.

---

## Results

### Summary Statistics of GRI
The Grid Resilience Index ranged from:

- **Minimum:** 35.57
- **Q1:** 43.58
- **Q3:** 48.25
- **Maximum:** 59.30
- **Mean:** 45.94

### Correlation Findings
The strongest correlation with GRI was:

- Supply–Demand Margin: **0.63**
- Storage Contribution: **0.53**
- Import Dependence: **0.32**
- Fuel-Mix Diversity: **0.28**
- Frequency Stability: **0.02**

### Seasonal Findings
Both low- and high-resilience periods were most frequently observed in **spring and summer**.

### Model Comparison

| Model | R² | MAE | RMSE |
|------|----:|----:|----:|
| XGBoost | 0.661 | 1.668 | 2.146 |
| RBF-SVM | 0.540 | 1.985 | 2.553 |

XGBoost outperformed RBF-SVM in both predictive accuracy and practicality for the full feature set.

---

## Diagnostics and Interpretability

Residual diagnostics showed:

- residuals centred near zero
- no strong heteroscedasticity
- strong alignment between predictions and actuals
- weaker performance in extreme cases

SHAP analysis showed that the most influential predictors included:

- `hour_sin`
- `WIND_TOTAL`
- `hour`
- `IMPORTS`
- `month_cos`
- `year`

Overall, the results show that resilience is shaped by a combination of:

- temporal structure
- wind availability
- imports
- conventional generation support
- secondary weather influences

---

## Key Findings

- Short-term resilience forecasting using open data is feasible.
- XGBoost performs better than RBF-SVM for this task.
- Margin, imports, and diversity are important operational drivers of resilience.
- Time structure is the strongest predictive signal in the forecasting model.
- Extreme stress conditions remain harder to predict accurately.

---

## Methodological Strengths

- Fully open-data workflow
- Transparent and reproducible integration pipeline
- Explicit treatment of time alignment and settlement periods
- Interpretable GRI design
- Combined descriptive analysis, forecasting, diagnostics, and SHAP interpretation

---

  ## Recommended Figures

Include these figures in results/figures/:

- Daily average TSD trend
- System frequency trend
- Daily average GRI trend
- Distribution of GRI components
- Correlation heatmap
- XGBoost diagnostic plots
- SHAP feature importance plot

---
## Limitations

- GRI weights are based on modelling assumptions rather than validation against operator-defined resilience frameworks, which may affect real-world interpretability.

- The analysis relies on open-source data, which excludes key operational variables such as reserve capacity, generator outage schedules, and balancing or ancillary service actions. These factors influence real-time system behaviour and their absence may limit the model’s ability to fully capture grid dynamics.

- Storage activity within the dataset is relatively limited, reflecting its current share in the GB energy mix. As a result, its contribution to both the GRI and the predictive model is less pronounced.

- Renewable generation effects are not explicitly modelled as standalone resilience channels, which may limit the ability to isolate their individual impact on grid stability.

---

## Reproducibility

This project is based entirely on publicly available data sources. Data acquisition, integration, modelling, and interpretation steps are documented in notebooks and scripts so that the workflow can be reproduced.


---

## Repository Structure

```
uk-energy-grid-resilience-prediction/

├── README.md
├── requirements.txt
├── .gitignore

├── data/
│   ├── raw/            # raw data (not included due to size and source constraints)
│   └── processed/      # final dataset used for modelling

├── notebooks/
│   ├── 01_data_integration.ipynb
│   ├── 02_gri_construction.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_model_training.ipynb
│   └── 05_evaluation.ipynb

├── results/
│   ├── figures/        # visualisations and plots
│   └── metrics/        # model performance outputs

├── report/
│   └── dissertation.pdf

└── docs/
    └── architecture_diagram.png
```
## Author

Suresh Manawadu
MSc Data Science, Coventry University

---
## Note

This repository is shared for academic and portfolio purposes. The GRI is a research construct and should not be used directly for operational decision-making without further validation.

- Extreme low-resilience events are harder to predict accurately, as they are relatively rare and often driven by complex, unobserved operational conditions.

- The SVR model was trained on a reduced subset of the dataset due to computational constraints, so the comparison with XGBoost is not fully symmetrical.
