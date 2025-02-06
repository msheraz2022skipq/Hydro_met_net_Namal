import pandas as pd
from dateutil import parser

# read the CSV file
csvTable = pd.read_csv('Dhibba Karsiyal 08Aug-10Oct2024.csv', usecols=["Reading Time", "Depth mm", "Temperature", "Rain mm", "Humidity (%)"])
# convert all time stamps into the same time format
# exclude the samples having wrong time stamp
for i, row in csvTable.iterrows():
    try:
        # Check if the time value is in the expected format ("%d/%m/%Y %I:%M:%S %p")
        if len(row['Reading Time']) < 12:
            raise parser.ParserError
        parsed_time = parser.parse(row['Reading Time'], dayfirst=True)
        csvTable.at[i, 'Reading Time'] = parsed_time
    except parser.ParserError:
        print(row['Reading Time'])
        csvTable = csvTable.drop(i)

# Drop any remaining rows that still contain invalid date-time values
csvTable = csvTable.dropna(subset=['Reading Time'])
# remove duplicates
csvTable = csvTable.drop_duplicates()
csvTable = csvTable.sort_values(by='Reading Time', ascending=False)
Sonar_data = csvTable[["Reading Time", "Depth mm"]]
Temperature_data = csvTable[["Reading Time", "Temperature"]]
Rain_data = csvTable[["Reading Time", "Rain mm"]]
Humidity_data = csvTable[["Reading Time", "Humidity (%)"]]
#Validate Data
#BudhyWali unit sonar is having around 2300 mm distance from earch in actual
Sonar_data.loc[~Sonar_data['Depth mm'].between(5000,8000), 'Depth mm'] = pd.NA
Humidity_data.loc[~Humidity_data['Humidity (%)'].between(0,100), 'Humidity (%)'] = pd.NA
Temperature_data.loc[~Temperature_data['Temperature'].between(-25,60), 'Temperature'] = pd.NA
Rain_data.loc[~Rain_data['Rain mm'].between(0,500), 'Rain mm'] = pd.NA
print('Ground Distance is ',Sonar_data['Depth mm'].max())
#Convert Depth into feets
Sonar_data['Depth mm'] = Sonar_data['Depth mm']*(3.281/1000)
Sonar_data = Sonar_data.rename(columns={'Depth mm': 'Depth in ft'})
Rain_data['Rain mm'] = Rain_data['Rain mm'] * 0.246
#calculate stream level
Range_data = Sonar_data
pd.to_numeric(Sonar_data['Depth in ft'], errors='coerce')
Range_data['Stream_level'] = Range_data['Depth in ft'].max() - Range_data['Depth in ft']
Stream_lev = Range_data[["Reading Time", "Stream_level"]]
#Write data into csv file
Temperature_data.to_csv('Level Sensor 3 - DhibbaKarsiyal_Temp.csv', index=False)
Rain_data.to_csv('Level Sensor 3 - DhibbaKarsiyal_Rain.csv', index=False)
Humidity_data.to_csv('Level Sensor 3 - DhibbaKarsiyal_Humidity.csv', index=False)
Stream_lev.to_csv('Level Sensor 3 - DhibbaKarsiyal_Streanlevel.csv', index=False)
#Create comprehensive data file
comprehensive = Stream_lev.merge(Rain_data, on='Reading Time', how='inner')\
                        .merge(Temperature_data, on='Reading Time', how='inner')\
                        .merge(Humidity_data, on='Reading Time', how='inner')

comprehensive.to_csv('Level Sensor 3 - DhibbaKarsiyal_comprehensive.csv', index=False)

####################### Data plots ###########################

print("Plotting Data...")
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

# Read the comprehensive data file
comprehensive_df = pd.read_csv('Level Sensor 3 - DhibbaKarsiyal_comprehensive.csv')

# Convert the 'DateAndTime' column to datetime type
comprehensive_df['Reading Time'] = pd.to_datetime(comprehensive_df['Reading Time'])

print("Plotting Level, Rain, Temperature, and Humidity...")
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(comprehensive_df['Reading Time'], comprehensive_df['Rain mm'], color='black', label='Rain (mm)', width=1)
ax1.set_ylabel('Rain (mm)', color='black')
ax2 = ax1.twinx()
ax2.plot(comprehensive_df['Reading Time'], comprehensive_df['Temperature'], color='blue', label='Temperature')
ax2.set_ylabel('Temperature', color='blue')
ax3 = ax1.twinx()
ax3.spines['right'].set_position(('outward', 60))
ax3.plot(comprehensive_df['Reading Time'], comprehensive_df['Stream_level'], color='orange', label='Stream Level')
ax3.set_ylabel('Stream Level', color='orange')
ax1.set_xlabel('Date and Time')
ax1.set_title('BudhyWali - Rain, Temperature, and Stream Level')
# Format the x-axis ticks to show only month and year
ax1.xaxis.set_major_locator(mdates.MonthLocator())  # Set tick locator to months
date_fmt = mdates.DateFormatter('%d-%b-%Y')
ax1.legend(loc='upper left', bbox_to_anchor=(0, 1))
ax2.legend(loc='upper left', bbox_to_anchor=(0, 0.95))
ax3.legend(loc='upper left', bbox_to_anchor=(0, 0.90))
fig.autofmt_xdate(rotation=45)
plt.tight_layout()  # Adjust layout to prevent clipping of labels
plt.savefig('Dhibba Karsiyal Rain, Temperature, and Stream Level Plot.png', dpi=300)
plt.show()
