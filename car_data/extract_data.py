# Parses out all cars sold with manual transmission from 1984-2025 from EPA data file

import pandas as pd

# read in specified columns from csv file to pandas dataframe
df = pd.read_csv('vehicles.csv')[['year', 'make', 'model', 'trany', 'cylinders']]

# filter rows to only select cars offered with a manual transmission
manual_cars = df[df['trany'].str.contains('Manual', case=False, na=False)]

# sort ascending
df_ascending = manual_cars.sort_values(by='year')

df_ascending.to_csv('parsed_data.csv', index=False)


# print(df_ascending)

# output to .txt file
# with open('parsed_data.txt', 'w') as f:
#     print(df_ascending.to_string(), file=f)
