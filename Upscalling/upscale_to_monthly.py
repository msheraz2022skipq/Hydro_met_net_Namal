import pandas as pd
import numpy as np
file_path = 'Namal Catchment Daily Dataset-V3.xlsx'
############################### Monthly Precipitation ###############################
df_precipitation = pd.read_excel(file_path, sheet_name='Daily Precipitation', parse_dates=['Timestamp'])
df_precipitation.set_index('Timestamp', inplace=True)
monthly_precipitation = pd.DataFrame(index=df_precipitation.resample('M').mean().index)
for col in df_precipitation.columns:
    monthly_precipitation[col] = df_precipitation[col].resample('M').apply(
        lambda x: x.mean()*(len(x)) if not x.isna().all().any() and x.notna().sum() >= 0.6 * len(x) else np.nan
    )

file_path_output = 'MonthlyPrecipitation.xlsx'
monthly_precipitation.to_excel(file_path_output, sheet_name='Monthly Precipitation')

print(f'Monthly Precipitation data written to {file_path_output}.')

############################### Monthly Lake Level ###############################

df_lakeLevel = pd.read_excel(file_path, sheet_name='Daily Lake Level', parse_dates=['Timestamp'])
df_lakeLevel.set_index('Timestamp', inplace=True)
monthly_lakeLevel = pd.DataFrame(index=df_lakeLevel.resample('M').mean().index)
for col in df_lakeLevel.columns:
    monthly_lakeLevel[col] = df_lakeLevel[col].resample('M').apply(
        lambda x: x.median()
    )

file_path_output = 'MonthlyLakeLevel.xlsx'
monthly_lakeLevel.to_excel(file_path_output, sheet_name='Monthly Lake Level')

print(f'Monthly Rainfall data written to {file_path_output}.')

############################### Monthly Stream Level ###############################

df_StreamLevel = pd.read_excel(file_path, sheet_name='Daily Stream Level', parse_dates=['Timestamp'])
df_StreamLevel.set_index('Timestamp', inplace=True)
monthly_StreamLevel = pd.DataFrame(index=df_StreamLevel.resample('M').mean().index)
for col in df_StreamLevel.columns:
    monthly_StreamLevel[col] = df_StreamLevel[col].resample('M').apply(
        lambda x: x.max()
    )

file_path_output = 'MonthlyStreamLevel.xlsx'
monthly_StreamLevel.to_excel(file_path_output, sheet_name='Monthly Stream Level')

print(f'Monthly Stream data written to {file_path_output}.')


# ############################### Monthly Avg Temperature ###############################


# df_temperature = pd.read_excel(file_path, sheet_name='Daily Avg Temperature', parse_dates=['Timestamp'])
# df_temperature.set_index('Timestamp', inplace=True)
# monthly_avg_temperature = df_temperature.resample('M').apply(
#     lambda x: x.mean() if not x.isna().all().any() and x.notna().sum() >= 0.7 * len(x) else np.nan
# )

# file_path_output = 'MonthlyAvgTemperature.xlsx'
# monthly_avg_temperature.to_excel(file_path_output, sheet_name='Monthly Lake Level')

# print(f'Monthly Average Temperature data written to {file_path_output}.')

# ############################### Monthly Avg Humidity ###############################


# df_humidity = pd.read_excel(file_path, sheet_name='Daily Avg Humidity', parse_dates=['Timestamp'])
# df_humidity.set_index('Timestamp', inplace=True)
# monthly_avg_humidity = df_humidity.resample('M').apply(
#     lambda x: x.mean() if not x.isna().all().any() and x.notna().sum() >= 0.7 * len(x) else np.nan
# )

# file_path_output = 'MonthlyAvgHumidity.xlsx'
# monthly_avg_humidity.to_excel(file_path_output, sheet_name='Monthly Relative Humidity')

# print(f'Monthly Average Humidity data written to {file_path_output}.')


file_name = 'Namal Catchment Monthly Dataset-V2.xlsx'

with pd.ExcelWriter(file_name, engine=('openpyxl')) as writer:
    monthly_precipitation.to_excel(writer, sheet_name='Monthly Precipitation')
    monthly_lakeLevel.to_excel(writer, sheet_name='Monthly Lake Level')
    # monthly_avg_temperature.to_excel(writer, sheet_name='Monthly Avg Temperature')
    # monthly_avg_humidity.to_excel(writer, sheet_name='Monthly Avg Humidity')
    monthly_StreamLevel.to_excel(writer, sheet_name='Monthly Stream Level')
print(f'Monthly data written to {file_name}.')

