from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature_front = db.Column(db.Float)
    temperature_back = db.Column(db.Float)
    current_teg = db.Column(db.Float)
    current_solar = db.Column(db.Float)
    voltage_solar = db.Column(db.Float)
    voltage_teg = db.Column(db.Float)
    power_solar = db.Column(db.Float)
    power_teg = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)