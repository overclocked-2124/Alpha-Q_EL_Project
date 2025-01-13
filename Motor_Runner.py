from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import SensorData
import joblib
import time
import serial

# Database configuration
DATABASE_URI = 'sqlite:///sensor_data.db'

# Create the database engine and session
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Configure the serial connection
ser = serial.Serial(
    port='COM12',  # Replace with your ESP32's serial port
    baudrate=115200,
    timeout=1
)

try:
    while True:
        # Fetch the latest data from the SensorData table
        latest_data = session.query(SensorData).order_by(SensorData.timestamp.desc()).first()
        if latest_data:
            # Prepare input data for the model
            input_data = [[
                latest_data.temperature_front,
                latest_data.irradience_front,  # Replace with actual irradiance if different
                latest_data.temperature_front * latest_data.irradience_front,
                19.881,  # Replace with actual solar efficiency value
                6.0653,  # Replace with actual TEG efficiency value
                15.736  # Replace with actual net efficiency value
            ]]

            # Load the trained model
            model = joblib.load('solar_panel_model.pkl')

            # Make a prediction
            prediction = model.predict(input_data)
            print(f"Prediction: {prediction[0]}")

            # Send the prediction to the ESP32
            ser.write(str(prediction[0]).encode())
            time.sleep(0.1)  # Give the ESP32 time to receive the data

        time.sleep(2)  # Adjust the interval as needed

except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    ser.close()
    session.close()