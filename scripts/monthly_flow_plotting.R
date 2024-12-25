library(ggplot2)

# Define the path to your CSV file
file_path <- "F:/E/Master courses/Semesters/Thesis/New/Hydrologic Model/Excel Files/Output_Monthly_flow_cha072.csv"

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

# Create a new column for Month-Year
plot_data$Month_Year <- as.Date(paste(plot_data$Year, plot_data$Month, "1", sep = "-"), "%Y-%m-%d")

# Plot the hydrograph for both simulated and observed flows
library(scales)
plot <- ggplot(plot_data, aes(x = Month_Year)) +
  geom_line(aes(y = Observed_Flow), color = "green", size = 1, linetype = "solid") +
  geom_line(aes(y = Simulated_Flow), color = "blue", size = 1, linetype = "dashed") +
  labs(title = "Observed vs Simulated Flow Hydrograph",
       x = "Month-Year",
       y = "Flow (cms)") +
  scale_x_date(date_labels = "%b-%y", date_breaks = "6 months") +
  scale_y_continuous(
    breaks = seq(0, 125, by = 10), # Set y-axis breaks from 0 to 125 with a step size of 5
    labels = scales::comma_format() # Optional: Format labels with commas (e.g., 1,000)
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(hjust = 0.5, face = "bold"),
    axis.text = element_text(size = 10),
    axis.title = element_text(size = 12)
  )

# Display the plot
print(plot)
