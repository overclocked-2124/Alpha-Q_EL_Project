from flask import Flask, render_template, jsonify
import random  # For simulating sensor data

app = Flask(__name__)

# Simulated data endpoint
@app.route('/data')
def data():
    # Simulate sensor data
    voltage = random.uniform(0, 5)  # Simulated voltage value
    current = random.uniform(0, 10)  # Simulated current value
    temperature = random.uniform(20, 30)  # Simulated temperature value
    return jsonify({'voltage': voltage, 'current': current, 'temperature': temperature})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)