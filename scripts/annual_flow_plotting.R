# Load required libraries
library(ggplot2)
library(dplyr)
library(tidyr)

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

# Reshape the data to long format
long_data <- plot_data %>%
  pivot_longer(cols = c(Simulated_Flow, Observed_Flow), 
               names_to = "Flow_Type", 
               values_to = "Flow") %>%
  mutate(Flow_Type = recode(Flow_Type, 
                           Simulated_Flow = "Simulated", 
                           Observed_Flow = "Observed"))

# Create the grouped bar chart
bar_plot <- ggplot(long_data, aes(x = factor(Year), y = Flow, fill = Flow_Type)) +
  geom_bar(stat = "identity", position = position_dodge(width = 0.8), width = 0.7) +
  labs(title = "Observed vs Simulated Flow Per Year",
       x = "Year",
       y = "Flow (cms)") +
  scale_fill_manual(values = c("light green", "light blue")) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    axis.text = element_text(size = 12),
    axis.title = element_text(size = 14)
  )

# Display the bar chart
print(bar_plot)
