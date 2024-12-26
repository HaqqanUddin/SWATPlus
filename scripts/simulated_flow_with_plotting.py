import os
import pandas as pd
import warnings
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Suppress warnings
warnings.filterwarnings('ignore')

# Define parameter and channel ID
parameter = "        flo_out"  # Enter Parameter here
channel_id = "cha001"  # Replace with the desired channel ID

# Get the current working directory
current_working_dir = os.getcwd()
print(f"Current working directory: {current_working_dir}")

# Load data from CSV files
data_day_path = r'D:\D\Abdullah Azzam\BHL SWAT+\SWAT\F23_1\Scenarios\Default\TxtInOut\channel_sd_day.csv'
data_yr_path = r'D:\D\Abdullah Azzam\BHL SWAT+\SWAT\F23_1\Scenarios\Default\TxtInOut\channel_sd_yr.csv'
data_mon_path = r'D:\D\Abdullah Azzam\BHL SWAT+\SWAT\F23_1\Scenarios\Default\TxtInOut\channel_sd_mon.csv'

print(f"Loading data from:\n{data_day_path}\n{data_yr_path}\n{data_mon_path}")

try:
    data_day = pd.read_csv(data_day_path, skiprows=1)
    data_yr = pd.read_csv(data_yr_path, skiprows=1)
    data_mon = pd.read_csv(data_mon_path, skiprows=1)
    print("Data loaded successfully.")
except Exception as e:
    print(f"Error loading data: {e}")
    exit()

# Extract relevant columns
try:
    all_channels_flow_day = data_day[['   name        ', '   mon', '   day', '    yr', parameter]]
    all_channels_flow_yr = data_yr[['   name        ', '   mon', '   day', '    yr', parameter]]
    all_channels_flow_mon = data_mon[['   name        ', '   mon', '   day', '    yr', parameter]]
    print("Relevant columns extracted successfully.")
except KeyError as e:
    print(f"Error extracting columns: {e}")
    exit()

# Rename the flow column
all_channels_flow_day.rename(columns={parameter: 'Simulated Flow'}, inplace=True)
all_channels_flow_yr.rename(columns={parameter: 'Simulated Flow'}, inplace=True)
all_channels_flow_mon.rename(columns={parameter: 'Simulated Flow'}, inplace=True)

# Convert 'Simulated Flow' to numeric, forcing errors to NaN (useful for non-numeric data)
all_channels_flow_day['Simulated Flow'] = pd.to_numeric(all_channels_flow_day['Simulated Flow'], errors='coerce')
all_channels_flow_yr['Simulated Flow'] = pd.to_numeric(all_channels_flow_yr['Simulated Flow'], errors='coerce')
all_channels_flow_mon['Simulated Flow'] = pd.to_numeric(all_channels_flow_mon['Simulated Flow'], errors='coerce')

# Convert 'day', 'mon', 'yr' columns to numeric to avoid any text formatting issues
all_channels_flow_day['   day'] = pd.to_numeric(all_channels_flow_day['   day'], errors='coerce')
all_channels_flow_day['   mon'] = pd.to_numeric(all_channels_flow_day['   mon'], errors='coerce')
all_channels_flow_day['    yr'] = pd.to_numeric(all_channels_flow_day['    yr'], errors='coerce')

all_channels_flow_yr['   day'] = pd.to_numeric(all_channels_flow_yr['   day'], errors='coerce')
all_channels_flow_yr['   mon'] = pd.to_numeric(all_channels_flow_yr['   mon'], errors='coerce')
all_channels_flow_yr['    yr'] = pd.to_numeric(all_channels_flow_yr['    yr'], errors='coerce')

all_channels_flow_mon['   day'] = pd.to_numeric(all_channels_flow_mon['   day'], errors='coerce')
all_channels_flow_mon['   mon'] = pd.to_numeric(all_channels_flow_mon['   mon'], errors='coerce')
all_channels_flow_mon['    yr'] = pd.to_numeric(all_channels_flow_mon['    yr'], errors='coerce')

# Filter data for the specified channel ID
print(f"Filtering data for channel ID: {channel_id}")

selected_rows_day = all_channels_flow_day[all_channels_flow_day['   name        '].str.contains(channel_id)]
selected_rows_yr = all_channels_flow_yr[all_channels_flow_yr['   name        '].str.contains(channel_id)]
selected_rows_mon = all_channels_flow_mon[all_channels_flow_mon['   name        '].str.contains(channel_id)]

# Debug: Print number of rows selected for each time period
print(f"Rows selected for daily flow: {len(selected_rows_day)}")
print(f"Rows selected for yearly flow: {len(selected_rows_yr)}")
print(f"Rows selected for monthly flow: {len(selected_rows_mon)}")

# Drop the first column and its data
selected_rows_day = selected_rows_day.iloc[:, 1:]
selected_rows_yr = selected_rows_yr.iloc[:, 1:]
selected_rows_mon = selected_rows_mon.iloc[:, 1:]

# Define output Excel file name
output_dir = r'F:\E\Master courses\Github\Swat+ HSPF'
output_excel_file = os.path.join(output_dir, f"Simulated_Flow_{channel_id}.xlsx")

# Export data to a single Excel file with multiple sheets
print(f"Exporting data to Excel file: '{output_excel_file}'")

try:
    with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
        selected_rows_day.to_excel(writer, sheet_name='daily', index=False)
        selected_rows_mon.to_excel(writer, sheet_name='monthly', index=False)
        selected_rows_yr.to_excel(writer, sheet_name='annually', index=False)
    print("File exported successfully.")
except Exception as e:
    print(f"Error exporting file: {e}")
    exit()

# File paths
obs_file = r"F:\E\Master courses\Github\Swat+ HSPF\Observed_Flow_cha001.xlsx"
sim_file = r"F:\E\Master courses\Github\Swat+ HSPF\Simulated_Flow_cha072.xlsx"

# Load observed and simulated daily data
observed_daily = pd.read_excel(obs_file, sheet_name="daily", usecols=[3])  # Assuming the 4th column contains observed flow
simulated_daily = pd.read_excel(sim_file, sheet_name="daily", usecols=[0, 1, 2, 3])  # Columns for month, day, year, simulated flow

# Rename columns for clarity
observed_daily.columns = ["Observed Flow"]
simulated_daily.columns = ["month", "day", "year", "Simulated Flow"]

# Combine observed and simulated data for daily data
daily_data = pd.concat([simulated_daily, observed_daily], axis=1)

# Drop rows with missing values for daily data
daily_data.dropna(inplace=True)

# Create a datetime index for daily data
daily_data["date"] = pd.to_datetime(daily_data[["year", "month", "day"]], errors="coerce")

# Drop rows with invalid dates for daily data
daily_data.dropna(subset=["date"], inplace=True)

# Set the date as the index for daily data
daily_data.set_index("date", inplace=True)

# Plotting Daily Data: Observed vs Simulated Flow
plt.figure(figsize=(12, 6))
plt.plot(daily_data.index, daily_data["Observed Flow"], label="Observed Flow", color="blue", linewidth=1.0)
plt.plot(daily_data.index, daily_data["Simulated Flow"], label="Simulated Flow", color="orange", linewidth=1.0, linestyle="--")
plt.title("Daily Flow Hydrograph")
plt.xlabel("Date")
plt.ylabel("Flow (cfs)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show(block=False)  # Make this non-blocking

import pandas as pd
import matplotlib.pyplot as plt

# Load observed and simulated monthly data
observed_monthly = pd.read_excel(obs_file, sheet_name="monthly", usecols=[2])  # Adjust index if necessary
simulated_monthly = pd.read_excel(sim_file, sheet_name="monthly", usecols=[2, 0, 3])  # Year, Month, Simulated Flow

# Rename columns for clarity
observed_monthly.columns = ["Observed Flow"]
simulated_monthly.columns = ["Year", "Month", "Simulated Flow"]

# Combine observed and simulated data for monthly data
monthly_data = pd.concat([simulated_monthly, observed_monthly], axis=1)

# Create a combined "Month-Year" label as a string (correctly formatted)
monthly_data["Label"] = monthly_data["Month"].astype(str).str.zfill(2) + "-" + monthly_data["Year"].astype(str)

# Ensure the 'Label' column is treated as a string, not a numerical value
monthly_data["Label"] = monthly_data["Label"].astype(str)

# Plot the data
plt.figure(figsize=(14, 8))

# Plot observed flow
plt.plot(
    monthly_data["Label"],
    monthly_data["Observed Flow"],
    label="Observed Flow (cfs)",
    color="blue",
    linewidth=1,
)

# Plot simulated flow
plt.plot(
    monthly_data["Label"],
    monthly_data["Simulated Flow"],
    label="Simulated Flow (cfs)",
    color="orange",
    linestyle="--",
    linewidth=1,
)

# Set title and axis labels
plt.title("Monthly Flow Hydrograph", fontsize=12)
plt.xlabel("Months", fontsize=11)
plt.ylabel("Flows (cfs)", fontsize=11)

# Adjust x-axis ticks to display Month-Year at an interval
plt.xticks(
    monthly_data["Label"][::12],  # Show every 12th month for better spacing (adjust as needed)
    monthly_data["Label"][::12],  # Use the custom "Month-Year" label
    rotation=45,
    fontsize=12,
)

# Add legend and grid
plt.legend(fontsize=12, loc="upper left")
plt.grid(True, linestyle="--", alpha=0.7)

# Adjust layout and show the plot
plt.tight_layout()
plt.show(block=False)

# Load annual observed and simulated data
annual_observed = pd.read_excel(obs_file, sheet_name="annually", usecols=[0, 1])  # Year, Observed Flow
annual_simulated = pd.read_excel(sim_file, sheet_name="annually", usecols=[2, 3])  # Year, Simulated Flow

# Rename columns for clarity
annual_observed.columns = ["Year", "Observed Flow"]
annual_simulated.columns = ["Year", "Simulated Flow"]

# Merge annual observed and simulated data
annual_data = pd.merge(annual_observed, annual_simulated, on="Year", how="inner")

# Plotting Annual Data: Observed vs Simulated Flow
plt.figure(figsize=(12, 6))
width = 0.35  # Width of each bar
x = np.arange(len(annual_data["Year"]))  # X-axis positions for each year

# Plot observed and simulated bars
plt.bar(x - width / 2, annual_data["Observed Flow"], width, label="Observed Flow", color="blue", alpha=0.7)
plt.bar(x + width / 2, annual_data["Simulated Flow"], width, label="Simulated Flow", color="orange", alpha=0.7)

# Formatting the chart
plt.title("Annual Flow")
plt.xlabel("Year")
plt.ylabel("Flow (cfs)")
plt.xticks(x, annual_data["Year"].astype(int), rotation=45)  # Label x-axis with years
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()  # This will now show the second plot after the first one

def calculate_metrics(obs, sim):
    # Check if the variance of observed values is zero
    variance_obs = sum((obs - np.mean(obs)) ** 2)
    if variance_obs == 0:
        nse = np.nan  # or assign some other value like 0 or a warning message
    else:
        nse = 1 - sum((obs - sim) ** 2) / variance_obs
    
    r2 = linregress(obs, sim).rvalue ** 2
    rmse = np.sqrt(np.mean((obs - sim) ** 2))
    pbias = 100 * (sum(sim - obs) / sum(obs))
    
    return {"NSE": nse, "R²": r2, "RMSE": rmse, "PBIAS": pbias}

# Calculate metrics for daily data
metrics_daily = calculate_metrics(daily_data["Observed Flow"], daily_data["Simulated Flow"])

# Print metrics for daily data
print("\nPerformance Metrics for Daily Data:")
for metric, value in metrics_daily.items():
    print(f"{metric}: {value:.4f}")

# Calculate metrics for monthly data
metrics_monthly = calculate_metrics(monthly_data["Observed Flow"], monthly_data["Simulated Flow"])

# Print metrics for monthly data
print("\nPerformance Metrics for Monthly Data:")
for metric, value in metrics_monthly.items():
    print(f"{metric}: {value:.4f}")

# Calculate metrics for annual data
metrics_annual = calculate_metrics(annual_data["Observed Flow"], annual_data["Simulated Flow"])

# Print metrics for annual data
print("\nPerformance Metrics for Annual Data:")
for metric, value in metrics_annual.items():
    print(f"{metric}: {value:.4f}")