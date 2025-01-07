from flask import Flask, render_template, jsonify 
from flask_sqlalchemy import SQLAlchemy
from models import db, SensorData
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/data')
def data():
    latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()
    if latest_data:
        print("Latest data:", latest_data)  # Debugging
        return jsonify(latest_data.to_dict())
    else:
        return jsonify({})

@app.route('/data_page')
def data_page():
    data = SensorData.query.order_by(SensorData.timestamp.desc()).limit(50).all()
    data_list = [entry.to_dict() for entry in data]
    return render_template('Data.html', data=data_list)

@app.route('/data_page_data')
def data_page_data():
    data = SensorData.query.order_by(SensorData.timestamp.desc()).limit(50).all()
    data_list = [entry.to_dict() for entry in data]
    return jsonify(data_list)

@app.route('/')
def index():
    temperature_front = round(random.uniform(20, 30), 2)
    temperature_back = round(random.uniform(20, 30), 2)
    current_teg = round(random.uniform(0, 2), 2)
    current_solar = round(random.uniform(0, 5), 2)
    voltage_solar = round(random.uniform(0, 12), 2)
    voltage_teg = round(random.uniform(0, 5), 2)
    power_solar = voltage_solar * current_solar
    power_teg = voltage_teg * current_teg

    new_data = SensorData(
        temperature_front=temperature_front,
        temperature_back=temperature_back,
        current_teg=current_teg,
        current_solar=current_solar,
        voltage_solar=voltage_solar,
        voltage_teg=voltage_teg,
        power_solar=power_solar,
        power_teg=power_teg
    )
    db.session.add(new_data)
    db.session.commit()

    return render_template('index.html',
                           temperature_front=temperature_front,
                           temperature_back=temperature_back,
                           current_teg=current_teg,
                           current_solar=current_solar,
                           voltage_solar=voltage_solar,
                           voltage_teg=voltage_teg,
                           power_solar=power_solar,
                           power_teg=power_teg)

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

@app.route('/graph_data')
def graph_data():
    data = SensorData.query.order_by(SensorData.timestamp).all()
    data_list = [entry.to_dict() for entry in data]
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(debug=True)