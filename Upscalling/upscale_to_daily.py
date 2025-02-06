import pandas as pd
import numpy as np
file_path = 'Namal Catchement Dataset-Original.xlsx'
############################### Daily Precipitation ###############################
df_precipitation = pd.read_excel(file_path, sheet_name='Precipitation', parse_dates=['Timestamp'])
df_precipitation.set_index('Timestamp', inplace=True)
daily_precipitation = pd.DataFrame(index=df_precipitation.resample('D').mean().index)
for col in df_precipitation.columns:
    daily_precipitation[col] = df_precipitation[col].resample('D').apply(
        lambda x: x.iloc[-1] if x.iloc[-1] == x.iloc[-1] else x.iloc[:-1].max() if x.iloc[:-1].notna().any() else np.nan
    )

file_path_output = 'DailyPrecipitation.xlsx'
daily_precipitation.to_excel(file_path_output, sheet_name='Daily Precipitation')

print(f'Daily Precipitation data written to {file_path_output}.')

############################### Daily Lake Level ###############################

df_lakeLevel = pd.read_excel(file_path, sheet_name='Lake Level', parse_dates=['Timestamp'])
df_lakeLevel.set_index('Timestamp', inplace=True)
daily_lakeLevel = pd.DataFrame(index=df_lakeLevel.resample('D').mean().index)
for col in df_lakeLevel.columns:
    daily_lakeLevel[col] = df_lakeLevel[col].resample('D').apply(
        lambda x: x.median()
    )

file_path_output = 'DailyLakeLevel.xlsx'
daily_lakeLevel.to_excel(file_path_output, sheet_name='Daily Lake Level')

print(f'Daily Rainfall data written to {file_path_output}.')

############################### Daily Stream Level ###############################

df_StreamLevel = pd.read_excel(file_path, sheet_name='Stream Levels', parse_dates=['Timestamp'])
df_StreamLevel.set_index('Timestamp', inplace=True)
daily_StreamLevel = pd.DataFrame(index=df_StreamLevel.resample('D').mean().index)
for col in df_StreamLevel.columns:
    daily_StreamLevel[col] = df_StreamLevel[col].resample('D').apply(
        lambda x: x.max()
    )

file_path_output = 'DailyStreamLevel.xlsx'
daily_StreamLevel.to_excel(file_path_output, sheet_name='Daily Stream Level')

print(f'Daily Stream data written to {file_path_output}.')


# ############################### Daily Avg Temperature ###############################


# df_temperature = pd.read_excel(file_path, sheet_name='Temperature', parse_dates=['Timestamp'])
# df_temperature.set_index('Timestamp', inplace=True)
# daily_avg_temperature = df_temperature.resample('D').apply(
#     lambda x: x.mean() if not x.isna().all().any() and x.notna().sum() >= 0.7 * len(x) else np.nan
# )

# file_path_output = 'DailyAvgTemperature.xlsx'
# daily_avg_temperature.to_excel(file_path_output, sheet_name='Daily Lake Level')

# print(f'Daily Average Temperature data written to {file_path_output}.')

# ############################### Daily Avg Humidity ###############################


# df_humidity = pd.read_excel(file_path, sheet_name='Relative Humidity', parse_dates=['Timestamp'])
# df_humidity.set_index('Timestamp', inplace=True)
# daily_avg_humidity = df_humidity.resample('D').apply(
#     lambda x: x.mean() if not x.isna().all().any() and x.notna().sum() >= 0.7 * len(x) else np.nan
# )

# file_path_output = 'DailyAvgHumidity.xlsx'
# daily_avg_humidity.to_excel(file_path_output, sheet_name='Daily Relative Humidity')

# print(f'Daily Average Humidity data written to {file_path_output}.')


file_name = 'Namal Catchment Daily Dataset-V3.xlsx'

with pd.ExcelWriter(file_name, engine=('openpyxl')) as writer:
    daily_precipitation.to_excel(writer, sheet_name='Daily Precipitation')
    daily_lakeLevel.to_excel(writer, sheet_name='Daily Lake Level')
    # daily_avg_temperature.to_excel(writer, sheet_name='Daily Avg Temperature')
    # daily_avg_humidity.to_excel(writer, sheet_name='Daily Avg Humidity')
    daily_StreamLevel.to_excel(writer, sheet_name='Daily Stream Level')
print(f'Daily data written to {file_name}.')

