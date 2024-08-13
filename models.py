from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    purchase_date = db.Column(db.Date)
    light_conditions = db.Column(db.String(64))
    watering_frequency = db.Column(db.String(64))
    fertilizing_frequency = db.Column(db.String(64))
    notes = db.Column(db.String(256))
    user_id = db.Column(db.Integer, nullable=False)
