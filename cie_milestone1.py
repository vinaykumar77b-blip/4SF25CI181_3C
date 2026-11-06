
import pandas as pd
import numpy as np
from pathlib import Path

# Read the CSV dataset
file_path = Path(__file__).parent / "AirQualityUCI.csv"

df = pd.read_csv(file_path, sep=';', decimal=',', low_memory=False)

# Remove completely empty columns
df = df.dropna(axis=1, how='all')

# Display dataset information
print("========== DATASET INFORMATION ==========")

print("\nDataset Shape:")
print(df.shape)

print("\nFirst Five Records:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())

print("\nDataset Information:")
df.info()

print("\nStatistical Description:")
print(df.describe().round(2))

# Check actual null values
print("\nActual Null Values in Each Column:")
print(df.isnull().sum())

# Check missing values represented by -200
numeric_columns = df.select_dtypes(include=np.number).columns

print("\nValues Represented by -200:")
print(df[numeric_columns].eq(-200).sum())

print("\nTotal -200 Values:")
print(df[numeric_columns].eq(-200).sum().sum())

print("\n========== DATASET ANALYSIS COMPLETED ==========")


# ==========================================
# DATA CLEANING AND TRANSFORMATION
# ==========================================

print("\n========== DATA CLEANING ==========")

# Step 1: Remove completely empty rows
df = df.dropna(how='all').copy()

print("\nDataset Shape After Removing Empty Rows:")
print(df.shape)

# Step 2: Identify numerical columns
numeric_columns = df.select_dtypes(include=np.number).columns

# Step 3: Replace -200 with NaN
df[numeric_columns] = df[numeric_columns].replace(-200, np.nan)

# Step 4: Display missing values before imputation
print("\nMissing Values Before Imputation:")
missing_values = df[numeric_columns].isnull().sum()
print(missing_values)

# Display missing value percentages
missing_percentage = (
    df[numeric_columns].isnull().mean() * 100
).round(2)

print("\nMissing Value Percentage:")
print(missing_percentage)

# Step 5: Apply mean imputation
column_means = df[numeric_columns].mean()

df[numeric_columns] = df[numeric_columns].fillna(column_means)

print("\nMissing Values After Mean Imputation:")
print(df[numeric_columns].isnull().sum())

# Step 6: Combine Date and Time into DateTime
df['DateTime'] = pd.to_datetime(
    df['Date'].astype(str) + ' ' +
    df['Time'].astype(str).str.replace('.', ':', regex=False),
    format='%d/%m/%Y %H:%M:%S',
    errors='coerce'
)

# Remove rows with invalid dates
df = df.dropna(subset=['DateTime']).copy()

# Step 7: Remove original Date and Time columns
df = df.drop(columns=['Date', 'Time'])

# Step 8: Create new columns
df['Hour'] = df['DateTime'].dt.hour
df['Month'] = df['DateTime'].dt.month
df['Month_Name'] = df['DateTime'].dt.month_name()
df['Day'] = df['DateTime'].dt.day_name()

# Step 9: Display cleaned dataset
print("\nCleaned DataFrame:")
print(df.head())

print("\nCleaned Dataset Information:")
print(df.info())

# Step 10: Save cleaned dataset
output_path = Path(__file__).parent / "cleaned_air_quality.csv"

df.to_csv(output_path, index=False)

print("\nCleaned dataset saved successfully!")
print("File:", output_path)

print("\n========== DATA CLEANING COMPLETED ==========")


# ==========================================
# INSIGHT GENERATION
# ==========================================

print("\n========== INSIGHT GENERATION ==========")

# Create a Year-Month column
df['Year_Month'] = df['DateTime'].dt.to_period('M').astype(str)

# Calculate monthly average pollution levels
monthly_summary = df.groupby('Year_Month')[
    ['CO(GT)', 'NOx(GT)', 'NO2(GT)']
].mean()

print("\nMonthly Average Pollution Levels:")
print(monthly_summary.round(2))

# Calculate hourly average CO levels
hourly_summary = df.groupby('Hour')['CO(GT)'].mean()

print("\nHourly Average CO Levels:")
print(hourly_summary.round(2))

# Find the hour with highest average CO
peak_co_hour = hourly_summary.idxmax()
peak_co_value = hourly_summary.max()

print("\nINSIGHT 1:")
print("Highest average CO level occurs at hour:",
      peak_co_hour)
print("Average CO level:", round(peak_co_value, 2))

# Find the month with highest average NO2
peak_no2_month = monthly_summary['NO2(GT)'].idxmax()
peak_no2_value = monthly_summary['NO2(GT)'].max()

print("\nINSIGHT 2:")
print("Month with highest average NO2:",
      peak_no2_month)
print("Average NO2 level:", round(peak_no2_value, 2))

# Calculate pollutant correlations
pollutant_columns = [
    'CO(GT)',
    'C6H6(GT)',
    'NOx(GT)',
    'NO2(GT)'
]

correlation = df[pollutant_columns].corr()

# Find the strongest correlation between two pollutants
correlation_pairs = []

for i in range(len(pollutant_columns)):
    for j in range(i + 1, len(pollutant_columns)):
        value = correlation.iloc[i, j]
        correlation_pairs.append(
            (pollutant_columns[i],
             pollutant_columns[j],
             value)
        )

strongest_pair = max(
    correlation_pairs,
    key=lambda x: abs(x[2])
)

print("\nINSIGHT 3:")
print("Strongest correlation is between:",
      strongest_pair[0], "and", strongest_pair[1])
print("Correlation value:",
      round(strongest_pair[2], 3))

# Calculate temperature and CO relationship
temperature_correlation = df['T'].corr(df['CO(GT)'])

print("\nINSIGHT 4:")
print("Correlation between Temperature and CO:",
      round(temperature_correlation, 3))

# Save the updated cleaned dataset
df.to_csv(output_path, index=False)

print("\n========== INSIGHT GENERATION COMPLETED ==========")

# ==========================================
# DATA VISUALIZATION
# ==========================================

import matplotlib.pyplot as plt

print("\n========== CREATING CHARTS ==========")

# Create charts folder
charts_path = Path(__file__).parent / "charts"
charts_path.mkdir(exist_ok=True)

# CHART 1: Monthly NO2 Pollution Trend
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_summary.index,
    monthly_summary['NO2(GT)'],
    marker='o'
)

plt.title("Monthly Average NO2 Pollution Trend")
plt.xlabel("Year and Month")
plt.ylabel("Average NO2 Level")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.savefig(
    charts_path / "monthly_pollution.png",
    dpi=300
)
plt.close()


# CHART 2: Hourly CO Pollution Trend
plt.figure(figsize=(10, 6))

plt.plot(
    hourly_summary.index,
    hourly_summary.values,
    marker='o'
)

plt.title("Hourly Average CO Pollution")
plt.xlabel("Hour of the Day")
plt.ylabel("Average CO Level")
plt.xticks(range(0, 24))
plt.grid(True)
plt.tight_layout()

plt.savefig(
    charts_path / "hourly_pollution.png",
    dpi=300
)
plt.close()


# CHART 3: Pollutant Correlation Heatmap
plt.figure(figsize=(9, 7))

plt.imshow(
    correlation,
    cmap='coolwarm',
    vmin=-1,
    vmax=1
)

plt.colorbar(label="Correlation")

plt.xticks(
    range(len(pollutant_columns)),
    pollutant_columns,
    rotation=30,
    ha='right'
)

plt.yticks(
    range(len(pollutant_columns)),
    pollutant_columns
)

for i in range(len(pollutant_columns)):
    for j in range(len(pollutant_columns)):
        plt.text(
            j, i,
            f"{correlation.iloc[i, j]:.2f}",
            ha='center',
            va='center'
        )

plt.title("Pollutant Correlation Heatmap")
plt.tight_layout()

plt.savefig(
    charts_path / "correlation_heatmap.png",
    dpi=300
)
plt.close()


# CHART 4: Temperature vs CO
plt.figure(figsize=(10, 6))

plt.scatter(
    df['T'],
    df['CO(GT)'],
    alpha=0.35,
    s=12
)

plt.title("Temperature vs CO Levels")
plt.xlabel("Temperature (Celsius)")
plt.ylabel("CO Level")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    charts_path / "temperature_vs_co.png",
    dpi=300
)
plt.close()


print("\nAll four charts created successfully!")

print("Charts saved in:", charts_path)

print("\n========== VISUALIZATION COMPLETED ==========")
