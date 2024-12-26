# Load required libraries
# ggplot2 for creating plots, dplyr for data manipulation, and tidyr for reshaping data
library(ggplot2)  # For creating visualizations
library(dplyr)    # For data manipulation and transformations
library(tidyr)    # For reshaping data (wide to long format)

# Define the path to your CSV file
# Replace with the actual file path on your system
file_path <- "F:/E/Master courses/Semesters/Thesis/New/Hydrologic Model/Excel Files/Output_Year_flow_cha072.csv"

# Read the CSV file into a data frame
# The `header = TRUE` argument ensures the first row is used as column names
data <- read.csv(file_path, header = TRUE)

# Extract relevant columns from the data frame
# We are assuming that the file structure has:
# 2nd column = Months, 4th column = Year, 5th column = Simulated Flow, 6th column = Observed Flow
months <- data[[2]]  # Extract month data (from 2nd column)
years <- data[[4]]   # Extract year data (from 4th column)
simulated_flows <- data[[5]]  # Extract simulated flow data (from 5th column)
observed_flows <- data[[6]]   # Extract observed flow data (from 6th column)

# Combine the extracted columns into a new data frame for easy plotting
# The new data frame will have columns: Month, Year, Simulated_Flow, Observed_Flow
plot_data <- data.frame(
  Month = months,               # Assign months
  Year = years,                 # Assign years
  Simulated_Flow = simulated_flows,  # Assign simulated flow data
  Observed_Flow = observed_flows   # Assign observed flow data
)

# Reshape the data from wide format to long format using pivot_longer
# This allows us to stack the 'Simulated_Flow' and 'Observed_Flow' columns into a single column for plotting
long_data <- plot_data %>%
  pivot_longer(cols = c(Simulated_Flow, Observed_Flow),  # Specify columns to reshape
               names_to = "Flow_Type",                   # Create a new column for the flow type (Simulated/Observed)
               values_to = "Flow")                       # Create a new column for the flow values

# Recode the 'Flow_Type' column to use more user-friendly labels for easier interpretation
long_data <- long_data %>%
  mutate(Flow_Type = recode(Flow_Type, 
                           Simulated_Flow = "Simulated",   # Rename "Simulated_Flow" to "Simulated"
                           Observed_Flow = "Observed"))    # Rename "Observed_Flow" to "Observed"

# Create the grouped bar chart using ggplot2
# The chart will compare the simulated and observed flow values for each year
bar_plot <- ggplot(long_data, aes(x = factor(Year), y = Flow, fill = Flow_Type)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +  # Create bars with dodge position for grouping
  labs(title = "Observed vs Simulated Flow Per Year",   # Set the plot title
       x = "Year",                                      # Set the x-axis label
       y = "Flow (cms)")                                # Set the y-axis label (flow in cubic meters per second)
  scale_fill_manual(values = c("light green", "light blue")) +  # Customize bar colors for simulated and observed flows
  theme_minimal() +  # Use a minimal theme for a cleaner plot
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),  # Center and bold the plot title
    axis.text = element_text(size = 12),                    # Adjust the font size of axis labels
    axis.title = element_text(size = 14)                    # Adjust the font size of axis titles
  )

# Display the generated bar chart
# This will render the plot created above
print(bar_plot)