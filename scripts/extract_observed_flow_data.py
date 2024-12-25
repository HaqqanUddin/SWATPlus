import pandas as pd

# Usage example
input_file = r'F:\E\Master courses\Github\Swat+ HSPF\Observed flow.txt'  # Replace with your input text file path
output_file = r'F:\E\Master courses\Github\Swat+ HSPF\Observed_Flow_cha072.xlsx'  # Replace with the new target Excel file name

def extract_and_import_flow_data(input_file, output_file):
    # Load the text file as a DataFrame, skipping unnecessary rows
    data = pd.read_csv(input_file, sep='\s+', skiprows=25, header=None)

    # Assign column names based on structure
    data.columns = ['agency_cd', 'site_no', 'datetime', 'flow', 'qualifier']

    # Ensure 'flow' contains only numeric values, dropping non-numeric rows
    data['flow'] = pd.to_numeric(data['flow'], errors='coerce')
    data = data.dropna(subset=['flow'])

    # Convert 'datetime' column to datetime format
    data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')
    data = data.dropna(subset=['datetime'])  # Drop rows with invalid datetime

    # Create new columns for day, month, and year
    data['day'] = data['datetime'].dt.day
    data['month'] = data['datetime'].dt.month
    data['year'] = data['datetime'].dt.year

    # Prepare the final data for daily flow with the desired columns: day, month, year, and Observed Flow
    daily_data = data[['day', 'month', 'year', 'flow']].rename(columns={'flow': 'Observed Flow (cfs)'})

    # Calculate monthly averages
    monthly_data = daily_data.groupby(['year', 'month'], as_index=False)['Observed Flow (cfs)'].mean()

    # Calculate annual averages
    annual_data = daily_data.groupby('year', as_index=False)['Observed Flow (cfs)'].mean()

    # Save all data to an Excel file with three separate sheets
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Add daily data to 'daily' sheet
        daily_data.to_excel(writer, sheet_name='daily', index=False)

        # Add monthly data to 'monthly' sheet
        monthly_data.to_excel(writer, sheet_name='monthly', index=False)

        # Add annual data to 'annually' sheet
        annual_data.to_excel(writer, sheet_name='annually', index=False)

    print(f"Flow data has been extracted and saved into {output_file}.")

extract_and_import_flow_data(input_file, output_file)
