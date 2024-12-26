import pandas as pd

# Usage example: Define the paths for the input file and output file
input_file = r'F:\E\Master courses\Github\Swat+ HSPF\Observed flow.txt'  # Replace with your input text file path
output_file = r'F:\E\Master courses\Github\Swat+ HSPF\Observed_Flow_cha072.xlsx'  # Replace with the new target Excel file name

def extract_and_import_flow_data(input_file, output_file):
    # Step 1: Load the text file into a DataFrame
    # Read the data from the input file, skipping the first 25 rows of metadata
    data = pd.read_csv(input_file, sep='\s+', skiprows=25, header=None)

    # Step 2: Assign column names to the DataFrame for clarity
    data.columns = ['agency_cd', 'site_no', 'datetime', 'flow', 'qualifier']

    # Step 3: Clean up the 'flow' column to keep only numeric values
    # Convert the 'flow' column to numeric, coercing any errors (non-numeric values) into NaN
    data['flow'] = pd.to_numeric(data['flow'], errors='coerce')
    # Drop rows where 'flow' is NaN (invalid data)
    data = data.dropna(subset=['flow'])

    # Step 4: Convert the 'datetime' column to a proper datetime format
    # Convert the 'datetime' column to datetime, coercing any errors (invalid date formats) into NaT
    data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')
    # Drop rows with invalid datetime values
    data = data.dropna(subset=['datetime'])

    # Step 5: Extract day, month, and year from the 'datetime' column
    data['day'] = data['datetime'].dt.day  # Extract the day from the 'datetime'
    data['month'] = data['datetime'].dt.month  # Extract the month from the 'datetime'
    data['year'] = data['datetime'].dt.year  # Extract the year from the 'datetime'

    # Step 6: Prepare the final data for daily flow with the relevant columns
    # Keep only the columns 'day', 'month', 'year', and 'flow', renaming 'flow' to 'Observed Flow (cfs)'
    daily_data = data[['day', 'month', 'year', 'flow']].rename(columns={'flow': 'Observed Flow (cfs)'})

    # Step 7: Calculate the monthly average flow
    # Group data by year and month, and calculate the mean of 'Observed Flow (cfs)'
    monthly_data = daily_data.groupby(['year', 'month'], as_index=False)['Observed Flow (cfs)'].mean()

    # Step 8: Calculate the annual average flow
    # Group data by year, and calculate the mean of 'Observed Flow (cfs)'
    annual_data = daily_data.groupby('year', as_index=False)['Observed Flow (cfs)'].mean()

    # Step 9: Save all the data to an Excel file with separate sheets for daily, monthly, and annual data
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Save daily data to the 'daily' sheet
        daily_data.to_excel(writer, sheet_name='daily', index=False)

        # Save monthly data to the 'monthly' sheet
        monthly_data.to_excel(writer, sheet_name='monthly', index=False)

        # Save annual data to the 'annually' sheet
        annual_data.to_excel(writer, sheet_name='annually', index=False)

    # Step 10: Print confirmation message
    print(f"Flow data has been extracted and saved into {output_file}.")

# Run the function with the provided file paths
extract_and_import_flow_data(input_file, output_file)
