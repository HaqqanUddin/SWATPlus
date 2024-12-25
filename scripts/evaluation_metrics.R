# Define the path to your CSV file
file_path <- "F:/E/Master courses/Semesters/Thesis/New/Hydrologic Model/Excel Files/Output_Year_flow_cha072.csv"

# Read the CSV file
data <- read.csv(file_path, header = TRUE)

# Extract relevant columns
# Assuming the structure: 2nd column = Months, 4th column = Year, 5th column = Simulated Flow, 6th column = Observed Flow
months <- data[[2]]
years <- data[[4]]
simulated_flows <- data[[5]]
observed_flows <- data[[6]]

# Combine data into a data frame
plot_data <- data.frame(
  Month = months,
  Year = years,
  Simulated_Flow = simulated_flows,
  Observed_Flow = observed_flows
)

# Calculate NSE
nse <- 1 - sum((observed_flows - simulated_flows)^2) / sum((observed_flows - mean(observed_flows))^2)
cat("Nash-Sutcliffe Efficiency (NSE):", nse, "\n")

# Calculate RMSE
rmse <- sqrt(mean((observed_flows - simulated_flows)^2))
cat("Root Mean Square Error (RMSE):", rmse, "\n")

# Calculate R²
r_squared <- cor(observed_flows, simulated_flows)^2
cat("Coefficient of Determination (R²):", r_squared, "\n")

# Calculate PBIAS
pbias <- 100 * sum(observed_flows - simulated_flows) / sum(observed_flows)
cat("Percent Bias (PBIAS):", pbias, "%\n")