from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import SensorData
import pandas as pd
import csv

# Define the column headers
headers = ['Temperature_C', 'Irradiance_W_m2', 'Temp_Irrad_Product', 'Solar_Efficiency', 'TEG_Efficiency', 'Net_Efficiency']

# Specify the file name
file_name = 'data.csv'

# Create and write headers to the CSV file
with open(file_name, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)

print(f"Empty CSV file '{file_name}' created with headers: {headers}")

# Database configuration
DATABASE_URI = 'sqlite:///data.db'  # Replace with your database URI

# Create the database engine and session
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Fetch all data from the SensorData table
print("Fetching all data:")
all_data = session.query(SensorData).all()

# Initialize a list to store rows
rows = []

# Iterate over all rows in all_data
for row in all_data:
    # Extract relevant data from the row and append to the list
    row_data = [
        row.temperature_front,  # Replace with the correct attribute for Temperature_C
        row.irradiance,         # Replace with the correct attribute for Irradiance_W_m2
        row.temperature_front * row.irradiance,  # Temp_Irrad_Product
        19.881, 6.0653, 15.736    # Replace with the correct attribute for Net_Efficiency
    ]
    rows.append(row_data)

# Create a DataFrame from the rows
df = pd.DataFrame(rows, columns=headers)

# Append the data to the CSV file
df.to_csv(file_name, mode='a', index=False, header=False)

print(f"Data appended to the CSV file '{file_name}'.")

# Print the DataFrame
print("DataFrame:")
print(df)

# Close the session
session.close()