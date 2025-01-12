from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, SensorData
from datetime import datetime
import pandas as pd
import google.generativeai as genai

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

genai.configure(api_key="AIzaSyAy2h11mWJ-ew43uVR2SZ3cMyqt8cTgfbs") # add api key here
model = genai.GenerativeModel("gemini-1.5-flash")


with app.app_context():
    db.create_all()

# Read CSV data
df = pd.read_csv('solar_teg_dataset.csv')

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.json
    new_data = SensorData(
        temperature_front=data['temperature_front'],
        temperature_back=data['temperature_back'],
        current_teg=data['current_teg'],
        current_solar=data['current_solar'],
        voltage_solar=data['voltage_solar'],
        voltage_teg=data['voltage_teg'],
        power_solar=data['power_solar'],
        power_teg=data['power_teg']
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({"status": "success"}), 200

@app.route('/data')
def data():
    latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()
    if latest_data:
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
    latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()
    if latest_data:
        return render_template('index.html',
                           temperature_front=latest_data.temperature_front,
                           temperature_back=latest_data.temperature_back,
                           current_teg=latest_data.current_teg,
                           current_solar=latest_data.current_solar,
                           voltage_solar=latest_data.voltage_solar,
                           voltage_teg=latest_data.voltage_teg,
                           power_solar=latest_data.power_solar,
                           power_teg=latest_data.power_teg)
    else:
        return render_template('index.html',
                           temperature_front=0,
                           temperature_back=0,
                           current_teg=0,
                           current_solar=0,
                           voltage_solar=0,
                           voltage_teg=0,
                           power_solar=0,
                           power_teg=0)

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

@app.route('/graph_data')
def graph_data():
    data = SensorData.query.order_by(SensorData.timestamp).all()
    data_list = [entry.to_dict() for entry in data]
    return jsonify(data_list)

@app.route('/simulation_analysis')
def simulation_analysis():
    return render_template('simulation_analysis.html')

@app.route('/csv_data')
def csv_data():
    # Convert DataFrame to list of dictionaries
    data = df.to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')