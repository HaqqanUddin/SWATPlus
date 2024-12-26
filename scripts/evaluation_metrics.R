# Define the path to your CSV file
# Replace this file path with the actual location of your CSV file
file_path <- "F:/E/Master courses/Semesters/Thesis/New/Hydrologic Model/Excel Files/Output_Year_flow_cha072.csv"

# Read the CSV file into a data frame
# header = TRUE ensures that the first row of the CSV file is treated as column names
data <- read.csv(file_path, header = TRUE)

# Extract relevant columns from the data
# Assuming the structure of the CSV file:
# 2nd column = Months, 4th column = Year, 5th column = Simulated Flow, 6th column = Observed Flow
months <- data[[2]]  # Extract the month data (from the 2nd column)
years <- data[[4]]   # Extract the year data (from the 4th column)
simulated_flows <- data[[5]]  # Extract simulated flow data (from the 5th column)
observed_flows <- data[[6]]   # Extract observed flow data (from the 6th column)

# Combine the extracted columns into a new data frame for easier processing and analysis
# The new data frame will have columns: Month, Year, Simulated_Flow, Observed_Flow
plot_data <- data.frame(
  Month = months,               # Assign months
  Year = years,                 # Assign years
  Simulated_Flow = simulated_flows,  # Assign simulated flow data
  Observed_Flow = observed_flows   # Assign observed flow data
)

# Calculate the Nash-Sutcliffe Efficiency (NSE) to evaluate the goodness of model predictions
# NSE = 1 - (sum of squared differences between observed and simulated) / (sum of squared differences from the mean of observed)
nse <- 1 - sum((observed_flows - simulated_flows)^2) / sum((observed_flows - mean(observed_flows))^2)
cat("Nash-Sutcliffe Efficiency (NSE):", nse, "\n")  # Print the NSE value

# Calculate the Root Mean Square Error (RMSE) to assess the model's prediction accuracy
# RMSE = square root of the average of squared differences between observed and simulated
rmse <- sqrt(mean((observed_flows - simulated_flows)^2))
cat("Root Mean Square Error (RMSE):", rmse, "\n")  # Print the RMSE value

# Calculate the Coefficient of Determination (R²) to measure the proportion of variance explained by the model
# R² is the square of the correlation coefficient between observed and simulated flows
r_squared <- cor(observed_flows, simulated_flows)^2
cat("Coefficient of Determination (R²):", r_squared, "\n")  # Print the R² value

# Calculate the Percent Bias (PBIAS) to evaluate model over- or under-estimation
# PBIAS = 100 * (sum of differences between observed and simulated) / sum of observed values
pbias <- 100 * sum(observed_flows - simulated_flows) / sum(observed_flows)
cat("Percent Bias (PBIAS):", pbias, "%\n")  # Print the PBIAS value