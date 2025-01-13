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
    irradience_front = db.Column(db.Float)
    irradience_back = db.Column(db.Float)
    irradience_onsolar = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'temperature_front': self.temperature_front,
            'temperature_back': self.temperature_back,
            'current_teg': self.current_teg,
            'current_solar': self.current_solar,
            'voltage_solar': self.voltage_solar,
            'voltage_teg': self.voltage_teg,
            'power_solar': self.power_solar,
            'power_teg': self.power_teg,
            'irradience_front': self.irradience_front,
            'irradience_back': self.irradience_back,
            'irradience_onsolar': self.irradience_onsolar,
            'timestamp': self.timestamp.isoformat()
        }