# Load required library
# ggplot2 is used for creating the plot
library(ggplot2)

# Define the path to your CSV file
# Replace this file path with the actual location of your CSV file
file_path <- "F:/E/Master courses/Semesters/Thesis/New/Hydrologic Model/Excel Files/Output_Monthly_flow_cha072.csv"

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

# Combine the extracted columns into a new data frame for easier processing and plotting
# The new data frame will have columns: Month, Year, Simulated_Flow, Observed_Flow
plot_data <- data.frame(
  Month = months,               # Assign months
  Year = years,                 # Assign years
  Simulated_Flow = simulated_flows,  # Assign simulated flow data
  Observed_Flow = observed_flows   # Assign observed flow data
)

# Create a new column for Month-Year in the format YYYY-MM
# This will combine Year and Month columns into a single date-like column
plot_data$Month_Year <- as.Date(paste(plot_data$Year, plot_data$Month, "1", sep = "-"), "%Y-%m-%d")

# Plot the hydrograph for both simulated and observed flows
# Using ggplot2 to create a line plot with customizations
library(scales)  # Load 'scales' package for formatting the axis labels

plot <- ggplot(plot_data, aes(x = Month_Year)) +
  # Plot the observed flow as a solid green line
  geom_line(aes(y = Observed_Flow), color = "green", size = 1, linetype = "solid") +
  # Plot the simulated flow as a dashed blue line
  geom_line(aes(y = Simulated_Flow), color = "blue", size = 1, linetype = "dashed") +
  # Add labels and titles
  labs(title = "Observed vs Simulated Flow Hydrograph",
       x = "Month-Year",  # Label for x-axis
       y = "Flow (cms)")  # Label for y-axis
  # Customize the x-axis labels to show Month-Year (e.g., Jan-2015, Feb-2015, etc.)
  + scale_x_date(date_labels = "%b-%y", date_breaks = "6 months") +
  # Customize the y-axis: Set breaks and format labels with commas
  + scale_y_continuous(
    breaks = seq(0, 125, by = 10),  # Set y-axis breaks from 0 to 125 with a step size of 10
    labels = scales::comma_format()  # Optional: Format labels with commas (e.g., 1,000)
  ) +
  # Use a minimal theme for the plot
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),  # Center and bold the title
    axis.text = element_text(size = 10),  # Adjust font size of axis labels
    axis.title = element_text(size = 12)  # Adjust font size of axis titles
  )

# Display the plot
# This will render the plot created using ggplot2
print(plot)