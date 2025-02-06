import pandas as pd

# Read the CSV file and select specific columns
csvTable = pd.read_csv('Dhoke Peera 16Aug-10Oct2024_proper_time.csv', usecols=["Reading Time", "Temp (DS18B20)", "Rain mm", "Humidity (%)"])
csvTable['Reading Time'] = pd.to_datetime(csvTable['Reading Time'])
#csvTable['Reading Time'] = csvTable['Reading Time'].dt.strftime('%d/%m/%Y %I:%M:%S %p')
csvTable = csvTable.dropna(subset=['Reading Time'])
csvTable = csvTable.drop_duplicates(subset=['Reading Time'])

# Validate Data
csvTable['Humidity (%)'] = csvTable['Humidity (%)'].where(csvTable['Humidity (%)'].between(0, 100), pd.NA)
csvTable['Temp (DS18B20)'] = csvTable['Temp (DS18B20)'].abs().where((csvTable['Temp (DS18B20)'] < 0) & (csvTable['Temp (DS18B20)'].shift(1) > 5), csvTable['Temp (DS18B20)'])
csvTable['Rain mm'] = csvTable['Rain mm'].where(csvTable['Rain mm'].between(0, 1500), pd.NA)
csvTable['Rain mm'] = csvTable['Rain mm'] * 0.246  # Convert to feet
# Write cleaned data into CSV files
csvTable[["Reading Time", "Temp (DS18B20)"]].to_csv('Rain Gauge 2 - DhokePeera_Temp.csv', index=False)
csvTable[["Reading Time", "Rain mm"]].to_csv('Rain Gauge 2 - DhokePeera_Rain.csv', index=False)
csvTable[["Reading Time", "Humidity (%)"]].to_csv('Rain Gauge 2 - DhokePeera_Humidity.csv', index=False)
# Create comprehensive data file
comprehensive = csvTable[["Reading Time", "Rain mm","Temp (DS18B20)", "Humidity (%)"]]
comprehensive.to_csv('Rain Gauge 2 - DhokePeera_comprehensive.csv', index=False)
#####################################################################################
# Plot Rain, Temperature, and Humidity
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Read the data
comprehensive_df = pd.read_csv('Rain Gauge 2 - DhokePeera_comprehensive.csv')

# Convert 'Reading Time' to datetime if it's not already in datetime format
comprehensive_df['Reading Time'] = pd.to_datetime(comprehensive_df['Reading Time'])

# Plot Rain, Temperature, and Humidity
print("Plotting Rain, Temperature, and Humidity...")
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(comprehensive_df['Reading Time'], comprehensive_df['Rain mm'], color='black', label='Rain (mm)', width=1)
ax1.set_ylabel('Rain (mm)', color='black')

ax2 = ax1.twinx()
ax2.plot(comprehensive_df['Reading Time'], comprehensive_df['Temp (DS18B20)'], color='blue', label='Temperature')
ax2.set_ylabel('Temperature', color='blue')

ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))
ax3.plot(comprehensive_df['Reading Time'], comprehensive_df['Humidity (%)'], color='orange', label='Humidity')
ax3.set_ylabel('Humidity', color='orange')

ax1.set_xlabel('Date and Time')
ax1.set_title('Dhoke Peera - Rain, Temperature, and Humidity')

# Format the x-axis ticks to show only month and year
ax1.xaxis.set_major_locator(mdates.MonthLocator())  # Set tick locator to months
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))  # Format the tick labels

ax1.legend(loc='upper left', bbox_to_anchor=(0, 1))
ax2.legend(loc='upper left', bbox_to_anchor=(0, 0.95))
ax3.legend(loc='upper left', bbox_to_anchor=(0, 0.90))

fig.autofmt_xdate(rotation=45)
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.savefig('Dhoke Peera Rain, Temperature, and Humidity Plot.png', dpi=300)
plt.show()

