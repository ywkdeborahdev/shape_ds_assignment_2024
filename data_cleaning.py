import pandas as pd


outputFileName = "output2/yuenlong/concatenated_output.csv"
# Read the CSV file into a DataFrame
df = pd.read_csv(outputFileName)

# Data Cleaning
# Fill empty cells in 'bigEstateName' first with values from 'estateName', then from 'buildingName'
df['bigEstateName'] = df['bigEstateName'].fillna(df['estateName']).fillna(df['buildingName'])

# Save the updated DataFrame back to a CSV file
df.to_csv('example.csv', index=False)

print("New column added successfully.")