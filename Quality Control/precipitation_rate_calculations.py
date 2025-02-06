import pandas as pd
import numpy as np

file_path = 'Clean Data 01Apr-30Sep2024-Processed.xlsx'
df_precipitation = pd.read_excel(file_path, sheet_name='Rain')

df_precipitation.sort_values(by='Timestamp', inplace=True)

########################## Remove Zero-anomalies ##############################

df_corrected_precipitation = df_precipitation.copy()
for col in df_precipitation.columns[1:]:
    mask_anomaly = (df_precipitation[col] == 0) & (df_precipitation[col].shift(-1) > 0) & (df_precipitation[col].shift(1) > 0)
    df_corrected_precipitation[col] = df_precipitation[col].where(~mask_anomaly, np.nan)
with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
    df_corrected_precipitation.to_excel(writer, sheet_name='Precipitation', index=False)
print(f'Corrected precipitation data written to Precipitation Sheet.')
########################### Rainfall Rate Calculations ########################
df_precipitation = pd.read_excel(file_path, sheet_name='Precipitation')
df_precipitaionRate = pd.DataFrame({'Timestamp': df_precipitation['Timestamp']})
for col in df_precipitation.columns[1:]:
    precipitation_col = df_precipitation[col].diff().clip(lower=0)
    df_precipitaionRate[f'{col}'] = precipitation_col

with pd.ExcelWriter(file_path, engine='openpyxl', mode='a') as writer:
    df_precipitaionRate.to_excel(writer, sheet_name='Precipitation Rate', index=False)

print(f'Precipitation rate data written to file.')
############################   Daily Rainfall     #############################


df_precipitation = pd.read_excel(file_path, sheet_name='Precipitation', parse_dates=['Timestamp'])
df_precipitation.set_index('Timestamp', inplace=True)
daily_precipitation = pd.DataFrame(index=df_precipitation.resample('D').mean().index)
for col in df_precipitation.columns:
    daily_precipitation[col] = df_precipitation[col].resample('D').apply(
        lambda x: x.iloc[-1] if x.iloc[-1] == x.iloc[-1] else x.iloc[:-1].max() if x.iloc[:-1].notna().any() else np.nan
    )

file_path_output = 'DailyPrecipitation.xlsx'
daily_precipitation.to_excel(file_path_output, sheet_name='Daily Precipitation')

print(f'Daily Rainfall data written to {file_path_output}.')