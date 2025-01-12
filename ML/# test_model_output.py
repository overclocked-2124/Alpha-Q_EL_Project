# test_model_output.py

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load the trained model
model = joblib.load('solar_panel_model.pkl')
print("Model loaded successfully.")

# Define the range for temperature and irradiance
temperature_range = np.arange(55, 70, 1)  # Temperature from 15°C to 30°C in steps of 1°C
irradiance_range = np.arange(800, 1501, 10)  # Irradiance from 800 W/m² to 1500 W/m² in steps of 10 W/m²

# Fixed values for other features
solar_efficiency = 19.881
teg_efficiency = 6.0653
net_efficiency = 15.736

# Iterate over the temperature and irradiance ranges
for temp in temperature_range:
    for irrad in irradiance_range:
        # Create the input data
        input_data = [[temp, irrad, solar_efficiency, teg_efficiency, net_efficiency]]
        input_df = pd.DataFrame(input_data, columns=[
            'Temperature_C', 'Irradiance_W_m2', 'Solar_Efficiency', 'TEG_Efficiency', 'Net_Efficiency'
        ])
        
        # Make a prediction
        prediction = model.predict(input_df)
        
        # Print the results
        print(f"Temperature: {temp}°C, Irradiance: {irrad} W/m², Predicted Action: {prediction[0]}")