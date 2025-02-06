import pandas as pd
from tqdm import tqdm

# Read the Excel file
file_path = 'Clean Data 01Apr-30Sep2024.xlsx'
sheet_name = 'Precipitation'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Convert Timestamp column to datetime type
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

total_missing = df.isnull().sum().sum()

# Initialize tqdm for tracking progress
with tqdm(total=total_missing, desc="Filling Missing Data") as pbar:
    # Iterate through each column except the first one (Timestamp)
    for col in df.columns[1:]:
        print('Processing ', col)
        
        # Filter out rainy (non-empty) days
        non_empty_days = df[df[col].notnull()]['Timestamp'].dt.date.unique()

        # Iterate through each non-empty day
        for day in non_empty_days:
            # Get missing indices for the day
            missing_indices = df[(df['Timestamp'].dt.date == day) & (df[col].isnull())].index

            # Iterate through missing indices
            for index in missing_indices:
                # Increment progress bar for each missing value processed
                pbar.update(1)

                # Find the next available value after the gap
                next_available_index = index + 1
                while next_available_index in missing_indices:
                    next_available_index += 1

                # Check if the next available value exists and the previous and next available values are the same
                if next_available_index < len(df) and df[col].iloc[index - 1] == df[col].iloc[next_available_index]:
                    # Check if the last available value and next available value have the same date
                    last_available_date = df['Timestamp'].iloc[index - 1].date()
                    next_available_date = df['Timestamp'].iloc[next_available_index].date()
                    if last_available_date == next_available_date:
                        # Fill the missing values within the gap with the same value
                        df.loc[index:next_available_index, col] = df[col].iloc[index - 1]

# Save the filled data to a new Excel file
new_file_path = 'Clean Data 01Apr-30Sep2024-GapFilled.xlsx'
df.to_excel(new_file_path, index=False)

print("Filled data saved to", new_file_path)

################ Handle Misleading Zeros between two non-zero readings ###########

import pandas as pd
# Load the Excel file
file_path = "Clean Data 01Apr-30Sep2024-GapFilled.xlsx"
df = pd.read_excel(file_path)
print('Processing data to handle misleading zeros')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
daily_groups = df.groupby(df['Timestamp'].dt.date)
for col in df.columns[1:]:
    print('Processing', col)
    updated_values = df[col].copy()
    
    for date, group in daily_groups:
        group_filtered = group[group['Timestamp'].dt.time > pd.Timestamp('00:00:00').time()]

        non_zero_indices = group_filtered[group_filtered[col] != 0].index
        zero_indices = group_filtered[group_filtered[col] == 0].index

        if non_zero_indices.empty:
            continue
        
        non_zero_values = group_filtered.loc[non_zero_indices, col].values
        non_zero_values_indices = non_zero_indices        
        non_zero_dict = dict(zip(non_zero_values_indices, non_zero_values))
        
        for idx in zero_indices:
            prev_non_zero = group_filtered.loc[group_filtered.index < idx, col].replace(0, pd.NA).last_valid_index()
            next_non_zero = group_filtered.loc[group_filtered.index > idx, col].replace(0, pd.NA).first_valid_index()
            
            if prev_non_zero is not None and next_non_zero is not None:
                prev_val = non_zero_dict[prev_non_zero]
                next_val = non_zero_dict[next_non_zero]
                
                if prev_val == next_val:
                    updated_values.at[idx] = prev_val
                else:
                    updated_values.at[idx] = None
    df[col] = updated_values
df.to_excel("Clean Data 01Apr-30Sep2024-FinalData-Precipitation.xlsx", index=False)
print("Final data saved...")
