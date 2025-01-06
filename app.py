from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

@app.route('/data')
def data():
    temperature_front = random.uniform(20, 30)
    temperature_back = random.uniform(20, 30)
    current_teg = random.uniform(0, 2)
    current_solar = random.uniform(0, 5)
    voltage_solar = random.uniform(0, 12)
    voltage_teg = random.uniform(0, 5)
    power_solar = voltage_solar * current_solar
    power_teg = voltage_teg * current_teg
    return jsonify({
        'temperature_front': round(temperature_front, 2),
        'temperature_back': round(temperature_back, 2),
        'current_teg': round(current_teg, 2),
        'current_solar': round(current_solar, 2),
        'voltage_solar': round(voltage_solar, 2),
        'voltage_teg': round(voltage_teg, 2),
        'power_solar': round(power_solar, 2),
        'power_teg': round(power_teg, 2)
    })

@app.route('/data_page')
def data_page():
    data = [
        {
            'temperature_front': round(random.uniform(20, 30), 2),
            'temperature_back': round(random.uniform(20, 30), 2),
            'current_teg': round(random.uniform(0, 2), 2),
            'current_solar': round(random.uniform(0, 5), 2),
            'voltage_solar': round(random.uniform(0, 12), 2),
            'voltage_teg': round(random.uniform(0, 5), 2),
            'power_solar': round(random.uniform(0, 60), 2),
            'power_teg': round(random.uniform(0, 10), 2)
        }
        for _ in range(10)
    ]
    return render_template('Data.html', data=data)

@app.route('/')
def index():
    # Generate random data for the current variables
    temperature_front = round(random.uniform(20, 30), 2)
    temperature_back = round(random.uniform(20, 30), 2)
    current_teg = round(random.uniform(0, 2), 2)
    current_solar = round(random.uniform(0, 5), 2)
    voltage_solar = round(random.uniform(0, 12), 2)
    voltage_teg = round(random.uniform(0, 5), 2)
    power_solar = voltage_solar * current_solar
    power_teg = voltage_teg * current_teg

    return render_template('index.html',
                           temperature_front=temperature_front,
                           temperature_back=temperature_back,
                           current_teg=current_teg,
                           current_solar=current_solar,
                           voltage_solar=voltage_solar,
                           voltage_teg=voltage_teg,
                           power_solar=power_solar,
                           power_teg=power_teg)

if __name__ == '__main__':
    app.run(debug=True)