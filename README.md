# Air Quality Data Analysis – CIE Milestone 1

## Project Overview

This project focuses on analyzing an Air Quality dataset using Python, Pandas, NumPy, Matplotlib and Seaborn.

The main objective is to understand air pollution data, perform data transformations, identify and handle missing values using mean imputation, generate meaningful insights and visualize the results.

## Dataset Information

- **Dataset:** Air Quality Dataset
- **Source:** UCI Machine Learning Repository
- **Original records:** 9,471 rows
- **Valid records after removing empty rows:** 9,357
- **Original columns:** 15
- **File:** AirQualityUCI.csv

Dataset source: https://archive.ics.uci.edu/dataset/360/air+quality

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib

## Project Implementation

### 1. Dataset Reading
Loaded the CSV dataset using Pandas and examined its structure.

### 2. Data Understanding
Used:
- head()
- info()
- describe()
- shape
- isnull().sum()

### 3. Data Transformation
- Removed completely empty rows.
- Replaced -200 missing-value indicators with NaN.
- Converted Date and Time into a DateTime column.
- Created Hour, Month, Month_Name and Day columns.
- Removed unnecessary original Date and Time columns.

### 4. Handling Missing Values
Identified missing values and applied mean imputation to numerical columns.

All missing numerical values were filled successfully.

### 5. Insight Generation

The analysis produced the following findings:

1. The highest average CO level occurred at 7 PM, with an average value of 3.51.
2. February 2005 recorded the highest monthly average NO2 level of 158.57.
3. CO and Benzene (C6H6) showed the strongest correlation, with a correlation coefficient of 0.812.
4. Temperature and CO showed a very weak correlation of 0.020.

### 6. Data Visualization

Four charts were generated:

- Monthly average NO2 pollution trend.
- Hourly average CO pollution.
- Pollutant correlation heatmap.
- Temperature versus CO scatter plot.

## Project Structure

```text
CIE-MILESTONE-1/
│
├── AirQualityUCI.csv
├── cie_milestone1.py
├── cleaned_air_quality.csv
├── README.md
│
└── charts/
    ├── monthly_pollution.png
    ├── hourly_pollution.png
    ├── correlation_heatmap.png
    └── temperature_vs_co.png
```

## Libraries Required

Install the required libraries using:

```bash
pip install pandas numpy matplotlib seaborn
```

## How to Run

1. Download or clone this repository.
2. Install the required Python libraries.
3. Keep the CSV dataset in the same folder as the Python script.
4. Execute:

```bash
python cie_milestone1.py
```

## Conclusion

This project demonstrates how Python and Pandas can be used to analyze real-world air quality data. Missing values were handled using mean imputation, additional features were created through data transformation, meaningful insights were generated and the results were presented through visualizations.

The project provides practical experience in data preprocessing, analysis and visualization.

## Dataset Reference

UCI Machine Learning Repository – Air Quality Dataset.

https://archive.ics.uci.edu/dataset/360/air+quality