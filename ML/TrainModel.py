import joblib
import pandas as pd
import sklearn
print("Scikit-learn version in TrainModel.py:", sklearn.__version__)

# Load the saved model
model = joblib.load('solar_panel_model.pkl')
print("Model loaded successfully.")
print(f"Model type: {type(model)}")  # Should print <class 'sklearn.ensemble._forest.RandomForestClassifier'>

# Example input data
example_data = [[50, 1000,50000, 19.881, 6.0653, 15.736]]
example_df = pd.DataFrame(example_data, columns=[
    'Temperature_C', 'Irradiance_W_m2','Temp_Irrad_Product', 'Solar_Efficiency', 'TEG_Efficiency', 'Net_Efficiency'
])

# Make a prediction
prediction = model.predict(example_df)
print("Prediction for example:", prediction)