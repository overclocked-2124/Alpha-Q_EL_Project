import requests
import time
import random

# Flask server URL
SERVER_URL = "http://127.0.0.1:5000/receive_data"  # Replace with your server's IP and port if needed


def generate_mock_sensor_data():
    """
    Generates fake sensor data for testing.
    """
    return {
        "temperature_front": round(random.uniform(20, 30), 2),  # Random temperature between 20°C and 30°C
        "temperature_back": round(random.uniform(20, 30), 2),  # Random temperature between 20°C and 30°C
        "current_teg": round(random.uniform(0, 2), 2),  # Random current between 0A and 2A
        "current_solar": round(random.uniform(0, 5), 2),  # Random current between 0A and 5A
        "voltage_solar": round(random.uniform(0, 12), 2),  # Random voltage between 0V and 12V
        "voltage_teg": round(random.uniform(0, 5), 2),  # Random voltage between 0V and 5V
        "power_solar": round(random.uniform(0, 60), 2),  # Random power between 0W and 60W
        "power_teg": round(random.uniform(0, 10), 2),  # Random power between 0W and 10W
    }


def send_sensor_data():
    """
    Sends mock sensor data to the Flask server.
    """
    while True:
        # Generate fake sensor data
        sensor_data = generate_mock_sensor_data()

        response = requests.post(SERVER_URL, json=sensor_data)

        


if __name__ == "__main__":
    send_sensor_data()