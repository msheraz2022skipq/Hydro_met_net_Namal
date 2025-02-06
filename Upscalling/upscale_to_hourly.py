import pandas as pd
import numpy as np
file_path_input = 'Namal Catchement Dataset-Original.xlsx'

####################################   Rain   ##############################################

df_rain = pd.read_excel(file_path_input, sheet_name='Precipitation Rate', parse_dates=['Timestamp'])
df_rain.set_index('Timestamp', inplace=True)
hourly_avg_rain = df_rain.resample('H').apply(
    lambda x: x.mean()*6 if not x.isna().all().any() and x.notna().sum() >= 0.6 * len(x) else np.nan
)

file_path_output = 'HourlyPrecipitation-60%.xlsx'
hourly_avg_rain.to_excel(file_path_output, sheet_name='Hourly Precipitation')

print(f'Hourly Rain data written to {file_path_output}.')

####################################   Lake Level   ##############################################

df_LakeLevel = pd.read_excel(file_path_input, sheet_name='Lake Level', parse_dates=['Timestamp'])
df_LakeLevel.set_index('Timestamp', inplace=True)
hourly_median_LakeLevel = df_LakeLevel.resample('H').apply(
    lambda x: x.median() if not x.isna().all().any() else np.nan
)

file_path_output = 'HourlyLakeLevel.xlsx'
hourly_median_LakeLevel.to_excel(file_path_output, sheet_name='HourlyLakeLevel')

print(f'Hourly Lake Level data written to {file_path_output}.')

####################################   Stream Level   ##############################################

df_StreamLevel = pd.read_excel(file_path_input, sheet_name='Stream Levels', parse_dates=['Timestamp'])
df_StreamLevel.set_index('Timestamp', inplace=True)
hourly_max_StreamLevel = df_StreamLevel.resample('H').apply(
    lambda x: x.max() if not x.isna().all().any() else np.nan
)

file_path_output = 'HourlyStreamLevel.xlsx'
hourly_max_StreamLevel.to_excel(file_path_output, sheet_name='HourlyStreamLevel')

print(f'Hourly Lake Level data written to {file_path_output}.')


file_name = 'HourlyData.xlsx'

# Create an Excel writer
with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
    # Save each DataFrame to a different sheet
    hourly_avg_rain.to_excel(writer, sheet_name='Hourly Precipitation')
    hourly_median_LakeLevel.to_excel(writer, sheet_name='HourlyLakeLevel')
    hourly_max_StreamLevel.to_excel(writer, sheet_name='HourlyStreamLevel')